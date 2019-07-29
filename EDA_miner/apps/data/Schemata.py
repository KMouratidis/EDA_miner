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
        create_table(df, columns=[{"name": [col, "Data type:" + types[col], "Sub-type:" + subtypes[col]], "id": col,
                                   "type": dash_type[types[col]]}
                                  for col in df.columns]),
    ]