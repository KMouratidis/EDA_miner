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

import dash_bootstrap_components as dbc

from .server import app, redis_conn
from utils import create_dropdown, get_data_schema
from visualization.graphs.graphs2d import scatterplot
import layouts

import pandas as pd
import numpy as np
import dill
from flask_login import current_user
from sklearn.metrics import confusion_matrix
import plotly.graph_objs as go
from sklearn.base import ClusterMixin, ClassifierMixin, RegressorMixin


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

    return [

        # The right side with the results
        html.Div([

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

            # A modal for exporting the model
            dbc.Modal([
                dbc.ModalHeader("Trained model export report."),
                dbc.ModalBody(id="modal_body")
            ], id=f"export_model_modal", is_open=False),

            # The fitting results (target of the tab menu)
            html.Div(id="fitting_report_pipeline")
        ], id="training_results_div"),

        # The tab menu
        html.Div([

            # Choose a dataset
            html.Div(create_dropdown("Available pipelines", options=[
                {'label': f'Pipeline --> {pipe_name}', 'value': pipe_name}
                for pipe_name in available_pipelines
            ], multi=False, id="pipeline_choice")),

            html.Div(id="variable_choices_pipeline"),

        ], id="pipelines_menu"),
    ]


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

        # Append the input_node.id to the keys in case of columns
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
           for base in [ClassifierMixin, RegressorMixin]):

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

        html.Div([
            html.H6("Export trained model..."),
            html.Button("Export!", id="export_model_button"),
        ])
    ])


@app.callback(
    [Output("hidden_results_metrics_pipeline", "children"),
     Output("hidden_results_visualizations_pipeline", "children"),
     Output("export_model_as_name", "is_disabled")],
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

    # Make sure all variables have a value before fitting
    if any(x is None for x in [xvars, pipeline_choice]):
        raise PreventUpdate()

    user_id = current_user.username

    pipeline = dill.loads(redis_conn.get(pipeline_choice))
    name = pipeline_choice.split("_")[2]
    model = dill.loads(redis_conn.get(f"{user_id}_graph_{name}"))

    output_node_id = "_".join(pipeline_choice.split("_")[-2:])
    output_node = model.graph.node_collection[output_node_id]

    if not isinstance(output_node.model_class(), ClusterMixin):
        # Test if yvars was provided
        if yvars is None:
            raise PreventUpdate()

    # Initialize the clean version of yvars.
    # The clean versions are used for pandas indexing.
    # The original versions MIGHT be used during the
    # deployment stage when given different datasets.
    clean_yvars = yvars

    datasets = []
    for input_node in model.input_nodes:
        dataset = input_node.params["dataset"]
        columns = list(get_data_schema(dataset, redis_conn)["types"].keys())
        columns.extend(columns)

        # Remove the node id from the yvars
        # -1 because of the extra underscore
        if yvars.endswith(input_node.id):
            clean_yvars = yvars[:len(yvars)-len(input_node.id)-1]

        # same for xvars
        clean_xvars = [xvar[:len(xvar)-len(input_node.id)-1]
                       if xvar.endswith(input_node.id) else xvar
                       for xvar in xvars]

        df = dill.loads(redis_conn.get(dataset))
        # Skip the last characters as they are the input_node's id
        df = df.loc[:, [col for col in df.columns
                        if (col in clean_xvars+[clean_yvars])]]

        # since the datasets are concatenated, add the node id again
        df.columns = [f"{col}_{input_node.id}" for col in df.columns]

        # Join the datasets
        datasets.append(df)

    # FIXME: We're selecting the first because of one input during
    #        development but we also need to handle for multi-input.
    if (all(dataset.shape[0] == datasets[0].shape[0]
            for dataset in datasets[1:])):
        X = pd.concat(datasets, axis=1)

    elif (all(dataset.shape[1] == datasets[0].shape[1]
            for dataset in datasets[1:])):
        X = pd.concat(datasets, axis=0)

    else:
        print([dataset.shape for dataset in datasets])
        raise Exception("CANNOT CONCAT")

    # Only one is needed
    # This might also need fixing as Y might exist in only one dataset
    Y = X[yvars]

    # The datasets contain the yvars, so drop them, unless...
    if yvars not in xvars:
        # Someone might want to intentionally pass the Yvar to the model
        # probably for demonstration purposes. Who are we to judge?
        X = X.drop(yvars, axis=1)

    # If we have a classification problem...
    if isinstance(output_node.model_class(), ClassifierMixin):
        Y = pd.factorize(Y)[0]

    pipeline.fit(X, Y)

    # Save the fitted model for 1 hour. If the users want, they can save it
    # in the next step.
    redis_conn.set(f"{user_id}_trainedModel_{name}",
                   dill.dumps(pipeline),
                   ex=3600)
    redis_conn.set(f"{user_id}_trainedModelParams_{name}",
                   dill.dumps({"xvars": xvars,
                               "yvars": yvars,
                               "problem_type": output_node.problem,
                               "node_type": output_node.node_type}),
                   ex=3600)

    predictions = pipeline.predict(X)
    score = pipeline.score(X, Y)

    # TODO: EVERYTHING below here is the same as in single_model.
    #       Consider refactoring.
    metrics = []
    if isinstance(output_node.model_class(), RegressorMixin):
        metrics.append(html.H4(f"Mean Squared Error: {score:.3f}"))

    elif isinstance(output_node.model_class(), ClassifierMixin):
        metrics.append(html.H4(f"Accuracy: {100*score:.3f} %"))
        metrics.append(html.H4("Confusion matrix:"))

        classes = X[yvars].unique()

        confusion = confusion_matrix(Y, predictions)
        metrics.append(html.Table([
            html.Thead([html.Th(" ")] + [html.Th(cls) for cls in classes]),

            html.Tbody([
               html.Tr([html.Td(html.B(cls))]+[
                   html.Td(item) for item in row
               ]) for (cls, row) in zip(classes, confusion)
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
            'layout': go.Layout(
                scene={
                    "xaxis_title": xvars[0].split("_input_file")[0],
                    "yaxis_title": xvars[1].split("_input_file")[0],
                    "zaxis_title": xvars[2].split("_input_file")[0],
                },
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                height=650
            )
        }

    elif len(xvars) == 2:
        traces = scatterplot(X[xvars[0]], X[xvars[1]],
                             marker={'color': predictions.astype(np.float)})

        figure = {
            'data': [traces],
            'layout': go.Layout(
                scene={
                    "xaxis_title": xvars[0].split("_input_file")[0],
                    "yaxis_title": xvars[1].split("_input_file")[0],
                },
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                height=650
            )
        }

    else:
        figure = {}

    return metrics, figure, False


@app.callback([Output("export_model_modal", "is_open"),
               Output("modal_body", "children")],
              [Input("export_model_button", "n_clicks")],
              [State('pipeline_choice', "value")])
def export_model_as(n_clicks, pipeline_choice):
    if not n_clicks:
        raise PreventUpdate()

    user_id = current_user.username
    name = pipeline_choice.split("_")[2]

    # Check how many models the user has saved. If they are at
    # their limit, then don't save this model.
    total_permanent_models = 0
    for key in redis_conn.keys(f"{user_id}_trainedModel*"):
        if redis_conn.ttl(key) == -1:
            total_permanent_models += 1

    if total_permanent_models >= 3:
        return True, html.Div("Delete an existing model before saving "
                              "a new one, or contact the admin for favors.")

    # Permanently save the model & params.
    redis_conn.persist(f"{user_id}_trainedModel_{name}")
    redis_conn.persist(f"{user_id}_trainedModelParams_{name}")

    return True, html.Div(f"Saved model {name} successfully")
