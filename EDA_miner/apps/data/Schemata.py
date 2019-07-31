from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import dash_table

import dash_bootstrap_components as dbc

from server import app
from utils import r, get_data, pretty_print_tweets, create_table
from apps.data.View import get_available_choices
from apps.data.data_utils.schema_heuristics import infer_types

import dill


# TODO: WHEN IMPLEMENTING THIS DON'T FORGET TO KEEP TRACK OF DATASET
#       DESCRIPTORS AS MENTIONED HERE:
#       https://frictionlessdata.io/specs/table-schema/


def Schema_Options(user_id):
    options, results = get_available_choices(r, user_id)

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


@app.callback([Output("schema_confirmation", "message"),
               Output("schema_confirmation", "displayed")],
              [Input("update_schema", "n_clicks")],
              [State("table_colnames", "children"),
               State("row_type", "children"),
               State("row_subtype", "children"),
               State("dataset_choice", "value"),
               State("user_id", "children")])
def update_schema(n_clicks, table_colnames, row_types, row_subtypes,
                  dataset_choice, user_id):
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
        user_id (str): Session/user id.

    Returns:
        list(str, bool): A message and a boolean for a browser alert.
    """


    types = {}
    for col_name, col in zip(table_colnames, row_types):
        dropdown = col["props"]["children"]
        dropdown_value = dropdown["props"]["value"]
        col_name = col_name["props"]["children"]

        types[col_name ] = dropdown_value

    subtypes = {}
    for col_name, col in zip(table_colnames, row_subtypes):
        dropdown = col["props"]["children"]
        dropdown_value = dropdown["props"]["value"]
        col_name = col_name["props"]["children"]

        subtypes[col_name] = dropdown_value

    r.set(f"{user_id}_{dataset_choice}_schema", dill.dumps({
        "types": types,
        "subtypes": subtypes
    }))

    return "Updated", True



@app.callback(Output("table_schema", "children"),
              [Input("dataset_choice", "value")],
              [State("user_id", "children")])
def show_schema(api_choice, user_id):


    if api_choice is None:
        return [html.H4("Nothing selected.")]

    else:
        df = get_data(api_choice, user_id)

    if df is None:
        return [html.H4("Nothing to display")]

    schema = r.get(f"{user_id}_{api_choice}_schema")
    if schema is None:
        sample = df.sample(n=50, replace=True).dropna()
        types, subtypes = infer_types(sample, is_sample=True)
        r.set(f"{user_id}_{api_choice}_schema", dill.dumps({
            "types": types,
            "subtypes": subtypes
        }))

    else:
        schema = dill.loads(schema)
        types, subtypes = schema["types"], schema["subtypes"]

    # Mapping of types (strings) from schema to dash_table.
    # See: https://dash.plot.ly/datatable/typing
    dash_type = {
        "float": "numeric",
        "integer": "numeric",
        "categorical": "text",
        "date": "datetime",
        "string": "text"
    }

    return [
        html.Br(),
        dcc.ConfirmDialog(id="schema_confirmation"),
        html.Button("Update schema", id="update_schema"),

        schema_table(df[:200], types, subtypes)
    ]