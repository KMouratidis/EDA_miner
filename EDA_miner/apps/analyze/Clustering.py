"""
    TBW...
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.exceptions import PreventUpdate

from server import app
import layouts
from utils import create_dropdown, mapping, get_data
from apps.exploration.graphs.graphs2d import scatterplot

import plotly.graph_objs as go
import numpy as np


def Clustering_Options(options, results):

    return html.Div(children=[
        # Choose a dataset
        html.Div(create_dropdown("Available datasets", options,
                                 multi=False, id="dataset_choice_clustering"),
                 className="horizontal_dropdowns"),

        # Choose an algorithm
        html.Div(create_dropdown("Choose algorithm type", options=[
            {'label': 'DBSCAN', 'value': 'dbscan'},
            {'label': 'K-Means Clustering', 'value': 'kmc'},
        ], multi=False, id="algo_choice_clustering"),
                 className="horizontal_dropdowns"),

        ## Two empty divs to be filled by callbacks
        # Available choices for fitting
        html.Div(id="variable_choices_clustering"),

        #Available number of clusters
        html.P("Number of clusters:"),
        daq.NumericInput(
            id='clusters_input',
            min=0,
            value=3,
            max=10
        ),
        # The results
        html.Div(id="training_results_clustering"),

        # The graph
        dcc.Graph(id="clustering_results"),
    ])


@app.callback(Output("variable_choices_clustering", "children"),
              [Input("dataset_choice_clustering", "value"),
               Input("algo_choice_clustering", "value")],
              [State("user_id", "children")])
def render_variable_choices_clustering(dataset_choice, algo_choice_clustering,
                                       user_id):
    """
    Create a menu of dcc components to select dataset, variables,
    and training options.

    Args:
        dataset_choice (str): Name of dataset.
        algo_choice_clustering (str): The choice of algorithm type.
        user_id (str): Session/user id.

    Returns:
        list: Dash elements.
    """


    df = get_data(dataset_choice, user_id)

    # Make sure all variables have a value before returning choices
    if any(x is None for x in [df, dataset_choice, algo_choice_clustering]):
        return [html.H4("Select dataset and algorithm first.")]

    # Truncate labels so they don't fill the whole dropdown
    options = [{'label': col[:35], 'value': col} for col in df.columns]

    layout = [
        html.Div(create_dropdown("X variable(s)", options,
                                 multi=True, id="xvars_clustering"),
                 className="horizontal_dropdowns"),
        html.Div(create_dropdown("Target not applicable", options,
                                 multi=False, id="yvars_clustering"),
                 className="horizontal_dropdowns"),
    ]

    return layout


@app.callback(
    [Output("training_results_clustering", "children"),
     Output("clustering_results", "figure")],
    [Input("xvars_clustering", "value"),
     Input("yvars_clustering", "value"),
     Input("clusters_input", "value")],
    [State('algo_choice_clustering', "value"),
     State("user_id", "children"),
     State("dataset_choice_clustering", "value")])
def fit_clustering_model(xvars, yvars, n_clusters, algo_choice_clustering,
                         user_id, dataset_choice):
    """
    Take user choices and, if all are present, fit the appropriate model.

    Args:
        xvars (list(str)): predictor variables.
        yvars (str): target variable; not needed.
        algo_choice_clustering (str): The choice of algorithm type.
        user_id: Session/user id.
        dataset_choice: Name of dataset.

    Returns:
        list, dict: Dash element(s) with the results of model fitting,
                    and parameters for plotting a graph.
    """


    df = get_data(dataset_choice, user_id)

    ## Make sure all variables have a value before fitting
    if any(x is None for x in [xvars, df, dataset_choice,
                               algo_choice_clustering]):
        raise PreventUpdate()

    # TODO: Make this interface cleaner
    # We have the dictionary that maps keys to models so use that
    if algo_choice_clustering == "kmc":
        model = mapping[algo_choice_clustering](n_clusters=n_clusters)
    else:
        model = mapping[algo_choice_clustering]()

    model.fit(df[xvars])

    # TODO: Find a meaningful way (metric) to notify the user of model score.
    layout = [[html.H4(f"Clustering model scored: {model.score(df[xvars])}")]]

    labels = model.labels_
    # TODO: If Y is given, visualize the (in)correctly grouped points.
    # If we have >=2 variables, visualize the clusters
    if len(xvars) >= 3:

        trace1 = go.Scatter3d(x=df[xvars[0]],
                              y=df[xvars[1]],
                              z=df[xvars[2]],
                              showlegend=False,
                              mode='markers',
                              marker=dict(
                                  color=labels.astype(np.float),
                                  line={'color': 'black', 'width': 1}
                              ))

        layout += [{
            'data': [trace1],
            'layout': layouts.default_2d(xvars[0], xvars[1])
        }]

    elif len(xvars) == 2:
        trace = scatterplot(df[xvars[0]], df[xvars[1]],
                            marker={'color': labels.astype(np.float)})

        layout += [{
            'data': [trace],
            'layout': layouts.default_2d(xvars[0], xvars[1])
        }]

    else:
        layout += [{}]

    return layout
