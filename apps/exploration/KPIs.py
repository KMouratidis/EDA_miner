"""
    This module is about building and viewing KPIs.
    The user should be able to view more advanced graphs
    and also create their own indicators.

    You can write code in this module, but keep in
    mind that it may be moved later on to lower-level
    modules.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
import layouts
import styles
from utils import r, create_dropdown, get_data
from apps.exploration.graphs import graphs2d, kpis

import plotly.graph_objs as go

import numpy as np


SideBar_KPIs = [
    ]


def KPI_Options(options, results):

    return html.Div(children=[

        html.Div(create_dropdown("Available datasets", options,
                                 multi=False, id="dataset_choice_kpi"),
                                 style=styles.dropdown()),

        # TODO: use this for graph selection
        html.Div(create_dropdown("Choose graph type", options,
                                 multi=False, id="graph_choice_kpi",
                                 disabled=True),
                 style=styles.dropdown()),

        html.Div(id="variable_choices_kpi", children=[
            html.Div(create_dropdown("X variables", options=[],
                             multi=False, id="xvars_kpi"),
                             style=styles.dropdown()),
            html.Div(create_dropdown("Y variable", options=[],
                             multi=True, id="yvars_kpi"),
                             style=styles.dropdown()),
            html.Div(create_dropdown("Bar Chart variable", options=[],
                             multi=False, id="secondary_yvars_kpi"),
                             style=styles.dropdown()),
        ]),

        dcc.Graph(id="graph_kpi"),
    ])


@app.callback([Output("xvars_kpi", "options"),
               Output("yvars_kpi", "options"),
               Output("secondary_yvars_kpi", "options"),],
              [Input("dataset_choice_kpi", "value")],
              [State("user_id", "children")])
def render_variable_choices_kpi(dataset_choice, user_id):

    df = get_data(dataset_choice, user_id)

    # Make sure all variables have a value before returning choices
    if any(x is None for x in [df, dataset_choice]):
        return [[], [], []]

    options=[{'label': col[:35], 'value': col} for col in df.columns]

    return [options, options, options]


@app.callback(
    Output("graph_kpi", "figure"),
    [Input("xvars_kpi", "value"),
     Input("yvars_kpi", "value"),
     Input("secondary_yvars_kpi", "value")],
    [State("user_id", "children"),
     State('dataset_choice_kpi', 'value')])
def plot_graph_kpi(xvars, yvars, secondary_yvars,
                   user_id, dataset_choice):

    df = get_data(dataset_choice, user_id)

    if any(x is None for x in [xvars, yvars, secondary_yvars,
                               df, dataset_choice]):
        return {}

    # baseline graph
    traces = kpis.baseline_graph(df, xvars, yvars, secondary_yvars)


    return {
        'data': traces,
        'layout': layouts.default_2d(xvars, yvars[0])
    }
