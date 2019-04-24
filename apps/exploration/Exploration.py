"""
This module defines the available graphs and creates the interface
for the 2D dashboard.

Global Variables:
    - Sidebar: To be used for creating side-menus.
    - Graphs_Export: Two buttons to export graphs (later used for
                     PDF report generation).

Functions:
    - Exploration_Options: Generate the layout of the dashboard.

Dash callbacks:
    - render_variable_choices_2d: Create a menu of dcc components for
                                  the user to choose  plotting options.
    - plot_graph_2d: Plot the graph according to user choices.
    - toggle_modal: Notify when a graph is exported.
    - export_graph_callback: Export a graph (to a hidden div). One for
                             every hidden graph.

Notes to others:
    You should only write code here with caution. You can use this
    module to add new buttons, input, or other interface-related,
    element, or maybe a new type of graph (in which case implement
    it in `graphs.graphs2d.py`).
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc

from server import app
import layouts
from utils import create_dropdown
from apps.data.View import get_data
from apps.exploration.graphs import graphs2d

import plotly.graph_objs as go


def Exploration_Options(options, results):

    return html.Div(children=[

        # Choose a dataset
        html.Div(create_dropdown("Available datasets", options,
                                 multi=False, id="dataset_choice_2d"),
                 className="horizontal_dropdowns"),

        # Choose a graph
        html.Div(create_dropdown("Choose graph type", options=[
            {'label': 'Line Graph', 'value': 'line_chart'},
            {'label': 'Scatter Plot', 'value': 'scatterplot'},
            {'label': 'Histogram Graph', 'value': 'histogram'},
            {'label': 'Correlation Graph', 'value': 'heatmap'},
            {'label': 'Bubble Graph', 'value': 'bubble_chart'},
            {'label': 'Pie Chart', 'value': 'pie'},
            {'label': 'Filled Area Graph', 'value': 'filledarea'},
            {'label': 'Error Bar Graph', 'value': 'errorbar'},
            {'label': '2D Density Plot', 'value': 'density2d'},
            {'label': 'PairPlot (matplotlib)', 'value': 'pairplot'},
        ], multi=False, id="graph_choice_exploration"),
                 className="horizontal_dropdowns"),

        # Available buttons and choices for plotting
        html.Div(id="variable_choices_2d", children=[
            html.Div(create_dropdown("X variable", options=[],
                                     multi=False, id="xvars_2d"),
                     className="horizontal_dropdowns"),

            html.Div(create_dropdown("Y variable", options=[],
                                     multi=False,
                                     id="yvars_2d"),
                     className="horizontal_dropdowns"),
        ]),

        # The graph itself
        dcc.Graph(id="graph_2d"),
    ])


# Export graph config
Graphs_Export = [
    # Fancy bootstrap card containing buttons
    dbc.Card([
        dbc.CardHeader("Export graphs"),
        dbc.CardBody([
            dbc.Button("Export graph config 1", id="export_graph1",
                       color="dark", n_clicks_timestamp=0),
            dbc.Button("Export graph config 2", id="export_graph2",
                       color="dark", n_clicks_timestamp=0),
        ]),
    ], className="export_graphs_card"),

    # When a graph is exported, notify the user
    dbc.Modal([
        dbc.ModalHeader("Graph exports:"),
        dbc.ModalBody("Nothing exported yet", id="modal_export_text"),
        dbc.ModalFooter(
            dbc.Button("Close", id="close_export_graph", className="ml-auto")
        )
    ], id="modal_export_graph"),
]

Sidebar = []


@app.callback([Output("xvars_2d", "options"),
               Output("yvars_2d", "options"),
               Output("yvars_2d", "multi")],
              [Input("dataset_choice_2d", "value"),
               Input("graph_choice_exploration", "value")],
              [State("user_id", "children")])
def render_variable_choices_2d(dataset_choice, graph_choice_exploration,
                               user_id):
    """
    Create a menu of dcc components for the user to choose
    plotting options.

    Args:
        dataset_choice (str): Name of dataset.
        graph_choice_exploration (str): The choice of graph type.
        user_id (str): Session/user id.

    Returns:
        [list(dict), list(dict), bool]: Key-value pairs to be input
                                        as `dcc.Dropdown` options and
                                        a boolean to indicate whether
                                        the graph needs a y-variable.

    Notes on implementation:
        These options should also take into account the datasets.
    """

    df = get_data(dataset_choice, user_id)

    # Make sure all variables have a value before returning choices
    if any(x is None for x in [df, dataset_choice,
                               graph_choice_exploration]):
        return [[], [], False]

    options = [{'label': col[:35], 'value': col} for col in df.columns]

    needs_yvar, allows_multi = graphs2d.graph_configs[graph_choice_exploration]
    
    return [options, options if needs_yvar else [], allows_multi]


@app.callback(
    [Output("graph_2d", "figure"),
     Output("yvars_2d", "disabled")],
    [Input("xvars_2d", "value"),
     Input("yvars_2d", "value"),
     Input("graph_choice_exploration", "value")],
    [State("user_id", "children"),
     State("dataset_choice_2d", "value")])
def plot_graph_2d(xvars, yvars, graph_choice_exploration,
                  user_id, dataset_choice):
    """
    Plot the graph according to user choices.

    Args:
        xvars (str): `x-axis` of the graph.
        yvars (str or list(str)): `y-axis`, can be multiple depending
                                  on graph type.
        graph_choice_exploration (str): The choice of graph type.
        user_id (str): Session/user id.
        dataset_choice (str): Name of dataset.

    Returns:
        [dict, bool]: A dictionary holding a plotly figure including
                      layout and a boolean to indicate whether a Y
                      variable is needed.
    """

    df = get_data(dataset_choice, user_id)

    # Make sure all variables have a value before moving further
    test_conditions = [xvars, df, dataset_choice, graph_choice_exploration]
    if any(x is None for x in test_conditions):
        return [{}, True]

    needs_yvar, allows_multi = graphs2d.graph_configs[graph_choice_exploration]

    # Also, if we needs_yvar and they are empty, return.
    if needs_yvar and yvars is None:
        return [{}, False]

    # Fix bugs occurring due to Dash not ordering callbacks
    if not allows_multi and isinstance(yvars, list):
        yvars = yvars[0]
    elif allows_multi and isinstance(yvars, str):
        yvars = [yvars]

    # Graph choices
    if graph_choice_exploration == 'line_chart':
        traces = [graphs2d.line_chart(df[xvars], df[yvar], name=yvar)
                  for yvar in yvars]

    elif graph_choice_exploration == 'scatterplot':
        traces = [graphs2d.scatterplot(df[xvars], df[yvar], name=yvar)
                  for yvar in yvars]

    elif graph_choice_exploration == 'histogram':
        traces = [graphs2d.histogram(df[xvars])]

    elif graph_choice_exploration == 'heatmap':
        traces = [graphs2d.heatmap(df[xvars], df[yvars])]

    elif graph_choice_exploration == 'bubble_chart':
        size = [20, 40, 60, 80, 100, 80, 60, 40, 20, 40]
        traces = [graphs2d.bubble_chart(df[xvars], df[yvar], size, name=yvar)
                  for yvar in yvars]

    elif graph_choice_exploration == 'pie':
        traces = [go.Pie(labels=df[xvars], values=df[yvars])]

    elif graph_choice_exploration == 'filledarea':
        traces = [graphs2d.filledarea(df[xvars], df[yvar], name=yvar)
                  for yvar in yvars]

    elif graph_choice_exploration == 'errorbar':
        traces = [graphs2d.errorbar(df[xvars], df[yvar], name=yvar)
                  for yvar in yvars]

    elif graph_choice_exploration == 'density2d':
        traces = graphs2d.density2d(df[xvars], df[yvars], name=yvars)

    elif graph_choice_exploration == 'pairplot':
        # We need more than 1 variable for a pairplot
        if len(yvars) >= 1:
            # This returns a whole figure, not a trace
            return graphs2d.pairplot(df[[xvars]+yvars]) + [not needs_yvar]
        else:
            traces = []
    else:
        traces = []

    return [{
        'data': traces,
        'layout': layouts.default_2d(xvars, ""),
    }, not needs_yvar]


@app.callback([Output("modal_export_graph", "is_open"),
               Output("modal_export_text", "children")],
              [Input("close_export_graph", "n_clicks")]+[
               Input(f"export_graph{exported_figure}", "n_clicks_timestamp")
               for exported_figure in range(1, 3)],
              [State("modal_export_graph", "is_open"),
               State("graph_2d", "figure")])
def toggle_modal(close, *args):
    """
    Notify when a graph is exported.

    Args:
        close (int): Number of times the close button was clicked.
        *args (multiple): Timestamps for export button clicks, whether
                          the modal is open, and the figure instance.

    Notes on implementation:
        Since the export buttons may increase in number we cannot avoid
        the *args parameter. Sadly, this *args has to contain other parts
        too, since dash `State`s must always be at the end.

    Returns:
        [bool, str or html element]: Whether to open/close the modal
                                     and the text (or html) displayed.
    """

    graph1, graph2, is_open, figure = args

    # TODO: Maybe return a better message?
    if close or graph1 or graph2:
        if graph1 > graph2 and figure:
            text = "Exported configurations as graph 1"
        elif graph2 > graph1 and figure:
            text = "Exported configurations as graph 2"
        else:
            text = "Nothing exported yet"

        return [not is_open, text]

    return [is_open, "Nothing exported yet."]


# Create callbacks for every figure we need saved
for exported_figure in range(1, 3):
    @app.callback(Output(f"saved_graph_configs{exported_figure}", "figure"),
                  [Input(f"export_graph{exported_figure}", "n_clicks")],
                  [State("graph_2d", "figure")])
    def export_graph_callback(n_clicks, figure):
        """
        Export a graph (to a hidden div). One for every hidden graph.

        Args:
            n_clicks (int): Number of clicks for each respective button.
            figure (dict): The figure parameters to be exported.

        Returns:
            dict: the figure is exported to the hidden div.
        """

        if (n_clicks is not None) and (n_clicks >= 1) and (figure is not None):
            return figure
        else:
            return {}
