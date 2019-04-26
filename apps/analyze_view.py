"""
This module takes care of the menu and choices provided when the
"Analyze & Predict" high-level tab is selected.

Dash callbacks:
    - tab_subpages: Given the low-level tab choice, render the \
                    appropriate view.

Notes to others:
    You should probably not write code here, unless you are defining
    a new level-2 tab. Here you can find functionality to define or
    train ML / NN models. Implementations go to their own modules
    down the package hierarchy, in `apps.analyze`.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import r
from apps.analyze import Model_Builder_Layout, Regression_Options
from apps.analyze import Classification_Options, Clustering_Options
from apps.analyze import Econometrics_Options, Pipeline_Options
from apps.data.View import get_available_choices



layout = html.Div(children=[
    html.Div(children=[
        dcc.Tabs(id="level2_tabs", value="model_builder", children=[
            dcc.Tab(label='Model builder', value='model_builder',
                    id="model_builder"),
            dcc.Tab(label='Pipelines trainer', value='pipelines',
                    id="pipelines"),
            dcc.Tab(label='Regression', value='regression',
                    id="regression"),
            dcc.Tab(label='Classification', value='classification',
                    id="classification"),
            dcc.Tab(label='Clustering', value='clustering',
                    id="clustering"),
            dcc.Tab(label='Econometrics', value='econometrics',
                    id="econometrics"),
        ]),
    ]),
    html.Div(id="model-content"),
])


# Subtabs
@app.callback(Output('model-content', 'children'),
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


    # Check whether the user has uploaded data
    # TODO: This check for data existence might be slow.
    #       It would be good to test/review and improve it.
    #       Same as in `exploration_view.py` !
    options, results = get_available_choices(r, user_id)
    if all(v is None for k, v in results.items()):
        return html.H4("No data currently uploaded")

    if tab == "model_builder":
        return Model_Builder_Layout

    elif tab == "pipelines":
        return Pipeline_Options(options, results, user_id)

    elif tab == 'regression':
        return Regression_Options(options, results)

    elif tab == "classification":
        return Classification_Options(options, results)

    elif tab == "clustering":
        return Clustering_Options(options, results)

    elif tab == "econometrics":
        return Econometrics_Options(options, results)

    else:
        return [html.H4("Click on a subtab...")]
