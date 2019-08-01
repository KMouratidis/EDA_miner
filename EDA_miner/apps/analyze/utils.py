"""
This module defines the interface for fitting simple classification models.

Global Variables:
    - Classification_Options: Generate the layout of the dashboard.

Dash callbacks:
    - render_variable_choices_classification: Create a menu of dcc components \
                                              for the user to choose fitting \
                                              options.
    - fit_classification_model: Take user choices and, if all are present, fit \
                                the appropriate model.

Notes to others:
    Feel free to experiment as much as you like here, although you probably \
    want to write code elsewhere.
"""

import dash_html_components as html
from dash.dependencies import Input, Output, State

from server import app
from utils import create_dropdown, mapping, get_data



def render_variable_choices(tab):
    @app.callback(Output(f"variable_choices_{tab}", "children"),
                  [Input(f"dataset_choice_{tab}", "value"),
                   Input(f"algo_choice_{tab}", "value")],
                  [State("user_id", "children")])
    def _render_variable_choices(dataset_choice, algo_choice, user_id, tab=tab):
        """
        Create a menu of dcc components for the user to choose fitting options. \
        This function is similar for all menus in the analyze tab, and only needs \
        the `app.callback` applied to it

        Args:
            dataset_choice (str): Name of dataset.
            algo_choice (str): The choice of algorithm type.
            user_id (str): Session/user id.
            tab (str): The tab you're currently on. Must be the same as the one \
                       the other callbacks are listening to.

        Returns:
            list: Dash elements.
        """


        df = get_data(dataset_choice, user_id)

        # Make sure all variables have a value before returning choices
        if any(x is None for x in [df, dataset_choice, algo_choice]):
            return [html.H4("Select dataset and algorithm first.")]

        # Truncate labels so they don't fill the whole dropdown
        options = [{'label': col[:35], 'value': col} for col in df.columns]

        layout = [
            html.Div(create_dropdown("X variable(s)", options,
                                     multi=True, id=f"xvars_{tab}"),
                     className="horizontal_dropdowns"),
            html.Div(create_dropdown("Y variable", options,
                                     multi=False, id=f"yvars_{tab}"),
                     className="horizontal_dropdowns"),
        ]

        return layout