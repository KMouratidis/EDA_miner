"""
This module defines the interface for fitting (pre)defined pipelines.

Functions:
    - Pipeline_Options: Generate the layout of the dashboard.

Dash callbacks:
    - render_variable_choices_pipeline: Create a menu of dcc components \
                                        for the user to choose fitting \
                                        options.
    - fit_pipeline_model: Fits any pipelines defined.

Notes to others:
    You should probably not write code here, UNLESS reworking the interface.
"""


from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

from .server import app, redis_conn
from utils import create_dropdown, get_data_schema
from .models import pipeline_classes
from visualization.graphs.graphs2d import scatterplot
import layouts

import pandas as pd
import numpy as np
import dill
from flask_login import current_user
from sklearn.metrics import confusion_matrix
import plotly.graph_objs as go


def Pipeline_Options(options):
    """
    Generate the layout of the dashboard.

    Args:
        options (list(dict)): Available datasets as options for `dcc.Dropdown`.

    Returns:
        A Dash element or list of elements.
    """

    user_id = current_user.username

    available_pipelines = {k.decode(): redis_conn.get(k)
                           for k in redis_conn.keys(f'{user_id}_pipeline_*')}

    return html.Div([

        # The left side with the options
        html.Div(id="pipeline_choices", children=[

            # Choose a dataset
            html.Div(create_dropdown("Available pipelines", options=[
                {'label': f'Pipeline --> {pipe_name}', 'value': pipe_name}
                for pipe_name in available_pipelines
            ], multi=False, id="pipeline_choice")),

            html.Div(id="variable_choices_pipeline")
            ,
        ], className="col-sm-3"),

        # The right side with the results
        html.Div(id="training_results_div", children=[

            # Choose type of metric to display
            dcc.Tabs(id="results_tabs_pipeline", value='metrics', children=[
                dcc.Tab(label='Metrics', value='metrics'),
                dcc.Tab(label='Visualizations', value='visualizations'),
            ]),

            # Hidden divs for the intermediate results
            html.Div(id="hidden_results_metrics_pipeline",
                     style={"display": "none"}),
            html.Div(id="hidden_results_visualizations_pipeline",
                     style={"display": "none"}),

            # The fitting results (target of the tab menu)
            html.Div(id="fitting_report_pipeline")

        ], className="col-sm-9"),
    ], className="row")


# TODO: This is exactly the same as in single_model so you might
#       want to move it to app.py (?)
@app.callback(Output("fitting_report_pipeline", "children"),
              [Input("results_tabs_pipeline", "value"),
               Input("hidden_results_metrics_pipeline", "children"),
               Input("hidden_results_visualizations_pipeline", "children")])
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
        return dcc.Graph(id="training_results_viz_pipeline",
                         figure=results_visualizations),


@app.callback(Output("variable_choices_pipeline", "children"),
              [Input("pipeline_choice", "value")])
def render_variable_choices_pipeline(pipeline_choice):
    """
    Create a menu of dcc components to select pipeline and variables.

    Args:
        algo_choice_pipeline (str): Choice among (pre)defined pipelines.

    Returns:
        list: Dash elements.
    """

    user_id = current_user.username

    # Make sure all variables have a value before returning choices
    if pipeline_choice is None:
        return [html.H4("Select a pipeline first.")]

    pipeline = dill.loads(redis_conn.get(pipeline_choice))

    # Reminder: pipelines are named after their graphs following
    # these conventions:
    # Pipeline: userid_pipeline_userProvidedName_lastNodeID
    # Graph: userid_graph_userProvidedName

    # Get the graph for the model
    name = pipeline_choice.split("_")[2]
    model = dill.loads(redis_conn.get(f"{user_id}_graph_{name}"))

    # For each input node
    columns = []
    for input_node in model.input_nodes:
        dataset = input_node.params["dataset"]

        # Prepend the input_node.id to the keys in case of columns
        # with the same name.
        cols = list(f"{key}_{input_node.id}"
                    for key in get_data_schema(dataset, redis_conn)["types"].keys())
        columns.extend(cols)

    var_options = [{"label": col, "value": col}
                   for col in columns]

    # e.g.: linr_001
    output_node_id = "_".join(pipeline_choice.split("_")[-2:])
    output_node = model.graph.node_collection[output_node_id]

    # Depending on the problem type, dis/allow for a Y variable
    if any(isinstance(output_node.model_class(), base)
           for base in [pipeline_classes.ClassifierMixin,
                        pipeline_classes.RegressorMixin]):

        # Supervised
        disabled_y = False

    else:
        # Unsupervised
        disabled_y = True

    return html.Div([
        html.Div(create_dropdown("Choose variable(s) X",
                                 options=var_options,
                                 multi=True, id="xvars_pipeline")),
        html.Div(create_dropdown("Choose target variable Y",
                                 options=var_options,
                                 multi=False, id="yvars_pipeline",
                                 disabled=disabled_y)),
    ])


@app.callback(
    [Output("hidden_results_metrics_pipeline", "children"),
     Output("hidden_results_visualizations_pipeline", "children")],
    [Input("xvars_pipeline", "value"),
     Input("yvars_pipeline", "value")],
    [State('pipeline_choice', "value")])
def fit_model(xvars, yvars, pipeline_choice):
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

    user_id = current_user.username

    pipeline = dill.loads(redis_conn.get(pipeline_choice))
    name = pipeline_choice.split("_")[2]
    model = dill.loads(redis_conn.get(f"{user_id}_graph_{name}"))

    output_node_id = "_".join(pipeline_choice.split("_")[-2:])
    output_node = model.graph.node_collection[output_node_id]

    datasets = []
    for input_node in model.input_nodes:
        dataset = input_node.params["dataset"]
        columns = list(get_data_schema(dataset, redis_conn)["types"].keys())
        columns.extend(columns)

        df = dill.loads(redis_conn.get(dataset))
        # Skip the first characters as they are the input_node's id
        df = df.loc[:, [col[len(input_node.id):]
                        for col in df.columns
                        if (col in xvars+[yvars])]]

        # Join the datasets
        datasets.append(df)

    # Make sure all variables have a value before fitting
    if any(x is None for x in [xvars, yvars, pipeline_choice]):
        raise PreventUpdate()

    # FIXME: We're selecting the first because of one input during
    #        development but we also need to handle for multi-input.
    X = datasets[0]

    # The datasets contain the yvars, so drop them, unless...
    if yvars not in xvars:
        # Someone might want to intentionally pass the Yvar to the model
        # probably for demonstration purposes. Who are we to judge?
        X = X.drop(yvars, axis=1)

    # Only one is needed
    Y = datasets[0][yvars]

    # If we have a classification problem...
    if isinstance(output_node.model_class(), pipeline_classes.ClassifierMixin):
        Y = pd.factorize(Y)[0]

    pipeline.fit(X, Y)

    predictions = pipeline.predict(X)
    score = pipeline.score(X, Y)

    # TODO: EVERYTHING below here is the same as in single_model.
    #       Consider refactoring.
    metrics = []
    if isinstance(output_node.model_class(), pipeline_classes.RegressorMixin):
        metrics.append(html.H4(f"Mean Squared Error: {score:.3f}"))

    elif isinstance(output_node.model_class(), pipeline_classes.ClassifierMixin):
        metrics.append(html.H4(f"Accuracy: {100*score:.3f} %"))
        metrics.append(html.H4("Confusion matrix:"))

        classes = datasets[0][yvars].unique()

        confusion = confusion_matrix(Y, predictions)
        metrics.append(html.Table([
            html.Thead([html.Th(cls) for cls in classes]),

            html.Tbody([
               html.Tr([html.Td(item) for item in row])
               for row in confusion
            ])
        ]))

    else:
        metrics.append("Not implemented")

    # TODO: Visualize the (in)correctly grouped points.
    # If we have >=2 variables, visualize the classification
    if len(xvars) >= 3:

        trace1 = go.Scatter3d(x=X[xvars[0]],
                              y=X[xvars[1]],
                              z=X[xvars[2]],
                              showlegend=False,
                              mode='markers',
                              marker={
                                  'color': predictions.astype(np.float),
                                  'line': dict(color='black', width=1)
                              })

        figure = {
            'data': [trace1],
            'layout': layouts.default_2d(xvars[0], yvars[0])
        }

    elif len(xvars) == 2:
        traces = scatterplot(X[xvars[0]], X[xvars[1]],
                             marker={'color': predictions.astype(np.float)})

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
