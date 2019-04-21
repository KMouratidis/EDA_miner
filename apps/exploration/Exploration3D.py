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
import layouts
from utils import create_dropdown, get_data
from apps.exploration.graphs import graphs3d


Sidebar = []


def Exploration3D_Options(options, results):

    return html.Div(children=[

        html.Div([
            # Choose a dataset
            html.Div(create_dropdown("Available datasets", options,
                                     multi=False, id="dataset_choice_3d"),
                     className="vertical_dropdowns"),

            # Available buttons and choices for plotting
            html.Div(id="variable_choices_3d", children=[
                html.Div(create_dropdown(f"{dim} variable", options=[],
                                         multi=False, id=f"{dim}vars_3d"),
                         className="vertical_dropdowns")
                for dim in ["x", "y", "z"]]),

            # Export graph config
            html.Div([
                html.Br(),
                html.Button("Export graph config 1", id="export_graph1"),
                html.Button("Export graph config 2", id="export_graph2"),
            ], className="vertical_dropdowns"),

        ], className="col-sm-4"),

        # The graph itself
        html.Div([
            dcc.Graph(id="graph_3d"),
        ], className="col-sm-8"),
    ], className="row")


@app.callback([Output("xvars_3d", "options"),
               Output("yvars_3d", "options"),
               Output("zvars_3d", "options")],
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
        return [[], [], []]

    options = [{'label': col[:35], 'value': col} for col in df.columns]

    return [options, options, options]


@app.callback(
    Output("graph_3d", "figure"),
    [Input("xvars_3d", "value"),
     Input("yvars_3d", "value"),
     Input("zvars_3d", "value")],
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
