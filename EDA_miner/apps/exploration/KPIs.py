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

from server import app
import layouts
from utils import create_dropdown, get_data
from apps.exploration.graphs import kpis



Sidebar = [
    ]


def KPI_Options(options, results):

    return html.Div(children=[

        html.Div(create_dropdown("Available datasets", options,
                                 multi=False, id="dataset_choice_kpi"),
                 className="horizontal_dropdowns"),

        # TODO: use this for kpi/graph selection ?
        html.Div(create_dropdown("Choose graph type", options,
                                 multi=False, id="graph_choice_kpi",
                                 disabled=True),
                 className="horizontal_dropdowns"),

        html.Div(id="variable_choices_kpi", children=[
            html.Div(create_dropdown("X variables", options=[],
                                     multi=False, id="xvars_kpi"),
                     className="horizontal_dropdowns"),
            html.Div(create_dropdown("Y variable", options=[],
                                     multi=True, id="yvars_kpi"),
                     className="horizontal_dropdowns"),
            html.Div(create_dropdown("Bar Chart variable", options=[],
                                     multi=False, id="secondary_yvars_kpi"),
                     className="horizontal_dropdowns"),
        ]),

        dcc.Graph(id="graph_kpi"),
    ])


@app.callback([Output("xvars_kpi", "options"),
               Output("yvars_kpi", "options"),
               Output("secondary_yvars_kpi", "options")],
              [Input("dataset_choice_kpi", "value")],
              [State("user_id", "children")])
def render_variable_choices_kpi(dataset_choice, user_id):
    """
    Create a menu of dcc components for the user to choose \
    plotting options.

    Args:
        dataset_choice (str): Name of dataset.
        user_id (str): Session/user id.

    Returns:
        list(list(dict)): Key-value pairs to be input as \
                          `dcc.Dropdown` options.

    Notes on implementation:
        Currently only one type of KPI graph is supported, but more \
        should be added later on. Additionally, work should be done \
        on building custom KPIs and maybe graphs.
    """


    df = get_data(dataset_choice, user_id)

    # Make sure all variables have a value before returning choices
    if any(x is None for x in [df, dataset_choice]):
        return [[], [], []]

    options = [{'label': col[:35], 'value': col} for col in df.columns]

    return [options, options, options]


@app.callback(
    Output("graph_kpi", "figure"),
    [Input("xvars_kpi", "value"),
     Input("yvars_kpi", "value"),
     Input("secondary_yvars_kpi", "value")],
    [State("user_id", "children"),
     State('dataset_choice_kpi', 'value')])
def plot_graph_kpi(xvars, yvars, secondary_yvars,
                   user_id, dataset_choice):
    """
    Plot the graph according to user choices.

    Args:
        xvars (str): `x-axis` of the graph.
        yvars (str or list(str)): `y-axis`, can be multiple.
        secondary_yvars: `bar-chart` variable.
        user_id (str): Session/user id.
        dataset_choice (str): Name of dataset.

    Returns:
        dict: A dictionary holding a plotly figure including layout.
    """


    df = get_data(dataset_choice, user_id)

    if any(x is None for x in [xvars, yvars, secondary_yvars,
                               df, dataset_choice]):
        return {}

    # baseline graph
    traces = kpis.baseline_graph(df, xvars, yvars, secondary_yvars)

    return {
        'data': traces,
        'layout': layouts.default_2d(xvars, yvars[0])
    }
