"""
    This module takes care of the menu and choices provided when the
    "Analyze & Predict" level-1 tab is selected.

    You should probably not write code here, UNLESS you are defining
    a new level-2 tab.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import mapping, r
from apps.analyze import Model_Builder_Layout, Regression_Options
from apps.analyze import Classification_Options, Clustering_Options
from apps.analyze import Econometrics_Options
from apps.data.View import get_available_choices

import pandas as pd
import base64
import datetime


## TODO: Port internal functionality to apps.analyze_tabs

layout = html.Div(children=[
    html.Div(children=[
        dcc.Tabs(id="analyze_tabs", value="regression", children=[
            dcc.Tab(label='Model builder', value='model_builder',
                    id="model_builder"),
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


## Subtabs
@app.callback(Output('model-content', 'children'),
              [Input('analyze_tabs', 'value')],
              [State("user_id", "children")])
def tab_subpages(tab, user_id):
    """
        This callback is called when a level two tab
        is selected in the analysis menu. Accordingly,
        it returns an interface to provide further
        specifications for the model.
    """

    options, results = get_available_choices(r, user_id)

    # Check whether the user has uploaded data
    if all(v is None for k,v in results.items()):
        return html.H4("No data currently uploaded")

    if tab == "model_builder":
        return Model_Builder_Layout

    elif tab == 'regression':
        return Regression_Options(options, results)

    elif tab == "classification":
        return Classification_Options(options, results)

    elif tab == "clustering":
        return Clustering_Options(options, results)

    elif tab == "econometrics":
        return Econometrics_Options(options, results)

    else:
        return [html.H4("Click on a subtab..."),]
