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

from server import app
from utils import r, create_dropdown, get_data
from apps.analyze.models import pipeline_classes

import dill
from apps.analyze.models import pipeline_creator


def Pipeline_Options(options, results, user_id):

    if user_id.startswith("python_generated_ssid"):
        # Trim id
        user_id = user_id.split("-")[-1]

    available_pipelines = {k.decode(): r.get(k)
                           for k in r.keys(f'{user_id}_pipeline_*')}

    return html.Div(children=[
        # Dataset is defined in the ModelBuilder

        # Choose an algorithm
        html.Div(create_dropdown("Choose algorithm type", options=[
            {'label': f'Pipeline --> {pipe_name}', 'value': pipe_name}
            for pipe_name in available_pipelines
        ], multi=False, id="algo_choice_pipeline"),
                 className="horizontal_dropdowns"),

        # Available choices for fitting
        html.Div(id="variable_choices_pipeline", children=[
            # Debuggers
            html.Button("Fit model", id="fit_model", n_clicks=0,
                        style={"display": "none"}),
            html.Div(create_dropdown("", [], multi=True, id="xvars_pipeline",
                                     style={"display": "none"})),
            html.Div(create_dropdown("", [], multi=True, id="yvars_pipeline",
                                     style={"display": "none"})),

        ]),

        # The results
        html.Div(id="training_results_pipeline"),
    ])


@app.callback(Output("variable_choices_pipeline", "children"),
              [Input("algo_choice_pipeline", "value")],
              [State("user_id", "children")])
def render_variable_choices_pipeline(algo_choice_pipeline,
                                     user_id):
    """
    Create a menu of dcc components to select pipeline and variables.

    Args:
        algo_choice_pipeline (str): Choice among (pre)defined pipelines.
        user_id (str): Session/user id.

    Returns:
        list: Dash elements.
    """


    # Make sure all variables have a value before returning choices
    if algo_choice_pipeline is None:
        return [html.H4("Select a pipeline first.")]

    model = dill.loads(r.get(algo_choice_pipeline))

    input_node = pipeline_creator.find_pipeline_node(
        pipeline_classes.BaseInput
    )(model)

    terminal_node = pipeline_creator.find_pipeline_node(
        pipeline_classes.TerminalNode
    )(model)

    # defaults
    layout = []
    options = []

    if isinstance(input_node, pipeline_classes.GenericInput):
        try:
            dataset_choice = input_node.dataset
        except AttributeError:
            return [html.H4("Something went wrong with the input")]

        if isinstance(input_node, pipeline_classes.TwitterAPI):
            layout += [
                html.Button("Fit model", id="fit_model", n_clicks=0),

                # Debugger
                html.Div(dcc.Dropdown(options=[], multi=True, id="xvars_pipeline",
                                      style={"display": "none"})),
            ]

        else:
            df = get_data(dataset_choice, user_id)

            # Truncate labels so they don't fill the whole dropdown
            options = [{'label': col[:35], 'value': col} for col in df.columns]

            layout += [
                html.Div(create_dropdown("X variable(s)", options,
                                         multi=True, id="xvars_pipeline"),
                         className="horizontal_dropdowns"),

                # to debug the next callback
                html.Button("Fit model", id="fit_model", n_clicks=0,
                            style={"display": "none"})
            ]

    else:
        layout += [
            # Debuggers
            html.Button("Fit model", id="fit_model", n_clicks=0,
                               style={"display": "none"}),
            html.Div(dcc.Dropdown(options=[], multi=True, id="xvars_pipeline",
                                     style={"display": "none"})),
        ]

    if not isinstance(terminal_node, pipeline_classes.UnsupervisedLearner):
        layout += [html.Div(dcc.Dropdown(options=options,
                            multi=False, id="yvars_pipeline"),
                            className="horizontal_dropdowns")]

    else:
        # Only existing for debugging the next callback, no yvars needed
        layout += [dcc.Dropdown(options=[], id="yvars_pipeline",
                                style={"display": "none"})]

    return layout


@app.callback(
    Output("training_results_pipeline", "children"),
    [Input("xvars_pipeline", "value"),
     Input("yvars_pipeline", "value"),
     Input("fit_model", "n_clicks")],
    [State('algo_choice_pipeline', "value"),
     State("user_id", "children")])
def fit_pipeline_model(xvars, yvars, fit_model, algo_choice_pipeline, user_id):
    """
    Take user choices and, if all are present, fit the appropriate model.

    Args:
        xvars (list(str)): predictor variables.
        yvars (str): target variable.
        algo_choice_pipeline (str): Choice among (pre)defined pipelines.
        user_id: Session/user id.

    Returns:
        list: Dash element(s) with the results of model fitting.
    """

    if algo_choice_pipeline is None:
        raise PreventUpdate()


    # We have the dictionary that maps keys to models so use that
    model = dill.loads(r.get(algo_choice_pipeline))

    input_node = pipeline_creator.find_pipeline_node(
        pipeline_classes.GenericInput
    )(model)

    terminal_node = pipeline_creator.find_pipeline_node(
        pipeline_classes.TerminalNode
    )(model)

    if isinstance(input_node, pipeline_classes.GenericInput):
        if isinstance(input_node, pipeline_classes.TwitterAPI):
            if fit_model == 0:
                # Don't fit
                raise PreventUpdate()

            X = []

        else:
            try:
                dataset_choice = input_node.dataset
            except AttributeError:
                return [html.H4("Something went wrong with the input")]

            df = get_data(dataset_choice, user_id)

            ## Make sure all variables have a value before fitting
            if any(x is None for x in [xvars, df, dataset_choice]):
                raise PreventUpdate()

            # if we used df[xvars] directly the ordering of variables that the user
            # gave would actually affect the model. This forces those variables to
            # be in the order of the original df. It matters only here since the
            # user might have defined a FeatureMaker that depends on this.
            xvars = [xvar for xvar in df.columns if xvar in xvars]
            X = df[xvars]

    else:
        X = []

    if isinstance(terminal_node, pipeline_classes.UnsupervisedLearner):
        model.fit(X)
        return [html.H4(str(model.predict(X)))]

    else:

        if yvars is None:
            raise PreventUpdate()

        model.fit(X, df[yvars])

        # TODO: Implement score function for all models.
        return [
            html.H4(f"Pipeline model scored: {model.score(df[xvars], df[yvars])}")
        ]

