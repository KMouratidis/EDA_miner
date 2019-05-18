"""
This module defines the interface for doing econometrics stuff.

Functions:
    - Econometrics_Options: Generate the layout of the dashboard.

Dash callbacks:
    - render_variable_choices_econometrics: Create a menu of dcc components \
                                            for the user to choose fitting \
                                            options.
    - fit_econometrics_model: Fits any models defined.

Notes to others:
    Not implemented yet. Feel free to experiment as much as you like here. \
    What do econometricians do other than glorified linear regressions?! :D
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

from server import app
from utils import create_dropdown, get_data



def Econometrics_Options(options, results):

    return html.Div(children=[
        # Choose a dataset
        html.Div(create_dropdown("Available datasets", options,
                                 multi=False, id="dataset_choice_econometrics"),
                 className="horizontal_dropdowns"),

        # Choose an algorithm
        html.Div(create_dropdown("Choose algorithm type", options=[
            {'label': 'Econ1', 'value': 'econ1'},
            {'label': 'Econ2', 'value': 'econ2'},
        ], multi=False, id="algo_choice_econometrics"),
                 className="horizontal_dropdowns"),

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
    Create a menu of dcc components to select dataset, variables,
    and training options.

    Args:
        dataset_choice (str): Name of dataset.
        algo_choice_econometrics (str): The choice of algorithm type.
        user_id (str): Session/user id.

    Returns:
        list: Dash elements.
    """


    df = get_data(dataset_choice, user_id)

    # Make sure all variables have a value before returning choices
    if any(x is None for x in [df, dataset_choice, algo_choice_econometrics]):
        return [html.H4("Select dataset and algorithm first.")]

    # Truncate labels so they don't fill the whole dropdown
    options = [{'label': col[:35], 'value': col} for col in df.columns]

    layout = [
        html.Div(create_dropdown("X variable(s)", options,
                                 multi=True, id="xvars_econometrics"),
                 className="horizontal_dropdowns"),
        html.Div(create_dropdown("Target not applicable", options,
                                 multi=False, id="yvars_econometrics"),
                 className="horizontal_dropdowns"),
    ]

    return layout


@app.callback(
    Output("training_results_econometrics", "children"),
    [Input("xvars_econometrics", "value"),
     Input("yvars_econometrics", "value")],
    [State('algo_choice_econometrics', "value"),
     State("user_id", "children"),
     State("dataset_choice_econometrics", "value")])
def fit_econometrics_model(xvars, yvars, algo_choice_econometrics,
                           user_id, dataset_choice):
    """
    Take user choices and, if all are present, fit the appropriate model.

    Args:
        xvars (list(str)): predictor variables.
        yvars (str): target variable.
        algo_choice_econometrics (str): The choice of algorithm type.
        user_id: Session/user id.
        dataset_choice: Name of dataset.

    Returns:
        list: Dash element(s) with the results of model fitting.
    """


    df = get_data(dataset_choice, user_id)

    ## Make sure all variables have a value before fitting
    if any(x is None for x in [xvars, df, dataset_choice,
                               algo_choice_econometrics]):
        raise PreventUpdate()

    return [html.H4("Not implemented")]
