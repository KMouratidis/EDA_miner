
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


from utils import interactive_menu
from .server import app
from .upload import Upload_Options
from .view import View_Options
from .apis import API_Options
from .schemata import Schema_Options

from flask_login import login_required


app.layout = html.Div(children=[

    *interactive_menu(output_elem_id="sidenav2_contents"),

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


# TODO: Any sidemenus, if any, should be added here. If none, delete.
# TODO: This probably needs to become one with the next callback.
@app.callback(Output("sidenav2_contents", "children"),
              [Input('level2_tabs', 'value')])
def render_sidemenu(tab):
    """
    Render the menu in the side-navbar.

    Args:
        tab (str): The tab the user is currently on.

    Returns:
        A Dash element or list of elements.
    """

    return html.H4(tab)


@app.callback(Output('data-content', 'children'),
              [Input('level2_tabs', 'value')])
@login_required
def tab_subpages(tab):
    """
    Given the low-level tab choice, render the appropriate view.

    Args:
        tab (str): The tab the user is currently on.

    Returns:
        A list of HTML-dash components, usually within a div.
    """

    if tab == 'upload_data':
        # TODO: This might need change, depending on whether we specify
        #       different privileges for logged-in users.
        return Upload_Options

    elif tab == "view_data":
        return View_Options()

    elif tab == "api_data":
        # TODO: This might need change when the login is implemented
        return API_Options

    elif tab == "edit_schema":
        return Schema_Options()


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
