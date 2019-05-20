"""
This module provides utilities, functions, and other code that is \
meant to be used across the app. This may undergo changes soon.

Functions:
    - cleanup: Clean up after the Dash app exits.
    - create_dropdown: Create a dropdown with a title.
    - create_table: Creates a `dash_table.DataTable` given a `pd.DataFrame`.
    - encode_image: Read and base64-encode an image for the dash app.
    - get_data: Get a `pandas.DataFrame` with the specified data.
    - hard_cast_to_float: Convert to float or return 0.
    - parse_contents: Decode uploaded files and store them in Redis.
    - pretty_print_tweets: Create H5 elements from the user's Twitter \
                           timeline.
    - redis_startup: Connect to a Redis server & handle startup.

Global variables:
    - r: A Redis connection that is used throughout the app.
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

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBClassifier
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler

import pandas as pd
import feather
import numpy as np
import base64
import json
import io
import redis
import pickle
import os
import tempfile


# TODO: this needs to be replaced by the one in Model_Builder
mapping = {
    "logr": LogisticRegression,
    "linr": LinearRegression,
    "xgb": XGBClassifier,
    "dtr": DecisionTreeRegressor,
    "svr": SVR,
    "kmc": KMeans,
    "dbscan": DBSCAN,
    "stdsc": StandardScaler,
}


# TODO: Implement user_id correctly:
# create a Redis entry with all `user_id`s that
# joined the session and cleanup for each of them
# TODO: Persist data from logged in users
def cleanup(redis_conn):
    """
    Clean up after the Dash app exits.

    Args:
        redis_conn: `redis.Redis` object.

    Further details:
        Flush every key stored in the Redis database. If there \
        are users that have logged in and uploaded data, store \
        those on disk. Also remove any static files generated \
        while the server was running.
    """

    print("Cleaning up...")
    redis_conn.flushdb()

    # Remove user images
    static_path = os.path.dirname(__file__) + "/static/images"
    for img in os.listdir(static_path):
        if img.startswith("python_generated_ssid"):
            os.remove(f"{static_path}/{img}")


def create_dropdown(name, options, **kwargs):
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

    return [
        html.H5(name+":"),
        dcc.Dropdown(
            options=options,
            **kwargs
        )]


def create_table(df, table_id="table"):
    """
    Creates a `dash_table.DataTable` given a `pandas.DataFrame`.

    Args:
        df (`pandas.DataFrame`): the data.
        table_id (str, optional): id of the table element for usage \
                                  with dash callbacks.

    Returns:
        A `dash_table.DataTable` with pagination.
    """

    return dash_table.DataTable(
        id=table_id,
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        style_table={
            'maxHeight': '400',
            'overflowY': 'scroll'
        },
        sorting=True,
        editable=True,
        pagination_mode='fe',
        pagination_settings={
            "displayed_pages": 1,
            "current_page": 0,
            "page_size": 10,
        },
        navigation="page",
        # n_fixed_rows=1,
        style_cell={
            'width': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
            'paddingLeft': '15px',
            # 'paddingRight': '15px',
        },
        style_cell_conditional=[
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
        },
    )


def encode_image(image_path):
    """
    Read and base64-encode an image for the dash app.

    Args:
        image_path (str): absolute path or relative to the \
                          top-level directory.

    Returns:
        A str to be used for the src attribute of an img element.
    """

    return 'data:image/png;base64,{}'.format(base64.b64encode(
        open(image_path, 'rb').read()).decode())


def get_data(api_choice, user_id):
    """
    Get a `pandas.DataFrame` with the specified data.

    Args:
        api_choice (str): the key used by the Redis server \
                          to store the data.
        user_id (str): the user for whom to fetch data.
    """

    if api_choice is None:
        df = None

    elif api_choice == "gsheets_api":
        df = pickle.loads(r.get(f"{user_id}_{api_choice}_data"))

    # uploaded data
    elif api_choice.startswith("user_data"):
        df = pd.read_msgpack(r.get(f"{user_id}_{api_choice}"))

    elif api_choice.startswith("quandl_api"):
        df = pickle.loads(r.get(f"{user_id}_{api_choice}"))

    else:
        df = None

    return df


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
    except:
        ret = 0

    return ret


# TODO: this function needs to be reviewed because
#       it doesn't work correctly on error (i.e. returns a Div).
def parse_contents(contents, filename, date, user_id):
    """
    Decode uploaded files and store them in Redis.

    Args:
        contents (str): the content of the file to be decoded.
        filename (str): name of uploaded file.
        date (str): (modification?) date of the file.
        user_id (str): the user for whom to fetch data.

    Further details:
        After decoding the uploaded file, handle any remaining \
        operations here. This was stolen from the dash docs. Currently \
        it only supports csv, xls(x), json, and feather file types.
    """

    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'json' in filename:
            # Assume that the user uploaded an json file
            try:
                df = pd.DataFrame.from_dict(json.loads(decoded.decode('utf-8')))
            except ValueError:
                # JSON file is probably only one row, so convert it to list
                df = pd.DataFrame.from_dict([json.loads(decoded.decode('utf-8'))])
        elif "feather" in filename:
            # Assume that the user uploaded a feather file
            # Since this only reads from a file, we careate
            # a temporary named file
            with tempfile.NamedTemporaryFile() as tmp:
                tmp.write(decoded)
                # Pandas read_feather doesn't seem to work
                df = feather.read_dataframe(tmp.name)

        else:
            return html.Div(['Format not yet supported.'])

    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])

    name = os.path.splitext(filename)[0]
    # Store to redis for caching
    r.set(f"{user_id}_user_data_{name}", df.to_msgpack(compress='zlib'))

    return html.Div([
        "Data uploaded successfully."
    ])


def pretty_print_tweets(api, n_tweets):
    """
    Create H5 elements from the user's Twitter timeline.

    Args:
        api (`twitter.Api`): a connection to Twitter \
                             with verified credentials.
        n_tweets (int): the number of tweets to display.
    """

    return [
        html.H5(str(tweet.text))
        for tweet in api.GetUserTimeline()[:n_tweets]
    ]


def redis_startup():
    """
    Connect to a Redis server & handle startup.

    Returns:
        `redis.Redis`: a connection to a Redis server.

    Further details:
        Connects to a Redis server on its default port (6379) and \
        is also responsible for any other startup operations needed.
    """

    redis_conn = redis.Redis(host="localhost", port=6379, db=0)

    return redis_conn


r = redis_startup()
