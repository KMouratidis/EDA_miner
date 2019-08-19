"""
This module is about building and viewing KPIs. The user should be \
able to view more advanced graphs and also create their own indicators.

Global Variables:
    - Sidebar: To be used for creating side-menus.

Functions:
    - KPI_Options: Generate the layout of the dashboard.

Dash callbacks:
    - render_variable_choices_kpi: Create a menu of dcc components for \
                                   the user to choose  plotting options.
    - plot_graph_kpi: Plot the graph according to user choices.

Notes to others:
    Contributions are greatly needed and encouraged here. Main \
    functionality is still lacking in this part. You can use this \
    module to add new buttons, input, or other interface-related, \
    element, or maybe a new type of graph (in which case implement \
    it in `graphs.kpis.py`). Working on exporting KPI graphs is \
    also encouraged.
"""


from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from .server import app, redis_conn
import layouts
from utils import create_dropdown, get_variable_options
from .graphs import kpis

import dill


Sidebar = []


def KPI_Options(options):
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
                                     multi=False, id="dataset_choice_kpi"),
                     className="vertical_dropdowns"),

            # TODO: use this for kpi/graph selection ?
            html.Div(create_dropdown("Choose graph type", options,
                                     multi=False, id="graph_choice_kpi",
                                     disabled=True),
                     className="vertical_dropdowns"),

            # Available buttons and choices for plotting
            html.Div(id="variable_choices_kpi", children=[
                html.Div(create_dropdown("X variables", options=[],
                                         multi=False, id="xvars_kpi"),
                         className="vertical_dropdowns"),

                html.Div(create_dropdown("Y variable", options=[],
                                         multi=True, id="yvars_kpi"),
                         className="vertical_dropdowns"),

                html.Div(create_dropdown("Bar Chart variable", options=[],
                                         multi=False, id="secondary_yvars_kpi"),
                         className="vertical_dropdowns"),
            ])
        ], className="col-sm-3"),

        # The graph itself
        html.Div([
            dcc.Graph(id="graph_kpi", style={"minHeight": "650px"})
        ], className="col-sm-9"),

    ], className="row")


@app.callback([Output("xvars_kpi", "options"),
               Output("yvars_kpi", "options"),
               Output("secondary_yvars_kpi", "options")],
              [Input("dataset_choice_kpi", "value")])
def render_variable_choices_kpi(dataset_choice):
    """
    Create a menu of dcc components for the user to choose \
    plotting options.

    Args:
        dataset_choice (str): Name of the dataset.

    Returns:
        list(list(dict)): Key-value pairs to be input as \
                          `dcc.Dropdown` options.

    Notes on implementation:
        Currently only one type of KPI graph is supported, but more \
        should be added later on. Additionally, work should be done \
        on building custom KPIs and maybe graphs.
    """

    if dataset_choice is None:
        return [[]] * 3

    options = get_variable_options(dataset_choice, redis_conn)

    return [options] * 3


@app.callback(
    Output("graph_kpi", "figure"),
    [Input("xvars_kpi", "value"),
     Input("yvars_kpi", "value"),
     Input("secondary_yvars_kpi", "value")],
    [State('dataset_choice_kpi', 'value')])
def plot_graph_kpi(xvars, yvars, secondary_yvars, dataset_choice):
    """
    Plot the graph according to user choices.

    Args:
        xvars (str): `x-axis` of the graph.
        yvars (str or list(str)): `y-axis`, can be multiple.
        secondary_yvars: `bar-chart` variable.
        dataset_choice (str): Name of dataset.

    Returns:
        dict: A dictionary holding a plotly figure including layout.
    """

    # Conditions necessary to do any plotting
    conditions = [xvars, yvars, secondary_yvars, dataset_choice]
    if any(var is None for var in conditions):
        return {}

    df = dill.loads(redis_conn.get(dataset_choice))

    # baseline graph
    traces = kpis.baseline_graph(df, xvars, yvars, secondary_yvars)

    return {
        'data': traces,
        'layout': layouts.default_2d(xvars, yvars[0])
    }
