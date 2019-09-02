
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from .server import app
from .upload import Upload_Options
from .view import View_Options
from .apis import API_Options
from .schemata import Schema_Options
from utils import check_user_access

from flask_login import login_required


app.layout = html.Div(children=[

    # See below
    html.Div(id="dummy_redirect"),

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

        html.Div(id="data-content"),
    ]),


])


# Although we do not need (not yet at least) the menu here,
# The login manager will still return two elements since the
# other apps expect that. We handle it here with a dummy.
@app.callback([Output('data-content', 'children'),
               Output("dummy_redirect", "children")],
              [Input('level2_tabs', 'value')])
@login_required
@check_user_access("data")
def tab_subpages(tab):
    """
    Given the low-level tab choice, render the appropriate view and \
    side-navbar.

    Args:
        tab (str): The tab the user is currently on.

    Returns:
        A list of lists of HTML-dash components, usually within a div.
    """

    if tab == 'upload_data':
        return Upload_Options, html.Div(style={"display": "hidden"})

    elif tab == "view_data":
        return View_Options(), html.Div(style={"display": "hidden"})

    elif tab == "api_data":
        return API_Options, html.Div(style={"display": "hidden"})

    elif tab == "edit_schema":
        return Schema_Options(), html.Div(style={"display": "hidden"})


if __name__ == "__main__":
    # Normally you would run from here. Now it doesn't work for a few
    # reasons: 1) The "login_required" above has not been initialized
    # at the app level but at the project level, so either remove it
    # or use login_manager = LoginManager(app.server), 2) Upon
    # defining the app (see .server) we passed "requests_pathname_prefix"
    # which cause Dash to look at the wrong place for the static files,
    # so remove that too, and 3) Imports are defined as relative imports
    # so you need to care care of that too.
    app.run_server()
