"""
This module provides utilities, functions, and other code that is \
meant to be used across the app. This may undergo changes soon.

Functions:
    - cleanup: Clean up after the Dash app exits.
    - create_dropdown: Create a dropdown with a title.
    - create_table: Creates a `dash_table.DataTable` given a `pd.DataFrame`.
    - create_trace_dropdown: Create a menu item for traces.
    - convert_schema_to_frictionless: Convert the schema from our internal \
                                      format to the frictionless-data format.
    - get_dataset_options: Get datasets available to user as options for \
                           `dcc.Dropdown`.
    - get_data_schema: Get a dict with the specified dataset's schema.
    - hard_cast_to_float: Convert to float or return 0.
    - interactive_menu: Create the necessary elements for the sidemenus \
                        to become interactive.
    - save_schema: Save the schema including a preview for the data.
    - parse_contents: Decode uploaded files and store them in Redis.
    - redis_startup: Connect to a Redis server & handle startup.

Global variables:
    - redis_conn: A Redis connection that is used throughout the app.
    - mapping: A dict that maps tags to sklearn models meant for \
               creating dropdowns and used in `apps.analyze` modules.

Notes to others:
    You should probably not write code here, unless you are adding \
    functions aimed at being used by many lower-level modules. \
    Some of the functions here will later be moved to lower-level \
    modules (e.g. `pretty_print_tweets`).
"""

import dash_html_components as html
import dash_core_components as dcc
import dash_table

import visdcc

from data.data_utils.schema_heuristics import infer_types
from models import User, DataSchemas, db
from users_mgt import show_apps

from flask_login import current_user
from itertools import chain
from functools import wraps
from datetime import datetime
import pandas as pd
import numpy as np
import dill
import feather
import base64
import json
import io
import redis
import os
import tempfile


def check_user_access(app_name):
    """
    A decorator that handles the case where a user is not permitted to \
    access a certain app.
    """

    def decorator_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the list of apps for the current user
            user_apps = []
            if current_user.is_authenticated:
                user = User.query.get(current_user.id)
                user_apps = show_apps(user)

            # Inform the user that they have no access to the app
            if app_name not in user_apps:
                return [html.Div([
                    html.H3("You do not have access to this app. If you "
                            "require access, contact an administrator.")
                ]), []]

            # Or return the normal output
            else:
                return func(*args, **kwargs)

        return wrapper
    return decorator_func


def cleanup(redis_conn):
    """
    Clean up after the Dash app exits.

    Args:
        redis_conn: `redis.Redis` object.

    Further details:
        Flush every key stored in the Redis database. If there \
        are users that have logged in and uploaded data, store \
        those on disk.
    """

    # Get all keys and their data in a dict and save the dict
    # as a pickle
    redis_data = {k.decode(): redis_conn.get(k)
                  for k in redis_conn.keys('*')}

    with open("redisData.pkl", "wb") as f:
        dill.dump(redis_data, f)

    print("Cleaning up...")
    redis_conn.flushdb()


def create_dropdown(name, options, type_="regular", **kwargs):
    """
    Create a dropdown with a title.

    Args:
        name (str): the title above the dropdown.
        options (list(dict)): dictionaries should contain keys at least \
                             the keys (label, value).
        **kwargs: keyword-value pairs. Accepts any keyword-arguments \
                  that can be passed to `dcc.Dropdown`.

    Returns:
        list: an H5 and the Dropdown.
    """

    if type_ == "regular":
        return [
            html.H6(name+":"),
            dcc.Dropdown(
                options=options,
                **kwargs
            )]

    else:
        return html.Div([
            html.Div(name, className="trace-variable-name"),
            html.Div(dcc.Dropdown(options=options, **kwargs,
                                  className="plot-menu-input"),
                     className="plot-menu-input-div"),
        ], className="trace-menu-row")


def create_table(df, table_id="table", columns=None):
    """
    Creates a `dash_table.DataTable` given a `pandas.DataFrame`.

    Args:
        df (`pandas.DataFrame`): the data.
        table_id (str, optional): id of the table element for usage \
                                  with dash callbacks.
        columns (list(dict)): the column data passed to the data table.

    Returns:
        A `dash_table.DataTable` with pagination.
    """

    if columns is None:
        columns = [{"name": i, "id": i} for i in df.columns]

    return html.Div([
        dash_table.DataTable(
            id=table_id,
            columns=columns,
            data=df.to_dict("rows"),
            style_table={
                'maxHeight': '450px',
            },
            sort_action="native",
            sort_mode='multi',
            editable=True,
            filter_action="native",
            page_action='native',
            page_current=0,
            page_size=10,
            style_cell={
                'minWidth': '100px',
                'paddingLeft': '15px',
                "textAlign": "left",
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(218, 218, 218)'
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                },
            ],
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'rgb(230,230,230)',
                "fontWeight": "bold",
                "textAlign": "left",
                "paddingLeft": "5px"
            },
        )
    ], style={
        "overflowX": "auto",
        "overflowY": "hidden",
    })


def convert_schema_to_frictionless(schema):
    """
    Convert the schema from our internal format to the frictionless-data \
    format. See: https://frictionlessdata.io/specs/table-schema/
    """

    types = schema["types"]
    subtypes = schema["subtypes"]
    head = schema["head"]

    return {"fields": [{"name": col_name, "type": types[col_name],
                        "subtype": subtypes[col_name],
                        "data": head[col_name].values}
                       for col_name in types]}


def get_dataset_options(redis_conn):
    """
    Get datasets available to user as options for `dcc.Dropdown`.

    Args:
        redis_conn (`redis.Redis`): Connection to a Redis database.

    Returns:
        list(dict): A list of options to be used for making \
                    dropdowns for variables.
    """

    user_id = current_user.username

    # Get all available datasets's keys
    dataset_keys = redis_conn.keys(f"{user_id}_data_*")

    # Also get the example datasets' keys
    example_dataset_keys = redis_conn.keys(f"example_data_*")

    # Join the two and decode them
    dataset_keys = [key.decode() for key in chain(dataset_keys,
                                                  example_dataset_keys)]

    # Create the "options" for dcc elements
    available_datasets = [
        {'label': k, 'value': k}
        for k in dataset_keys
    ]

    return available_datasets


def get_data_schema(dataset_key, redis_conn):
    """
    Get a dict with the specified dataset's schema. The schema contains \
    three keys: types (int, float, ...), subtypes (binary, email, ...), \
    and head (5 rows from the `pd.DataFrame` sample).

    Args:
        dataset_key (str): the key used by the Redis server \
                           to store the data.
        redis_conn (`redis.Redis`): Connection to a Redis database.

    Returns:
        dict: The dataset schema
    """

    schema_key = dataset_key.replace("_data_", "_schema_")

    if redis_conn.exists(schema_key):
        return dill.loads(redis_conn.get(schema_key))

    return None


def get_variable_options(dataset_key, redis_conn):
    """
    Get available variables / columns as options for `dcc.Dropdown`.

    Args:
        dataset_key (str): the key used by the Redis server \
                           to store the data.
        redis_conn (`redis.Redis`): Connection to a Redis database.

    Returns:
        list(dict): A list of options to be used for making \
                    dropdowns for variables.
    """

    df_schema = get_data_schema(dataset_key, redis_conn)["types"]

    if df_schema is None:
        return []

    else:
        return [{'label': col[:35], 'value': col} for col in df_schema]


def hard_cast_to_float(x):
    """
    Convert to float or return 0.

    Args:
        x (anything): will be type-casted or 0'ed.

    Returns:
        float.
    """

    try:
        ret = np.float32(x)
    except ValueError:
        ret = 0.

    return ret


def interactive_menu(output_elem_id):
    """
    Create the necessary elements for the sidemenus to become interactive.

    Args:
        output_elem_id (str): The id for the div with the contents \
                          of the sidemenu.

    Returns:
        list: Dash elements, the sidebar, its buttons, and the \
              JS script to be run.
    """

    return [
        # The second sidebar with the tab-specific menu
        html.Div(id="sidenav2", className="sidenav2", children=[
            # Close button for the sidebar
            html.A(html.I(className="fas fa-times"), className="closebtn2",
                   id="closebtn2"),

            # Contents of the sidebar
            html.Div(id=output_elem_id),
        ]),

        # Open button for the sidebar
        html.Span(id="open_menu2", className="open_menu2", children=[
            html.I(className="fas fa-angle-double-right"),
        ]),

        # Interactivity: opening/closing the sidebar resizes
        # the main div and hides/shows appropriate menu buttons
        visdcc.Run_js(id='close_sidebar', run="""
            // show the button for opening the submenu
            var elem = document.getElementById("open_menu2");
            elem.style.display = "inline-block";
            
            // and bind the appropriate function to it
            elem.onclick = function(){openNav2()};
    
            // do the same for the close button
            var elem2 = document.getElementById("closebtn2");
            elem2.onclick = function(){closeNav2()};
        """)
    ]


def save_schema(key, types, subtypes, head, redis_conn, user_id,
                schema_status, redis_kwargs={}):
    """
    Save the schema including a preview for the data.

    Args:
        key (str): The Redis key where to save the data.
        types (dict): Mapping of columns to data types.
        subtypes (dict): Mapping of columns to secondary data types.
        head (`pd.DataFrame`): The first 5 rows of the data.
        redis_conn (`redis.Redis`): The connection to the desired database.
        user_id (str): The user for whom to fetch data.
        schema_status (str): Whether the schema was inferred or if \
                             the user explicitly changed it. Can be \
                             "ground_truth" or "inferred".

    Returns:
        bool: Whether Redis successfully stored the key.
    """

    if not isinstance(head, pd.DataFrame):
        raise ValueError("Incorrect data type for 'head'.")

    if len(head) > 5:
        head = head[:5]

    schema = {
        "types": types,
        "subtypes": subtypes,
        "head": head
    }

    # Save it in Redis
    ret = redis_conn.set(key, dill.dumps(schema), **redis_kwargs)

    # Also save to SQL.
    user = User.query.filter_by(username=user_id).first()
    new_schema = DataSchemas(user_id=user.id, timestamp=datetime.now(),
                             schema=schema, schema_status=schema_status)
    db.session.add(new_schema)
    db.session.commit()

    return ret


# TODO: better user feedback on error.
def parse_contents(contents, filename, date, user_id, redis_conn):
    """
    Decode uploaded files and store them in Redis.

    Args:
        contents (str): The content of the file to be decoded.
        filename (str): Name of uploaded file.
        date (str): (modification?) date of the file.
        user_id (str): The user for whom to fetch data.
        redis_conn (`redis.Redis`): The connection to the desired database.

    Further details:
        After decoding the uploaded file, handle any remaining \
        operations here. This was stolen from the dash docs. Currently \
        it only supports csv, xls(x), json, and feather file types.
    """

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    name, extension = os.path.splitext(filename)

    try:
        if extension == ".csv":
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        elif ".xls" in extension:
            df = pd.read_excel(io.BytesIO(decoded))

        elif extension == ".json":
            try:
                df = pd.DataFrame.from_dict(json.loads(decoded.decode('utf-8')))
            except ValueError:
                # JSON file is probably only one row, so convert it to list
                df = pd.DataFrame.from_dict([json.loads(decoded.decode('utf-8'))])

        elif extension == ".feather":
            # Assume that the user uploaded a feather file
            # Since this only reads from a file, we create
            # a temporary file
            with tempfile.NamedTemporaryFile() as tmp:
                tmp.write(decoded)
                # Pandas read_feather doesn't seem to work
                df = feather.read_dataframe(tmp.name)

        else:
            return html.Div(['Format not yet supported.'])

    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])

    # Store to redis.
    # IMPORTANT: Follow this key naming schema:
    # {user_id}_{data|connection|schema|has_connected}_{source}_{name}
    redis_conn.set(f"{user_id}_data_userdata_{name}", dill.dumps(df))

    # Take a sample and infer the schema from that
    sample = df.sample(n=50, replace=True).dropna()
    types, subtypes = infer_types(sample, is_sample=True)

    # Save the inferred schema to Redis
    save_schema(key=f"{user_id}_schema_userdata_{name}",
                types=types, subtypes=subtypes,
                head=sample.head(),
                redis_conn=redis_conn,
                user_id=user_id,
                schema_status="inferred")

    return html.Div([
        "Data uploaded successfully."
    ])


def redis_startup():
    """
    Connect to a Redis server & handle startup.

    Returns:
        `redis.Redis`: a connection to a Redis server.

    Further details:
        Connects to a Redis server on its default port (6379) and is \
        also responsible for any other startup operations needed such \
        as reading the data from the previous use.
    """

    redis_conn = redis.Redis(host="localhost", port=6379, db=0)

    # Read the pickle with the data from the previous usage.
    if os.path.exists("redisData.pkl"):
        with open("redisData.pkl", "rb") as f:
            redis_data = dill.load(f)

        # The pickle is a dictionary with key-value pairs taken
        # out of Redis, some of those are api handles (connection
        # objects from python libraries)
        for k, v in redis_data.items():
            redis_conn.set(k, v)

    # Load some example data for all users
    grandparent_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(grandparent_dir, "example_data")
    for file in os.listdir(data_dir):
        if file.endswith("csv"):
            name = file[:-4]

            df = pd.read_csv(os.path.join(data_dir, file))
            redis_conn.set(f"example_data_{name}",
                           dill.dumps(df))

            # Get a sample from this dataframe, infer types, and save them
            sample = df.sample(50, replace=True)
            types, subtypes = infer_types(sample, is_sample=True)

            save_schema(key=f"example_schema_{name}",
                        types=types, subtypes=subtypes,
                        head=sample.head(),
                        user_id="example",
                        schema_status="inferred",
                        redis_conn=redis_conn)

    return redis_conn

