"""
    To be implemented.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import r, create_dropdown, get_data

import dill


def Pipeline_Options(options, results, user_id):

    if user_id.startswith("python_generated_ssid"):
        # Trim id
        user_id = user_id.split("-")[-1]

    available_pipelines = {k.decode(): r.get(k)
                           for k in r.keys(f'{user_id}_pipeline_*')}

    return html.Div(children=[
        # Choose a dataset
        html.Div(create_dropdown("Available datasets", options,
                                 multi=False, id="dataset_choice_pipeline"),
                 className="horizontal_dropdowns"),

        # Choose an algorithm
        html.Div(create_dropdown("Choose algorithm type", options=[
            {'label': f'Pipeline --> {pipe_name}', 'value': pipe_name}
            for pipe_name in available_pipelines
        ], multi=False, id="algo_choice_pipeline"),
                 className="horizontal_dropdowns"),

        # Available choices for fitting
        html.Div(id="variable_choices_pipeline"),

        # The results
        html.Div(id="training_results_pipeline"),
    ])


@app.callback(Output("variable_choices_pipeline", "children"),
              [Input("dataset_choice_pipeline", "value"),
               Input("algo_choice_pipeline", "value")],
              [State("user_id", "children")])
def render_variable_choices_clustering(dataset_choice, algo_choice_regression,
                                       user_id):
    """
        This callback is used in order to create a menu of dcc components
        for the user to choose for altering across datasets.
    """

    df = get_data(dataset_choice, user_id)

    # Make sure all variables have a value before returning choices
    if any(x is None for x in [df, dataset_choice, algo_choice_regression]):
        return [html.H4("Select dataset and algorithm first.")]

    options = [{'label': col[:35], 'value': col} for col in df.columns]

    layout = [
        html.Div(create_dropdown("X variable(s)", options,
                                 multi=True, id="xvars_pipeline"),
                 className="horizontal_dropdowns"),
        html.Div(create_dropdown("Y variable", options,
                                 multi=False, id="yvars_pipeline"),
                 className="horizontal_dropdowns"),
    ]

    return layout


@app.callback(
    Output("training_results_pipeline", "children"),
    [Input("xvars_pipeline", "value"),
     Input("yvars_pipeline", "value")],
    [State('algo_choice_pipeline', "value"),
     State("user_id", "children"),
     State("dataset_choice_pipeline", "value")])
def fit_regression_model(xvars, yvars, algo_choice_pipeline,
                         user_id, dataset_choice):
    """
        This callback takes all available user choices and, if all
        are present, it fits the appropriate model.
    """

    df = get_data(dataset_choice, user_id)

    ## Make sure all variables have a value before fitting
    if any(x is None for x in [xvars, yvars, df, dataset_choice,
                               algo_choice_pipeline]):
        return []

    # We have the dictionary that maps keys to models so use that
    model = dill.loads(r.get(algo_choice_pipeline))

    model.fit(df[xvars], df[yvars])

    # TODO: Implement score function for all models, including clustering
    return [
        html.H4(f"Pipeline model scored: {model.score(df[xvars], df[yvars])}")
    ]
