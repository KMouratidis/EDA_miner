"""
This module defines the interface for connecting to APIs. \
It renders the appropriate layout according to the tab chosen.

Global Variables:
    - API_Options: Generate the layout for connecting to APIs. \
                   This is automatically generated for the APIs \
                   defined in `api_connectors.connectors_mapping`.

Dash callbacks:
    - render_api_login_form: Render the appropriate login form.
    - parse_credentials (multiple): Create callbacks for every API \
                                    login form, based on their \
                                    connectors' function arguments.
    - get_data_from_api (multiple): Create callbacks for every API \
                                    fetch_data function.

Notes to others:
    You probably do not want to write ANY code here. If you want to \
    define a new API connection do it in `api_layouts` conforming to \
    the abstract base class interface and it will be automatically \
    added here.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

from .server import app, redis_conn
from .data_utils.api_connectors import api_connect, connectors_mapping

import dill
from inspect import getfullargspec, signature
from flask_login import current_user


API_Options = html.Div(children=[
    html.H4("Connect to an API from the list:"),

    html.Div(children=[
        dcc.Tabs(id="api_choice", value='twitter', children=[
            dcc.Tab(label=selected_api_cls.label,
                    value=selected_api_cls.api_name,
                    id=f"{selected_api_cls.api_name}_api")
            for api, selected_api_cls in connectors_mapping.items()
        ]),
    ]),

    html.Div(id="api_login_form"),
    html.Div(id="api_user_interface"),
])


# Responsible for
@app.callback(Output('api_login_form', 'children'),
              [Input('api_choice', 'value')])
def render_api_login_form(api_choice):
    """
    Render the appropriate login form. It takes the choice of API and \
    searches the mappings for the layout. A different layout is returned \
    accoring to login status.

    Args:
        api_choice (str): One of the supported APIs.

    Returns:
        A Dash element or list of elements.
    """

    user_id = current_user.username

    connection = redis_conn.get(f"{user_id}_connection_{api_choice}")
    if connection is not None:
        connection = dill.loads(connection)
    else:
        # Default connection (login state)
        connection = connectors_mapping[api_choice]()

    return connection.render_layout()


# NOTE: To make these work, they need to get the API choice from the state,
#       not the loop, since the f-strings are interpreted when the functions
#       run, not when they are defined.
for api, selected_api_cls in connectors_mapping.items():
    @app.callback([Output(f'{api}_UI', 'children'),
                   Output(f'{api}_login_form', 'style')],
                  [Input(f'{api}_connect_button', 'n_clicks')],
                  [State("api_choice", "value")] + [
                      State(f"{api}_{var}", "value")
                      for var in getfullargspec(selected_api_cls.connect).args[1:]
                  ])
    def parse_credentials(n_clicks, api_choice, *func_params):
        """
        Create callbacks for every API login form, based on their \
        connectors' function arguments. This reads the various connect \
        functions and gets their arguments. **Note that the first argument \
        is `self` so we need the rest of the arguments.

        Args:
            n_clicks (int): Number of button clicks.
            api_choice (str): One of the supported APIs.
            *func_params (list): Depending on the selected api and its \
                                 connector function, the list of arguments \
                                 it needs to receive, in order.

        Returns:
            A Dash element or list of elements.
        """

        if n_clicks < 1:
            raise PreventUpdate()

        connection = api_connect(api_choice, *func_params)
        if connection.state == "authenticated":
            # Success logging in
            return connection.render_layout(), {"display": "none"}

        else:
            raise PreventUpdate()


    # Get the arguments for the fetch_data functions. getfullargspec
    # doesn't work because those functions have a cache.memoize decorator
    fetch_data_args = list(signature(selected_api_cls.fetch_data).parameters.keys())

    @app.callback(Output(f'{api}_results', 'children'),
                  [Input(f'get_{api}', 'n_clicks')],
                  [State("api_choice", "value")] + [
                      State(f"{api}_{var}", "value")
                      for var in fetch_data_args[1:]
                  ])
    def get_data_from_api(n_clicks, api_choice, *func_params):
        """
        Create callbacks for every API success form, based on their \
        connectors' function arguments. This reads the various fetch_data \
        functions and gets their arguments. **Note that the first argument \
        is `self` so we need the rest of the arguments.

        Args:
            n_clicks (int): Number of button clicks.
            api_choice (str): One of the supported APIs.
            *func_params (list): Depending on the selected api and its \
                                 fetch_data function, the list of \
                                 arguments it needs to receive, in order.

        Returns:
            A Dash element or list of elements.
        """

        user_id = current_user.username

        if any(x is None for x in func_params):
            return [html.H4("Missing input choices.")]

        if n_clicks > 0:
            # Get the connection. Redis key schema reminder:
            # {user_id}_{data|connection|schema|has_connected}_{source}_{name}
            connection = dill.loads(redis_conn.get(f"{user_id}_connection"
                                                   f"_{api_choice}"))
            # Fetch topics from the subreddit
            sample = connection.fetch_data(*func_params)
            # Display the first few rows
            return connection.pretty_print(sample)

        else:
            raise PreventUpdate()
