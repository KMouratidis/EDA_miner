"""
This module takes care of the menu and choices provided when the \
"Data view" high-level tab is selected.

Dash callbacks:
    - tab_subpages: Given the low-level tab choice, render the \
                    appropriate view.

Notes to others:
    You should probably not write code here, unless you are defining \
    a new level-2 tab. Here you can find find functionality to either \
    upload your data, connect to an API, or view/edit already uploaded \
    data. Implementations go to their own modules down the package \
    hierarchy, in `apps.data`.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from apps.data import Upload_Options, View_Options, API_Options, Schema_Options



layout = html.Div(children=[
    html.Div(children=[
        dcc.Tabs(id="level2_tabs", value='upload_data', children=[
            dcc.Tab(label='Upload Data', value='upload_data',
                    id="upload_data"),
            dcc.Tab(label='Connect to API', value='api_data',
                    id="api_data"),
            dcc.Tab(label='View Data', value='view_data',
                    id="view_data"),
            dcc.Tab(label="Edit data schema", value="edit_schema",
                    id="edit_schema")
        ]),
    ]),
    html.Div(id="data-content"),
])


@app.callback(Output('data-content', 'children'),
              [Input('level2_tabs', 'value')],
              [State("user_id", "children")])
def tab_subpages(tab, user_id):
    """
    Given the low-level tab choice, render the appropriate view.

    Args:
        tab (str): the low-level tab.
        user_id (str): the user/session uid.

    Returns:
        A list of HTML-dash components, usually within a div.
    """


    if tab == 'upload_data':
        # TODO: This might need change, depending on whether we specify
        #       different privileges for logged-in users.
        return Upload_Options

    elif tab == "view_data":
        return View_Options(user_id)

    elif tab == "api_data":
        # TODO: This might need change when the login is implemented
        return API_Options

    elif tab == "edit_schema":
        return Schema_Options(user_id)
