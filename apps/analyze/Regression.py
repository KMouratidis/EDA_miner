"""
    To be implemented.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import create_dropdown, mapping, get_data


def Regression_Options(options, results):

    return html.Div(children=[
        # Choose a dataset
        html.Div(create_dropdown("Available datasets", options,
                                 multi=False, id="dataset_choice_regression"),
                 className="horizontal_dropdown"),

        # Choose an algorithm
        html.Div(create_dropdown("Choose algorithm type", options=[
            {'label': 'Linear Regression', 'value': 'linr'},
            {'label': 'SVM Regression', 'value': 'svr'},
            {'label': 'Decision Tree Regression', 'value': 'dtr'}
        ], multi=False, id="algo_choice_regression"),
         className="horizontal_dropdown"),

        ## Two empty divs to be filled by callbacks
        # Available choices for fitting
        html.Div(id="variable_choices_regression"),

        # The results
        html.Div(id="training_results_regression"),
    ])


@app.callback(Output("variable_choices_regression", "children"),
              [Input("dataset_choice_regression", "value"),
               Input("algo_choice_regression", "value")],
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
                                 multi=True, id="xvars_regression"),
                 className="horizontal_dropdown"),
        html.Div(create_dropdown("Y variable", options,
                                 multi=False, id="yvars_regression"),
                 className="horizontal_dropdown"),
    ]

    return layout


@app.callback(
    Output("training_results_regression", "children"),
    [Input("xvars_regression", "value"),
     Input("yvars_regression", "value")],
    [State('algo_choice_regression', "value"),
     State("user_id", "children"),
     State("dataset_choice_regression", "value")])
def fit_regression_model(xvars, yvars, algo_choice_regression,
                         user_id, dataset_choice):
    """
        This callback takes all available user choices and, if all
        are present, it fits the appropriate model.
    """

    df = get_data(dataset_choice, user_id)

    ## Make sure all variables have a value before fitting
    if any(x is None for x in [xvars, yvars, df, dataset_choice,
                               algo_choice_regression]):
        return {}

    # We have the dictionary that maps keys to models so use that
    model = mapping[algo_choice_regression]()

    model.fit(df[xvars], df[yvars])

    return [
        html.H4(f"Regression model scored: {model.score(df[xvars], df[yvars])}")
    ]
