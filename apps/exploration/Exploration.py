"""
    This module defines the available graphs and creates the
    interface for the 2D dashboard. You can use this module
    if you want to add new buttons, input, or other, or maybe
    a new type of graph (in which case also modify graphs2d.py).

    You should only write code here with caution.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
import layouts
import styles
from utils import create_dropdown
from apps.data.View import get_data
from apps.exploration.graphs import graphs2d

import plotly.graph_objs as go


def Exploration_Options(options, results):

    return html.Div(children=[

        # Choose a dataset
        html.Div(create_dropdown("Available datasets", options,
                                 multi=False, id="dataset_choice_2d"),
                 style=styles.dropdown()),

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
                 style=styles.dropdown()),

        # Export graph config
        html.Div([
            html.Button("Export graph config 1", id="export_graph1"),
            html.Button("Export graph config 2", id="export_graph2"),
        ], style=styles.dropdown()),

        # Available buttons and choices for plotting
        html.Div(id="variable_choices_2d", children=[
            html.Div(create_dropdown("X variable", options=[],
                                     multi=False, id="xvars_2d"),
                     style=styles.dropdown()),

            html.Div(create_dropdown("Y variable", options=[],
                                     multi=False,
                                     id="yvars_2d"),
                     style=styles.dropdown()),
        ]),

        # The graph itself
        dcc.Graph(id="graph_2d"),
    ])


@app.callback([Output("xvars_2d", "options"),
               Output("yvars_2d", "options"),
               Output("yvars_2d", "multi")],
              [Input("dataset_choice_2d", "value"),
               Input("graph_choice_exploration", "value")],
              [State("user_id", "children")])
def render_variable_choices_2d(dataset_choice, graph_choice_exploration,
                               user_id):
    """
        This callback is used in order to create a menu of dcc components
        for the user to choose for altering plotting options based on datasets.
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
        This callback takes all available user choices and, if all
        are present, it returns the appropriate plot.
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


# Create callbacks for every figure we need saved
for exported_figure in range(1, 3):
    @app.callback(Output(f"saved_graph_configs{exported_figure}", "figure"),
                  [Input(f"export_graph{exported_figure}", "n_clicks")],
                  [State("graph_2d", "figure")])
    def export_graph_callback(n_clicks, figure):
        if n_clicks is not None and n_clicks >= 1:
            return figure
        else:
            return {}
