from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import dash_table

from server import app
from utils import r, get_data, pretty_print_tweets, create_table
from apps.data.View import get_available_choices
from apps.data.data_utils.schema_heuristics import infer_types

from itertools import chain


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
            ]),

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
              [Input("dataset_choice", "value")],
              [State("user_id", "children")])
def show_schema(api_choice, user_id):


    if api_choice is None:
        return [html.H4("Nothing selected.")]

    else:
        df = get_data(api_choice, user_id)

    if df is None:
        return [html.H4("Nothing to display")]

    sample = df.sample(n=50, replace=True).dropna()

    # Get current schema for the graph if it exists
    # TODO: Actually implement this, e.g.:
    #       `schema = r.get(f"{api_choice}_schema")`

    types, subtypes = infer_types(df, is_sample=True)

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

        schema_table(df[:200], types, subtypes)
    ]