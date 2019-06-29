from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import dash_table

from server import app
from utils import r, get_data, pretty_print_tweets, create_table
from apps.data.View import get_available_choices

from tableschema import Table
from itertools import chain


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

    df = df[df.columns[:10]]

    # This mumbo-jumbo is needed because tableschema incorrectly
    # infers numpy dtypes as "any/object" rather than the actual values
    try:
        # this will work if the data are numpy numeric dtypes
        list_data = df[:10].values.data.tolist()
    except NotImplementedError:
        # this is called probably only for "string" or "object"
        list_data = df[:10].values

    # Get current schema for the graph
    # TODO: Actually implement this, e.g.:
    #       `schema = r.get(f"{api_choice}_schema")`
    # The code converts the dataframe to a list of lists
    # because tableschema does not understand
    table = Table(list(list(row) for row in chain([df.columns],
                                                  list_data)))
    schema = table.infer()
    dtypes = [d["type"] for d in schema["fields"]]

    # Mapping of types (strings) from tableschema to dash_table.
    # See: https://frictionlessdata.io/specs/table-schema/
    # and https://dash.plot.ly/datatable/typing
    dash_type = {
        "string": "text",
        "number": "numeric",
        "integer": "numeric",
        "boolean": "text",
        "date": "datetime",
        "any": "object"
    }

    return [
        html.Br(),
        create_table(df, columns=[{"name": [col, dtype], "id": col,
                                   "type": dash_type[dtype]}
                                  for (col, dtype) in zip(df.columns, dtypes)]),
    ]