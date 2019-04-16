"""
    This module takes care of the menu and choices provided when the
    "Data view" level-1 tab is selected.

    You should probably not write code here, UNLESS you are defining
    a new level-2 tab.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from apps.data import Upload_Options, View_Options, API_Options


layout = html.Div(children=[
    html.Div(children=[
        dcc.Tabs(id="level2_tabs", value='upload_data', children=[
            dcc.Tab(label='Upload Data', value='upload_data',
                    id="upload_data"),
            dcc.Tab(label='Connect to API', value='api_data',
                    id="api_data"),
            dcc.Tab(label='View Data', value='view_data',
                    id="view_data"),
        ]),
    ]),
    html.Div(id="data-content"),
])


@app.callback(Output('data-content', 'children'),
              [Input('level2_tabs', 'value')],
              [State("user_id", "children")])
def tab_subpages(tab, user_id):
    """
        This is the second level of data tabs, that gets
        called when one of the first-level tabs is selected.
        Here you can either upload your data, connect to an
        API, or view already uploaded data.

        Input comes from current module, output comes from
        the modules in data_tabs (loaded in __init__)
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
