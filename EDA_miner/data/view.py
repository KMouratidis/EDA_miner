"""
This module provides views for the data (tables, lists of tweets, etc).

Global Variables:
    - View_Options: Generate the layout for inspecting available datasets.

Functions:
    - get_available_choices: Get datasets available to user.

Dash callbacks:
    - display_subdataset_choices: Show/hide input field for Quandl API.
    - render_table: Create a display for the chosen dataset.
    - display_reddit_posts: For the Reddit API, allow the user to \
                            specify a subreddit to get data from.

Note to others:
    You should probably not write code here, UNLESS you defined a \
    new connection to an API, or are doing refactoring.
"""

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from .server import app, redis_conn
from utils import create_table, get_dataset_options

import dill


def View_Options():
    """
    Generate the layout for inspecting available datasets.

    Returns:
        A Dash element or list of elements.
    """

    options = get_dataset_options(redis_conn)
    available_choices = html.Div(dcc.Dropdown(options=options,
                                              id="dataset_key"),
                                 className="horizontal_dropdowns")

    return [
        html.Br(),
        available_choices,

        dcc.Input(id="dataset_name", style={"display": "none"}),

        html.Div(id="table_view", children=[
            dash_table.DataTable(id='table'),
        ]),
    ]


@app.callback(Output("table_view", "children"),
              [Input("dataset_key", "value")])
def render_table(dataset_key):
    """
    Create a display for the chosen dataset.

    Args:
        dataset_key (str): Value from the dropdown. It is the Redis \
                           key for the dataset.

    Returns:
        list: A list of dash components.
    """

    if dataset_key is None:
        return [html.H4("Nothing selected.")]

    df = dill.loads(redis_conn.get(dataset_key))

    return [
        html.Br(),
        create_table(df),
    ]
