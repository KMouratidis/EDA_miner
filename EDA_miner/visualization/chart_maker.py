"""
This module defines the available graphs and creates the interface \
for the 2D dashboard.

Global Variables:
    - Sidebar: To be used for creating side-menus.

Functions:
    - Exploration_Options: Generate the layout of the dashboard.
    - make_trace: Create a plotly trace (plot element).
    - make_trace_menu: Helper function to create modals and trace menus.

Dash callbacks:
    - plot: Plot the graph according to user choices.
    - render_variable_choices: Update menu of dcc components for the user \
                               to choose plotting options.
    - toggle_modal: Open/close the modal for choosing a graph type, per trace.
    - update_graph_choice: Update the value (plot choice) of the respective \
                           button and its label.
    - dummy_add_trace: Show ("add") or hide ("remove") traces windows.
    - toggle_modal: Notify when a graph is exported.

Notes to others:
    You should only write code here with caution. You can use this \
    module to add new buttons, input, or other interface-related, \
    element, or maybe a new type of graph (in which case implement \
    it in `graphs.graphs2d.py`).
"""

import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc

from .server import app, redis_conn
from utils import create_dropdown, get_variable_options
from .graphs.graphs2d import graph2d_configs
from .graphs.utils import create_button

import dill
from flask_login import current_user


Sidebar = []

max_traces = 7


def make_trace_menu(n):
    """
    Helper function to create modals and trace menus.

    Args:
        n (int): The number/id of trace menu.

    Notes:
        Each trace needs a modal with buttons, a menu for choices, \
        and a callback to update the graph (probably with a "plot" button).
    """

    buttons = []
    for graph_type, (label, *_) in graph2d_configs.items():
        buttons.append(create_button(graph_type, label, n))

    # modal with buttons for graphs
    modal = html.Div([
        dbc.Modal([
            dbc.ModalHeader("Choose a graph type"),
            dbc.ModalBody([
                "2D graphs: ",

                html.Div(buttons)

            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id=f"close_choose_graph_{n}", className="ml-auto")
            )
        ], id=f"modal_choose_graph_{n}")
    ])

    # Traces menus
    div = html.Div([

        # Menu header
        html.Div([
            html.P(f"trace {n}", className="trace-title-text"),
        ], className="trace-title"),

        # Available buttons and choices for plotting
        # Holds the name AND opens a modal for graph selection
        html.Div([
            html.Div("Type", className="trace-variable-name"),
            html.Button("Scatterplot", value="scatterplot",
                        id=f"graph_choice_{n}", n_clicks=0,
                        className="plot-menu-input-button"),
        ], className="trace-menu-row"),

        # Available variable choices
        html.Div(create_dropdown("X", options=[], type_="trace",
                                 multi=False, id=f"xvars_{n}"),
                 className="plot-menu-input-div"),

        html.Div(create_dropdown("Y", options=[],  type_="trace",
                                 multi=False, id=f"yvars_{n}"),
                 className="plot-menu-input-div"),

        # Z-vars are not always needed, so keep them disabled and hidden
        html.Div(create_dropdown("Z", options=[], disabled=True, type_="trace",
                                 multi=False, id=f"zvars_{n}"),
                 className="plot-menu-input-div",
                 style={"display": "none"}, id=f"z_vars_div_{n}"),

    ], style={"display": "none"}, id=f"trace_{n}", className="trace-container")

    return modal, div


def Exploration_Options(options):
    """
    Generate the layout of the dashboard.

    Args:
        options (list(dict)): Available datasets as options for `dcc.Dropdown`.

    Returns:
        Two divs with Dash elements or lists of elements.
    """

    modals, divs = list(zip(*[make_trace_menu(x)
                              for x in range(1, max_traces+1)]))

    return [
        # The main content
        html.Div(dcc.Graph(id="graph"), className="main-content-graph"),

        # The tab menu
        html.Div([

            html.Div([

                html.Button("Add trace", id="add_trace", n_clicks=0),
                html.Button("Remove trace", id="remove_trace", n_clicks=0),

                html.Br(),
                html.Br(),
                dcc.Input(id="export_graph_name", placeholder="Graph name..."),
                html.Button("Export graph as...", id="export_graph", n_clicks=0),
                html.Div(id="export_throwaway_div", style={"display": "none"}),

                html.Div(modals, id="modals"),

                # Choose a dataset
                html.Div(create_dropdown("Available datasets", options,
                                         multi=False, id="dataset_choice")),

                # The variable choices
                html.Div([
                    *divs
                ], id="traces", className="traces-list"),

                html.Div(id="traces_maker"),
                # This is here to count the children
                html.Div(0, id="hidden_div", style={"display": "none"}),

            ], id="chartmaker_menu")
        ])
    ]


@app.callback(Output("export_throwaway_div", "children"),
              [Input("export_graph", "n_clicks")],
              [State("export_graph_name", "value"),
               State("graph", "figure")])
def export_graph(n_clicks, name, figure):
    if not (name and figure):
        raise PreventUpdate()

    redis_conn.set(f"{current_user.username}_figure_{name}", dill.dumps(figure))

    return [f"Graph {name} exported successfully"]


# For as many traces as are allowed, create their respective callbacks
for n in range(1, max_traces+1):

    # When the button (or graph buttons) is clicked, open/close the modal
    @app.callback(Output(f"modal_choose_graph_{n}", "is_open"),
                  [Input(f"graph_choice_{n}", "n_clicks"),
                   Input(f"close_choose_graph_{n}", "n_clicks")] + [
                      Input(graph_type + f"_{n}", "n_clicks")
                      for graph_type in graph2d_configs.keys()
                  ],
                  [State(f"modal_choose_graph_{n}", "is_open")])
    def toggle_modal(n1, n2, *rest):
        """
        Open/close the modal for choosing a graph type, per trace.

        Args:
            n1 (int): Number of button clicks, graph selection button.
            n2 (int): Number of button clicks, close menu button.
            *rest (list(int)): Number of button clicks, for all graph types \
                               for all traces.

        Returns:
            bool: Whether to open or close the modal.
        """

        *rest, is_open = rest

        if n1 or n2:
            return not is_open

        return is_open


    @app.callback([Output(f"graph_choice_{n}", "children"),
                   Output(f"graph_choice_{n}", "value"),
                   Output(f"z_vars_div_{n}", "style"),
                   Output(f"zvars_{n}", "disabled")],
                  [Input(graph_type + f"_{n}", "n_clicks")
                   for graph_type in graph2d_configs.keys()])
    def update_graph_choice(*inputs):
        """
        Update the value (plot choice) of the respective button and its label.

        Args:
            *inputs: The different plots (icons) for all shown/hidden traces \
                     for every graph type (total: max_traces * graph_types).

        Returns:
            list(str): The label and value of the various buttons, per \
                       trace menu.
        """

        if all(x is None for x in inputs):
            raise PreventUpdate()

        triggered = dash.callback_context.triggered[0]["prop_id"]
        triggered_id = triggered.split(".")[0]
        # [:-2] to discard n
        graph_type = triggered_id[:-2]

        # Get configuration for the graph choice
        (graph_name, needs_yvar, allows_multi,
         needs_zvar, func) = graph2d_configs[graph_type]

        disabled_z = not needs_zvar
        display_z = "none" if disabled_z else "block"

        return [graph2d_configs[graph_type][0], graph_type,
                {"display": display_z}, disabled_z]


    @app.callback([Output(f"xvars_{n}", "options"),
                   Output(f"yvars_{n}", "options"),
                   Output(f"zvars_{n}", "options")],
                  [Input("dataset_choice", "value")])
    def render_variable_choices(dataset_choice):
        """
        Update menu of dcc components for the user to choose plotting options.

        Args:
            dataset_choice (str): Name of the dataset.

        Returns:
            list(list(dict)): Variable options passed to `dcc.Dropdown`.
        """

        if dataset_choice is None:
            return [[]] * 3

        options = get_variable_options(dataset_choice, redis_conn)

        return [options] * 3


@app.callback([Output(f"trace_{n}", "style")
               for n in range(1, max_traces+1)] + [
                Output("hidden_div", "children")],
              [Input("add_trace", "n_clicks"),
               Input("remove_trace", "n_clicks")],
              [State("hidden_div", "children")])
def dummy_add_trace(add_trace, remove_trace, n_children):
    """
    Show ("add") or hide ("remove") traces windows.

    Args:
        add_trace (int): Number of button clicks.
        remove_trace (int): Number of button clicks.
        n_children (int): Number of traces currently showing.

    Returns:
        list(dict): The styles (i.e. shown/hidden) of the trace menus.
    """

    triggered = dash.callback_context.triggered[0]["prop_id"]
    triggered_id = triggered.split(".")[0]

    if triggered_id == "remove_trace":
        # "Close" the last one
        n_children -= 2

    if add_trace > 0:
        styles = []
        for _ in range(1, n_children + 2):
            styles.append({"display": "block"})

        for _ in range(n_children + 2, max_traces+1):
            styles.append({"display": "none"})

        if len(styles) > max_traces:
            print("Reached the limit!")
            raise PreventUpdate()

        return [*styles, n_children + 1]

    else:
        raise PreventUpdate()


@app.callback(Output("graph", "figure"),
              [Input("hidden_div", "children")]+[
               Input(f"graph_choice_{n}", "value")
               for n in range(1, max_traces+1)]+[
                  Input(f"xvars_{n}", "value")
                  for n in range(1, max_traces+1)]+[
                  Input(f"yvars_{n}", "value")
                  for n in range(1, max_traces+1)]+[
                  Input(f"zvars_{n}", "value")
                  for n in range(1, max_traces+1)]+[
                  Input("dataset_choice", "value")])
def plot(*params):
    """
    Plot the graph according to user choices.

    Args:
        *params (list): Number of traces, the choices of graph types, the \
                        choices of x variables, the choices of y variables, \
                        and the dataset choice.

    Returns:
        dict: The figure to be plotted.
    """

    *params, dataset_choice = params

    n_children, graph_types, xvars, yvars, zvars = (
        params[0],
        params[1:max_traces+1],
        params[max_traces+1:2*max_traces+1],
        params[2*max_traces+1:3*max_traces+1],
        params[3*max_traces+1:]
    )

    if dataset_choice is None:
        return {}

    # Get the dataset here and pass it to the make_trace
    df = dill.loads(redis_conn.get(dataset_choice))

    traces = []
    # This will iterate only for as many n_children
    for i, graph_type, x_var, y_var, z_var in zip(list(range(n_children)),
                                                  graph_types,
                                                  xvars, yvars, zvars):

        # Get configuration for the graph choice
        (graph_name, needs_yvar, allows_multi,
         needs_zvar, func) = graph2d_configs[graph_type]

        # Conditions necessary to do any plotting
        conditions = [graph_type, x_var]
        if needs_yvar:
            conditions.append(y_var)
        if needs_zvar:
            conditions.append(z_var)
        if any(var is None for var in conditions):
            # When adding new traces, don't send an empty graph
            # Instead, prevent the update
            raise PreventUpdate()

        new_traces = make_trace(graph_type, x_var, y_var, zvar=z_var, df=df)
        traces.extend(new_traces)

    return {
        "data": traces,
        "layout": {}
    }


def make_trace(graph_choice, xvar, yvar, zvar=None, df=None):
    """
    Create a plotly trace (plot element).

    Args:
        graph_choice (str): The type of graph to create.
        xvar (str): `x-axis` of the graph.
        yvar (str): `y-axis`.
        zvar (str): `z-axis`, if applicable.
        df (`pd.DataFrame`): The data to plot.

    Returns:
        list(`plotly.go.*`): Plotly traces.
    """

    plot_func = graph2d_configs[graph_choice][-1]

    traces = []
    # Graph choices
    if graph_choice in ['line_chart', 'heatmap', 'filledarea', 'errorbar',
                        'density2d', 'barchart', 'scatterplot']:
        traces.append(plot_func(df[xvar], df[yvar], name=yvar))

    elif graph_choice == 'histogram':
        traces.append(plot_func(df[xvar]))

    elif graph_choice == 'bubble_chart':
        size = [20, 40, 60, 80, 100, 80, 60, 40, 20, 40]  # ????
        traces.append(plot_func(df[xvar], df[yvar], size=size, name=yvar))

    elif graph_choice == 'pie':
        labels = df[xvar].unique()
        vals = df.groupby(xvar).count().iloc[:, 0]
        traces.append(plot_func(x=labels, y=vals))

    elif graph_choice == 'scatterplot3d':
        traces.append(plot_func(df[xvar], df[yvar], z=df[zvar]))

    return traces
