"""
    This module will be used to plot 3D graphs.

    You can write code in this module, but keep in
    mind that it may be moved later on to lower-level
    modules. Also, there is a chance that this will be
    moved entirely into another tab.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import r, create_dropdown, get_data
from apps.exploration.graphs import graphs2d, graphs3d, layouts, styles

import plotly.graph_objs as go


def Exploration3D_Options(options, results):

    return html.Div(children=[

        html.Div([
            # Choose a dataset
            html.Div(create_dropdown("Available datasets", options,
                                     multi=False, id="dataset_choice_3d"),
                     style=styles.dropdown_3d()),

            ## Two empty divs to be filled by callbacks
            # Available buttons and choices for plotting
            html.Div(id="variable_choices_3d"),

            # Export graph config
            html.Div([
                html.Br(),
                html.Button("Export graph config 1", id="export_graph1"),
                html.Button("Export graph config 2", id="export_graph2"),
            ], style=styles.dropdown_3d()),

        ], className="col-sm-4"),

        html.Div([
            # The graph itself
            dcc.Graph(id="graph_3d"),
        ], className="col-sm-8"),
    ], className="row")


@app.callback(Output("variable_choices_3d", "children"),
          [Input("dataset_choice_3d", "value")],
          [State("user_id", "children")])
def render_variable_choices_3d(dataset_choice, user_id):
    """
        This callback is used in order to create a menu of dcc components
        for the user to choose for altering plotting options based on datasets.
    """

    df = get_data(dataset_choice, user_id)

    # Make sure all variables have a value before returning choices
    if any(x is None for x in [df, dataset_choice]):
        return [html.H4("Select dataset.")]


    # TODO: This probably is not needed anymore, the check is performed above
    options = [{'label': "No dataset selected yet", 'value': "no_data"}]
    if df is not None:
        options=[{'label': col[:35], 'value': col} for col in df.columns]


    layout = [
        html.Div(create_dropdown(f"{dim} variable", options,
                                 multi=False, id=f"{dim}vars_3d"),
                       style=styles.dropdown_3d())
     for dim in ["x", "y", "z"]]


    return layout


@app.callback(
    Output("graph_3d", "figure"),
    [Input(f"{dim}vars_3d", "value")
        for dim in ['x', 'y', 'z']],
    [State("user_id", "children"),
     State("dataset_choice_3d", "value")])
def plot_graph_3d(xvars, yvars, zvars, user_id, dataset_choice_3d):
    """
        This callback takes all available user choices and, if all
        are present, it returns the appropriate plot.
    """

    df = get_data(dataset_choice_3d, user_id)

    traces = graphs3d.scatterplot(df[xvars], df[yvars], df[zvars])

    return {
        'data': traces,
        'layout': layouts.default_3d(xvars, yvars, zvars)
    }
