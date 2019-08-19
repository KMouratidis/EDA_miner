"""
This module defines the interface for fitting simple models for the \
three main machine learning tasks (regression, classification, and \
clustering. It also reports fitting metrics and a graph.

Functions:
    - single_model_options: Generate the layout of the dashboard.

Dash callbacks:
    - render_choices: Create a menu for fitting options, depending of \
                      the problem type.
    - fit_model: Take user choices and, if all are present, fit the \
                 appropriate model.
    - render_report: Get the results (graph and text metrics) and show them.

Notes to others:
    Feel free to experiment as much as you like here, although you \
    probably want to write code elsewhere.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

from .server import app, redis_conn
from .models.graph_structures import ml_options, node_options
import layouts
from utils import create_dropdown, get_data_schema
from visualization.graphs.graphs2d import scatterplot

import plotly.graph_objs as go
import numpy as np
import pandas as pd
import dill

from sklearn.metrics import confusion_matrix


def single_model_options(options):
    """
    Generate the layout of the dashboard.

    Args:
        options (list(dict)): Available datasets as options for `dcc.Dropdown`.

    Returns:
        A Dash element or list of elements.
    """

    return html.Div([

        # The left side with the options
        html.Div(id="model_choices", children=[
            # Choose a dataset
            html.Div(create_dropdown("Available datasets", options,
                                     multi=False, id="dataset_choice")),

            # Choose problem learning type
            html.Div(create_dropdown("Choose problem learning type", options=[
                {'label': 'Regression', 'value': 'regression'},
                {'label': 'Classification', 'value': 'classification'},
                {'label': 'Clustering', 'value': 'clustering'},
            ], multi=False, id="problem_type")),

            html.Div(id="variable_choices"),
        ], className="col-sm-3"),

        # The right side with the results
        html.Div(id="training_results_div", children=[

            # Choose type of metric to display
            dcc.Tabs(id="results_tabs", value='metrics', children=[
                dcc.Tab(label='Metrics', value='metrics'),
                dcc.Tab(label='Visualizations', value='visualizations'),
            ]),

            # Hidden divs for the intermediate results
            html.Div(id="hidden_results_metrics",
                     style={"display": "none"}),
            html.Div(id="hidden_results_visualizations",
                     style={"display": "none"}),

            # The fitting results (target of the tab menu)
            html.Div(id="fitting_report")

        ], className="col-sm-9"),
    ], className="row")


@app.callback(Output("fitting_report", "children"),
              [Input("results_tabs", "value"),
               Input("hidden_results_metrics", "children"),
               Input("hidden_results_visualizations", "children")])
def render_report(selected_tab, results_metrics, results_visualizations):
    """
    Get the results (graph and text metrics) and show them. This is \
    done in two steps instead of one because dbc.Tabs does not size \
    the `dcc.Graph` correctly.

    Args:
        selected_tab (str): The type of report metrics to show.
        results_metrics (Dash elements): The elements showing text metrics.
        results_visualizations (Dash elements): The elements showing graphs.

    Returns:
        A Dash element or list of elements.
    """

    if results_metrics is None and results_visualizations is None:
        raise PreventUpdate()

    if selected_tab == "metrics":
        return results_metrics

    else:
        return dcc.Graph(id="training_results_viz",
                         figure=results_visualizations),


@app.callback(Output("variable_choices", "children"),
              [Input("problem_type", "value"),
               Input("dataset_choice", "value")])
def render_choices(problem_type, dataset_choice):
    """
    Create a menu for fitting options, depending of the problem type. It \
    returns dropdowns with algorithm choices.

    Args:
        problem_type (str): One of: regression, classification, clustering.
        dataset_choice (str): Name of the dataset.

    Returns:
        A Dash element or list of elements.
    """

    if problem_type is None or dataset_choice is None:
        raise PreventUpdate()

    # Load the schema for the dataset
    df_schema = get_data_schema(dataset_choice, redis_conn)["types"]

    # From the schema take the dataset's column names
    var_options = [
        {"label": col, "value": col}
        for col in df_schema.keys()
    ]

    disabled_y = False
    algo_options = None

    # Depending on the problem type, show the available algorithms
    if problem_type in ["regression", "classification", "clustering"]:
        disabled_y = False
        algo_options = [
            {'label': estimator["label"], 'value': estimator["node_type"]}
            for estimator in ml_options
            if (estimator["parent"] == "models" and
                estimator["problem"] == problem_type)
        ]

        if problem_type == "clustering":
            disabled_y = True

    return html.Div([
        html.Div(create_dropdown("Choose algorithm type",
                                 options=algo_options,
                                 multi=False, id="algo_choice")),

        html.Div(create_dropdown("Choose variable(s) X",
                                 options=var_options,
                                 multi=True, id="xvars")),

        html.Div(create_dropdown("Choose target variable Y",
                                 options=var_options,
                                 multi=False, id="yvars",
                                 disabled=disabled_y)),
    ])


@app.callback(
    [Output("hidden_results_metrics", "children"),
     Output("hidden_results_visualizations", "children")],
    [Input("xvars", "value"),
     Input("yvars", "value"),
     Input('algo_choice', "value")],
    [State("dataset_choice", "value"),
     State("problem_type", "value")])
def fit_model(xvars, yvars, algo_choice, dataset_choice, problem_type):
    """
    Take user choices and, if all are present, fit the appropriate model. \
    The results of fitting are given to hidden divs. When the user uses \
    the tab menu then the appropriate menu is rendered.

    Args:
        xvars (list(str)): predictor variables.
        yvars (str): target variable.
        algo_choice (str): The choice of algorithm type.
        dataset_choice (str): Name of the dataset.
        problem_type (str): The type of learning problem.

    Returns:
        list, dict: Dash element(s) with the results of model fitting,
                    and parameters for plotting a graph.
    """

    df = dill.loads(redis_conn.get(dataset_choice))

    # Make sure all variables have a value before fitting
    if any(x is None for x in [xvars, yvars, df, dataset_choice,
                               algo_choice]):
        raise PreventUpdate()

    # The inverse mapping of ml_options, use it to get the sklearn model
    model = node_options[algo_choice]["model_class"]()

    # TODO: This probably needs a better/cleaner implementation and/or
    #       might need to be used in other parts as well.
    y = pd.factorize(df[yvars])
    model.fit(df[xvars], y[0])

    predictions = model.predict(df[xvars])
    score = model.score(df[xvars], y[0])

    metrics = []
    if problem_type == "regression":
        metrics.append(html.H4(f"Mean Squared Error: {score:.3f}"))

    elif problem_type == "classification":
        metrics.append(html.H4(f"Accuracy: {100*score:.3f} %"))
        metrics.append(html.H4("Confusion matrix:"))

        classes = df[yvars].unique()

        confusion = confusion_matrix(y[0], predictions)
        metrics.append(html.Table([
            html.Thead([html.Th(cls) for cls in classes]),

            html.Tbody([
               html.Tr([html.Td(item) for item in row])
               for row in confusion
            ])
        ]))

    else:
        metrics.append("Not implemented")

    labels = model.predict(df[xvars])
    # TODO: Visualize the (in)correctly grouped points.
    # If we have >=2 variables, visualize the classification
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

        figure = {
            'data': [trace1],
            'layout': layouts.default_2d(xvars[0], yvars[0])
        }

    elif len(xvars) == 2:
        traces = scatterplot(df[xvars[0]], df[xvars[1]],
                             marker={'color': labels.astype(np.float)})

        figure = {
            'data': [traces],
            'layout': go.Layout(
                xaxis={'title': xvars[0]},
                yaxis={'title': yvars[0]},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }

    else:
        figure = {}

    return metrics, figure
