from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from .server import app, redis_conn
from .view import get_dataset_options
from utils import get_data_schema, save_schema

import dill
from flask_login import current_user


def Schema_Options():
    """
    Generate the layout of the dashboard.

    Returns:
        A list of Dash elements.
    """

    options = get_dataset_options(redis_conn)

    available_choices = html.Div(dcc.Dropdown(options=options,
                                              id="dataset_choice"),
                                 className="horizontal_dropdowns")

    return [
        available_choices,

        html.Div(id="table_schema", children=[
            dash_table.DataTable(id='table'),
        ]),
    ]


all_datatypes_options = [
    {"label": dtype, "value": dtype}
    for dtype in "string float integer categorical date".split()
]


# TODO: Pagination
def schema_table(df, types, subtypes):
    """
    Helper to create the table. Dash's DataTable doesn't allow for \
    dropdowns to only some rows so we create our own where the first \
    row is the head, the second rows are like head but have dropdowns \
    for picking types

    Args:
        df (`pd.DataFrame`): The dataset.
        types (dict): The types from the data schema.
        subtypes (dict): The subtypes from the data schema.

    Returns:
        A Dash element containing the table.
    """

    subtype_options = {
        "categorical": [
            {"label": dtype, "value": dtype}
            for dtype in "binary categorical".split()
        ],
        "integer": [{"label": "integer", "value": "integer"}],
        "date": [{"label": "date", "value": "date"}],
        "float": [
            {"label": dtype, "value": dtype}
            for dtype in "float longitude latitude".split()
        ],
        "string": [
            {"label": dtype, "value": dtype}
            for dtype in "email ipv4 ipv6 mac_address string".split()
        ],
    }

    return html.Div([
        html.Table([
            html.Thead([
                html.Th(col_name)
                for col_name in df.columns
            ], id="table_colnames"),

            html.Tbody([
                html.Tr([
                    html.Td(dcc.Dropdown(
                        options=all_datatypes_options,
                        value=types[col_name]))
                    for col_name in df.columns
                ], id="row_type"),
                html.Tr([
                    html.Td(dcc.Dropdown(
                        options=subtype_options[types[col_name]],
                        value=subtypes[col_name]))
                    for col_name in df.columns
                ], id="row_subtype"),
            ] + [
                html.Tr([
                    html.Td(item)
                    for item in row
                ])
                for (i, row) in df.iterrows()
            ])
        ])
    ])


@app.callback(Output("table_schema", "children"),
              [Input("dataset_choice", "value")])
def show_schema(dataset_choice):
    """
    Show the schema for the dataset and allow the user to modify it.

    Args:
        dataset_choice (str): Name of dataset.

    Returns:
        list: A list of dash components. The custom table.
    """

    if dataset_choice is None:
        return [html.H4("Nothing selected.")]

    else:
        df = dill.loads(redis_conn.get(dataset_choice))

    if df is None:
        return [html.H4("Nothing to display")]

    schema = get_data_schema(dataset_choice, redis_conn)
    if schema is None:
        raise Exception("No schama for file")
    else:
        types, subtypes = schema["types"], schema["subtypes"]

    return [
        html.Br(),
        dcc.ConfirmDialog(id="schema_confirmation"),
        html.Button("Update schema", id="update_schema"),

        schema_table(df[:100], types, subtypes)
    ]


@app.callback([Output("schema_confirmation", "message"),
               Output("schema_confirmation", "displayed")],
              [Input("update_schema", "n_clicks")],
              [State("table_colnames", "children"),
               State("row_type", "children"),
               State("row_subtype", "children"),
               State("dataset_choice", "value")])
def update_schema(n_clicks, table_colnames, row_types, row_subtypes,
                  dataset_choice):
    """
    Update the dataset schema. This function takes the html elements \
    from the table head (containing column names) and its first two \
    rows (containing dropdowns with the data types/subtypes), parses \
    them and stores them in redis.

    Args:
        n_clicks (int): Number of button clicks.
        table_colnames (dict): The head (`html.Thead`) of the table, \
                               as a Dash dict.
        row_types (dict): The first table row (`html.Tr`) containing \
                          the Dash dropdown dict with the data types.
        row_subtypes (dict): The first table row (`html.Tr`) containing \
                             the Dash dropdown dict with the data subtypes.
        dataset_choice (str): Name of dataset.

    Returns:
        list(str, bool): A message and a boolean for a browser alert.
    """

    old_schema = get_data_schema(dataset_choice, redis_conn)
    user_id = current_user.username

    types = {}
    for col_name, col in zip(table_colnames, row_types):
        dropdown = col["props"]["children"]
        dropdown_value = dropdown["props"]["value"]
        col_name = col_name["props"]["children"]

        types[col_name] = dropdown_value

    subtypes = {}
    for col_name, col in zip(table_colnames, row_subtypes):
        dropdown = col["props"]["children"]
        dropdown_value = dropdown["props"]["value"]
        col_name = col_name["props"]["children"]

        subtypes[col_name] = dropdown_value

    schema_key = dataset_choice.replace("_data_", "_schema_")
    save_schema(key=schema_key,
                types=types, subtypes=subtypes,
                head=old_schema["head"],
                redis_conn=redis_conn,
                user_id=user_id,
                schema_status="ground_truth")

    return "Updated", True

