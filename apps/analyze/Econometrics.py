"""
    To be implemented.
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from server import app
import layouts
import styles
from utils import r, create_dropdown, mapping, get_data

import dash_bootstrap_components as dbc


def Econometrics_Options(options, results):

    return html.Div(children=[
        # Choose a dataset
        html.Div(create_dropdown("Available datasets", options,
                                 multi=False, id="dataset_choice_econometrics"),
                 style=styles.dropdown()),

        # Choose an algorithm
        html.Div(create_dropdown("Choose algorithm type",
                options=[
                    {'label': 'Econ1', 'value': 'econ1'},
                    {'label': 'Econ2', 'value': 'econ2'},
                ], multi=False, id="algo_choice_econometrics"),
                 style=styles.dropdown()),

        ## Two empty divs to be filled by callbacks
        # Available choices for fitting
        html.Div(id="variable_choices_econometrics"),

        # The results
        html.Div(id="training_results_econometrics"),
    ])


@app.callback(Output("variable_choices_econometrics", "children"),
              [Input("dataset_choice_econometrics", "value"),
               Input("algo_choice_econometrics", "value")],
              [State("user_id", "children")])
def render_variable_choices_econometrics(dataset_choice,
                                         algo_choice_econometrics,
                                         user_id):
    """
        This callback is used in order to create a menu of dcc components
        for the user to choose for altering across datasets.
    """

    df = get_data(dataset_choice, user_id)

    # Make sure all variables have a value before returning choices
    if any(x is None for x in [df, dataset_choice, algo_choice_econometrics]):
        return [html.H4("Select dataset and algorithm first.")]

    options = [{'label': col[:35], 'value': col} for col in df.columns]

    layout = [
        html.Div(create_dropdown("X variable(s)", options,
                                 multi=True, id="xvars_econometrics"),
                       style=styles.dropdown()),
        html.Div(create_dropdown("Target not applicable", options,
                                 multi=False, id="yvars_econometrics"),
                       style=styles.dropdown()),
    ]

    return layout


@app.callback(
    Output("training_results_econometrics", "children"),
    [Input("xvars_econometrics", "value"),
     Input("yvars_econometrics", "value")],
    [State('algo_choice_econometrics', "value"),
     State("user_id", "children"),
     State("dataset_choice_econometrics", "value")])
def fit_clustering_model(xvars, yvars, algo_choice_econometrics,
                  user_id, dataset_choice):
    """
        This callback takes all available user choices and, if all
        are present, it fits the appropriate model.
    """

    df = get_data(dataset_choice, user_id)

    ## Make sure all variables have a value before fitting
    if any(x is None for x in [xvars, df, dataset_choice,
                               algo_choice_econometrics]):
        return {}

    # We have the dictionary that maps keys to models so use that

    return [html.H4("Not implemented")]
