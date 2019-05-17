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
from dash.exceptions import PreventUpdate

from server import app
from utils import r
from apps.data.data_utils import api_connectors
from apps.data.data_utils.api_layouts import logins_ui_mapping

import pickle
from inspect import getfullargspec


API_Options = html.Div(children=[
    html.H4("Connect to an API from the list:"),

    html.Div(children=[
        dcc.Tabs(id="api_choice", value='twitter', children=[
            dcc.Tab(label='Twitter', value='twitter',
                    id="twitter_api"),
            dcc.Tab(label='Google Sheets', value='gsheets',
                    id="gsheets_api"),
            dcc.Tab(label='Reddit', value='reddit',
                    id="reddit_api"),
            dcc.Tab(label='Quandl', value='quandl',
                    id="quandl_api"),
            dcc.Tab(label='Spotify', value='spotify',
                    id="spotify_api"),
        ]),
    ]),

    html.Div(id="api_login_form"),
    html.Div(id="api_user_interface"),
])


# Responsible for rendering the available login form
@app.callback(Output('api_login_form', 'children'),
              [Input('api_choice', 'value')],
              [State("user_id", "children")])
def render_api_login_form(api_choice, user_id):


    if r.get(f"{user_id}_{api_choice}_api") is not None:
        # Previously connected
        return logins_ui_mapping[api_choice][1]
    else:
        return logins_ui_mapping[api_choice][0]


# Create callbacks for every API login form, based on
# their connectors' function arguments
for api, func in api_connectors.connectors_mapping.items():
    @app.callback([Output(f'{api}_UI', 'children'),
                   Output(f'{api}_login_form', 'style')],
                  [Input(f'{api}_connect_button', 'n_clicks')],
                  [State("api_choice", "value"),
                   State("user_id", "children")] + [
                      State(f"{api}_{var}", "value")
                      for var in getfullargspec(func).args
                  ])
    def parse_credentials(n_clicks, api_choice, user_id, *func_params):

        success = api_connectors.api_connect(api_choice, user_id, *func_params)

        if success:
            # Success logging in
            return logins_ui_mapping[api_choice][1], {"display": "none"}

        else:
            raise PreventUpdate()


# Callback that handles what happens with the Twitter UI
@app.callback(Output("twitter_results", "children"),
              [Input("get_tweets_username", "n_clicks")],
              [State("twitter_account_name", "value"),
               State("user_id", "children")])
def get_users_tweets(n_clicks, acc_name, user_id):


    if n_clicks > 0:
        api = pickle.loads(r.get(f"{user_id}_twitter_api_handle"))

        # TODO: This is a cache so consider a better implementation.
        query = r.get(f"{user_id}_twitter_data_{acc_name}")
        if query is None:
            # TODO: Consider saving for future use / as a dataset.
            query = api.GetUserTimeline(screen_name=acc_name)

            # Expire the retrieved tweets cache in one hour
            r.set(f"{user_id}_twitter_data_{acc_name}",
                  pickle.dumps(query), ex=3600)
        else:
            query = pickle.loads(query)

        return [html.P(str(status.text)) for status in query]

    else:
        raise PreventUpdate()
