"""
This module takes care of the menu and choices provided when the \
"Analyze & Predict" high-level tab is selected.

Dash callbacks:
    - tab_subpages: Given the low-level tab choice, render the \
                    appropriate view.
    - render_sidemenu: Render the menu in the side-navbar.

Notes to others:
    You should probably not write code here, unless you are defining \
    a new level-2 tab. Here you can find functionality to define or \
    train ML / NN models. Implementations go to their own modules \
    down the package hierarchy, in `apps.analyze`.
"""

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from .server import app, redis_conn
from .single_model import single_model_options
from .model_builder import Model_Builder_Layout
from .pipelines import Pipeline_Options
from utils import interactive_menu, get_dataset_options

from flask_login import login_required


app.layout = html.Div(children=[

    *interactive_menu(output_elem_id="sidenav2_contents"),

    html.Div(children=[
        dcc.Tabs(id="level2_tabs", value="model_builder", children=[
            dcc.Tab(label='Model builder', value='model_builder',
                    id="model_builder"),
            dcc.Tab(label='Pipelines trainer', value='pipelines',
                    id="pipelines"),
            dcc.Tab(label='Single model', value='single_model',
                    id="single_model"),
        ]),

        html.Div(id="model-content"),
    ]),

])


@app.callback([Output('model-content', 'children'),
               Output("sidenav2_contents", "children")],
              [Input('level2_tabs', 'value')])
@login_required
def tab_subpages(tab):
    """
    Given the low-level tab choice, render the appropriate view.

    Args:
        tab (str): The tab the user is currently on.

    Returns:
        A list of lists of HTML-dash components, usually within a div.
    """

    # Check whether the user has uploaded data
    dataset_options = get_dataset_options(redis_conn)

    if tab == "model_builder":
        return Model_Builder_Layout()

    elif tab == "pipelines":
        return Pipeline_Options(dataset_options)

    elif tab == 'single_model':
        return single_model_options(dataset_options)

    else:
        return [html.H4("Click on a subtab...")], html.H4(tab)


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
