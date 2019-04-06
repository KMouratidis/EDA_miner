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
from utils import r, create_dropdown, get_data

import plotly.graph_objs as go
from apps.analyze.models.utils import baseline
import numpy as np


SideBar_KPIs = [
    ]


def KPI_Options(options, results):

    return html.Div(children=[

        html.Div(create_dropdown("Available datasets", options,
                                 multi=False, id="dataset_choice_kpi"),
                                 style={'width': '30%',
                                        'display': 'inline-block',
                                        'margin':"10px"}
        ),

        # TODO: use this for graph selection
        html.Div(create_dropdown("Choose graph type", options,
                                 multi=False, id="graph_choice_kpi"),
                 style={'width': '30%',
                        'display': 'inline-block',
                        'margin':"10px"}
        ),

        html.Div(id="variable_choices_kpi"),

        dcc.Graph(id="graph_kpi"),
    ])


@app.callback(Output("variable_choices_kpi", "children"),
              [Input("dataset_choice_kpi", "value")],
              [State("user_id", "children")])
def render_variable_choices_kpi(dataset_choice, user_id):

    data = get_data(dataset_choice, user_id)

    options = [{'label': "No dataset selected yet", 'value': "no_data"}]
    if data is not None:
        options=[{'label': col[:35], 'value': col} for col in data.columns]

    return [
        html.Div(create_dropdown("X variables", options,
                         multi=False, id="xvars_kpi"),
                         style={'width': '30%', 'display': 'inline-block',
                                'margin':"10px"}),
        html.Div(create_dropdown("Y variable", options,
                         multi=True, id="yvars_kpi"),
                         style={'width': '30%', 'display': 'inline-block',
                                'margin':"10px"}),
        html.Div(create_dropdown("Bar Chart variable", options,
                         multi=False, id="secondary_yvars_kpi"),
                         style={'width': '30%', 'display': 'inline-block',
                                'margin':"10px"}),
    ]


def hard_cast_to_float(x):
    try:
        ret = np.float32(x)
    except:
        ret = 0

    return ret


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

    if any(x is None for x in [xvars, yvars, secondary_yvars, df]):
        return {}

    # baseline graph
    traces = [
        go.Scatter(
            x=df[xvars],
            y=baseline(df[yvar].apply(hard_cast_to_float)),
            mode='lines',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': (0,100,255)}
            },
            name=f"Baseline for {' '.join(yvar.split()[:2])}",
        ) for yvar in yvars] + [
        # one scatter for each y variable
        go.Scatter(x=df[xvars],
                   y=df[yvar].apply(hard_cast_to_float),
                   mode='lines+markers',
                   marker={
                       'size': 8,
                       'line': {
                           'width': 0.5,
                           'color': 'rgb(210, 40, 180)'
                        },
                       'color': 'rgb(180, 35, 180)'
                   },
                   name=yvar
            ) for yvar in yvars] + [
        # Bar plot for the second variable
        go.Bar(
            x=df[xvars],
            y=df[secondary_yvars].apply(hard_cast_to_float),
        )
        ]

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': xvars},
            yaxis={'title': yvars[0]}, # yvars is a list (multi=True)
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
        )
    }
