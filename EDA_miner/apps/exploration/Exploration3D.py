"""
This module defines the available graphs and creates the interface \
for the 3D dashboard.

Global Variables:
    - Sidebar: To be used for creating side-menus.

Functions:
    - Exploration3D_Options: Generate the layout of the dashboard.

Dash callbacks:
    - render_variable_choices_3d: Create a menu of dcc components for \
                                  the user to choose  plotting options.
    - plot_graph_3d: Plot the graph according to user choices.

Notes to others:
    You should only write code here with caution, although contribution \
    in this part are very encouraged. You can use this module to add new \
    buttons, input, or other interface-related, element, or maybe a new \
    type of graph (in which case implement it in `graphs.graphs3d.py`). \
    Keep in mind that it may be moved later on to lower-level modules. \
    Also, there is a chance that this will be moved entirely into another \
    tab. Finally, exporting 3D graphs is currently not implemented, so \
    work on that is encouraged as well.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

from server import app
import layouts
from utils import create_dropdown, get_data
from apps.exploration.graphs import graphs3d



Sidebar = []


def Exploration3D_Options(options):
    """
    Generate the layout of the dashboard.

    Args:
        options (list(dict)): Available datasets as options for `dcc.Dropdown`.

    Returns:
        A Dash element or list of elements.
    """

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
    Create a menu of dcc components for the user to choose
    plotting options.

    Args:
        dataset_choice (str): Name of dataset.
        user_id (str): Session/user id.

    Notes on implementation:
        Currently only one type of 3D graph is supported, but more
        should be added later on.
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
    Plot the graph according to user choices.

    Args:
        xvars (str): `x-axis` of the graph.
        yvars (str): `y-axis`.
        zvars (str): `z-axis`.
        user_id (str): Session/user id.
        dataset_choice_3d (str): Name of dataset.

    Returns:
        dict: A dictionary holding a plotly figure including layout.
    """

    if any(x is None for x in [xvars, yvars, zvars]):
        raise PreventUpdate()


    df = get_data(dataset_choice_3d, user_id)

    traces = graphs3d.scatterplot3d(df[xvars], df[yvars], df[zvars])

    return {
        'data': traces,
        'layout': layouts.default_3d(xvars, yvars, zvars)
    }
