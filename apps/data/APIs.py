"""
This module defines the interface for connecting to APIs.
It renders the appropriate layout according to the tab chosen.

Dash callbacks:
    - api_connect: Render the appropriate view for the chosen API.

Notes to others:
    You should probably not write code here, UNLESS you first
    defined a new connection to an API (also update View module).
    Remember to include the elements necessary for the app to
    function correctly (see `debugger_layout`), or feel free to
    rework the whole thing if you can.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import r
from apps.data.data_utils import api_layouts, api_connectors

import pickle
import quandl


API_Options = html.Div(children=[
    html.H4("Connect to an API from the list:"),

    html.Div(children=[
        dcc.Tabs(id="api_choice", value='twitter_api', children=[
            dcc.Tab(label='Twitter', value='twitter_api',
                    id="twitter_api"),
            dcc.Tab(label='Google Sheets', value='gsheets_api',
                    id="gsheets_api"),
            dcc.Tab(label='Reddit', value='reddit_api',
                    id="reddit_api"),
            dcc.Tab(label='Quandl', value='quandl_api',
                    id="quandl_api"),
            dcc.Tab(label='Spotify', value='spotify_api',
                    id="spotify_api"),
        ]),
    ]),

    html.Div(id="api_login_form", children=[
        *api_layouts.debugger_layout,
    ]),
])


@app.callback(Output('api_login_form', 'children'),
              [Input('api_choice', 'value'),
               Input('connect_button', 'n_clicks')],
              [State("user_id", "children"),
               State("input1", "value"),
               State("input2", "value"),
               State("input3", "value"),
               State("input4", "value")])
def api_connect(api_choice, n_clicks, user_id,
                input1, input2, input3, input4):
    """
    Render the appropriate view for the chosen API.

    Args:
        api_choice (str): Value from the tabs.
        n_clicks (int): Number of times button was clicked.
        user_id (str): Session/user id.
        input1 (str): API-specific credential or value.
        input2 (str): API-specific credential or value.
        input3 (str): API-specific credential or value.
        input4 (str): API-specific credential or value.

    Returns:
        list: A list of dash components.

    Further details:
        Depending on the tab choice, provide the appropriate form.
        This callback is also responsible for adding the submit button
        if necessary. When a user selects a tab where they have already
        connected then an appropriate message is returned.
    """


    connected = r.get(f"{user_id}_{api_choice}") is not None

    if connected:
        return [
            html.H4("Connected previously"),
            *api_layouts.debugger_layout,
        ]

    if n_clicks is None:
        n_clicks = 0

    if api_choice == "twitter_api":
        if n_clicks >= 1:
            api_connectors.twitter_connect(input1, input2, input3,
                                           input4, user_id)
            return api_layouts.success_message("Twitter")

        else:
            return api_layouts.twitter_layout

    elif api_choice == "gsheets_api":
        if n_clicks >= 1:
            api_connectors.google_sheets_connect(input1, input2, user_id)
            return api_layouts.success_message("Google Sheets")

        else:
            return api_layouts.gsheets_layout

    elif api_choice == "reddit_api":

        if n_clicks >= 1:
            api_connectors.reddit_connect(input1, input2, user_id)
            return api_layouts.success_message("Reddit")

        else:
            return api_layouts.reddit_layout

    elif api_choice == "quandl_api":
        if n_clicks >= 1:
            # Does't exactly need an authentication function
            quandl.ApiConfig.api_key = input1

            r.set(f"{user_id}_{api_choice}", "true")
            r.set(f"{user_id}_{api_choice}_{input2}",
                  pickle.dumps(quandl.get(input2)))

            # TODO: This needs revisiting for allowing user to add
            # multiple datasets
            return api_layouts.success_message("Quandl")

        else:
            return api_layouts.quandl_layout

    elif api_choice == "spotify_api":
        if n_clicks >= 1:
            api_connectors.spotify_connect(input1, input2, user_id)
            return api_layouts.success_message("Spotify")

        else:
            return api_layouts.spotify_layout

    else:
        return [
            html.H4(f"{api_choice} not yet implemented"),
            html.H4("Debug element, please ignore"),
            *api_layouts.debugger_layout,
        ]
