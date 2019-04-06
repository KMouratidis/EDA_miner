"""
    This module defines the interface for connecting to APIs.
    It renders the appropriate layout according to the tab chosen.

    You should probably not write code here, UNLESS you first
    defined a new connection to an API (also update View module).
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import r, pretty_print_tweets
from apps.data import View_Options
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
        *api_layouts.debuger_layout,
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
        Depending on the tab choice, provide the appropriate form.
        This callback is also responsible for adding the submit button
        if necessary.
    """

    connected = r.get(f"{user_id}_{api_choice}") is not None

    if connected:
        return [
            html.H4("Connected previously"),
            *api_layouts.debuger_layout,
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
            return api_layout.success_message("Spotify")

        else:
            return api_layouts.spotify_layout

    else:
        return [
            html.H4(f"{api_choice} not yet implemented"),
            html.H4("Debug element, please ignore"),
            *api_layouts.debuger_layout,
        ]
