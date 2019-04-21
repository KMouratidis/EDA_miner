"""
    To be implemented.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
import layouts
from utils import r, create_dropdown, mapping, get_data
from apps.exploration.graphs.graphs2d import scatterplot

import plotly.graph_objs as go
import numpy as np
import pandas as pd

def Classification_Options(options, results):

    return html.Div(children=[
        # Choose a dataset
        html.Div(create_dropdown("Available datasets", options,
                                 multi=False, id="dataset_choice_classification"),
                 className="horizontal_dropdown"),

        # Choose an algorithm
        html.Div(create_dropdown("Choose algorithm type", options=[
            {'label': 'Logistic Regression', 'value': 'logr'},
            {'label': 'XGBoost', 'value': 'xgb'},
        ], multi=False, id="algo_choice_classification"),
                 className="horizontal_dropdown"),

        ## Two empty divs to be filled by callbacks
        # Available choices for fitting
        html.Div(id="variable_choices_classification"),

        # The results
        html.Div(id="training_results_classification"),

        dcc.Graph(id="classification_results")
    ])


@app.callback(Output("variable_choices_classification", "children"),
              [Input("dataset_choice_classification", "value"),
               Input("algo_choice_classification", "value")],
              [State("user_id", "children")])
def render_variable_choices_classification(dataset_choice,
                                           algo_choice_classification, user_id):
    """
        This callback is used in order to create a menu of dcc components
        for the user to choose for altering across datasets.
    """

    df = get_data(dataset_choice, user_id)

    # Make sure all variables have a value before returning choices
    if any(x is None for x in [df, dataset_choice, algo_choice_classification]):
        return [html.H4("Select dataset and algorithm first.")]

    options = [{'label': col[:35], 'value': col} for col in df.columns]

    layout = [
        html.Div(create_dropdown("X variable(s)", options,
                                 multi=True, id="xvars_classification"),
                 className="horizontal_dropdown"),
        html.Div(create_dropdown("Y variable", options,
                                 multi=False, id="yvars_classification"),
                 className="horizontal_dropdown"),
    ]

    return layout


@app.callback(
    [Output("training_results_classification", "children"),
     Output("classification_results", "figure")],
    [Input("xvars_classification", "value"),
     Input("yvars_classification", "value")],
    [State('algo_choice_classification', "value"),
     State("user_id", "children"),
     State("dataset_choice_classification", "value")])
def fit_classification_model(xvars, yvars, algo_choice_classification,
                  user_id, dataset_choice):
    """
        This callback takes all available user choices and, if all
        are present, it fits the appropriate model.
    """

    df = get_data(dataset_choice, user_id)

    ## Make sure all variables have a value before fitting
    if any(x is None for x in [xvars, yvars, df, dataset_choice,
                               algo_choice_classification]):
        return [[html.H4("Select dataset and algorithm first.")], {}]

    # We have the dictionary that maps keys to models so use that
    model = mapping[algo_choice_classification]()
    y = pd.factorize(df[yvars])
    model.fit(df[xvars], y[0])

    labels = model.predict(df[xvars])

    layout = [
        html.H4(f"Classification model scored: {model.score(df[xvars], y[0])}")
    ]

    if len(xvars) >= 3:

        trace1 = go.Scatter3d(x=df[xvars[0]],
                              y=df[xvars[1]],
                              z=df[xvars[2]],
                              showlegend=False,
                              mode='markers',
                              marker={
                                  'color': labels.astype(np.float),
                                  'line': dict(color='black', width=1)
                              })

        layout += [{
            'data': [trace1],
            'layout': layouts.default_2d(xvars[0], yvars[0])
        }]

    elif len(xvars) == 2:
        traces = scatterplot(df[xvars[0]], df[xvars[1]],
                             marker={'color': labels.astype(np.float)})

        layout += [{
            'data': traces,
            'layout': layouts.default_2d(xvars[0], yvars[0])
        }]

    else:
        layout += [{}]

    return layout
