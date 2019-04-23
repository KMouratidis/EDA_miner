"""
    This module will be used to show network data.

    You can write code in this module, but keep in
    mind that it may be moved later on to lower-level
    modules.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

import dash_cytoscape as cyto

from server import app
from utils import r, create_dropdown
from apps.data.View import get_data

from itertools import chain


def Network_Options(options, results):

    return html.Div(children=[

        html.Div([
            # Choose a dataset
            html.Div(create_dropdown("Available datasets", options,
                                     multi=False, id="dataset_choice_network"),
                     className="vertical_dropdowns"),

            # Available buttons and choices for plotting
            html.Div(create_dropdown("In-node", options=[],
                                     multi=False, id="in_node"),
                     className="vertical_dropdowns"),
            html.Div(create_dropdown("Out-node", options=[],
                                     multi=False,
                                     id="out_node"),
                     className="vertical_dropdowns"),
            html.Div(create_dropdown("Layout", id='dropdown-callbacks-1',
                                     value='grid', multi=False,
                                     clearable=False,
                                     options=[
                                         {'label': name,
                                          'value': name}
                                         for name in ['grid', 'random',
                                                      'circle', 'concentric',
                                                      'cose']
                                     ]),
                     className="vertical_dropdowns")

        ], className="col-sm-3"),

        # The graph itself
        html.Div([
            cyto.Cytoscape(
                id='cytoscape_network_graph',
                layout={'name': 'preset'},
                style={'width': '100%', 'height': '700px'},
                elements=[
                    {'data': {'id': 'one', 'label': 'Example Node 1'},
                     'position': {'x': 75, 'y': 75}},
                    {'data': {'id': 'two', 'label': 'Example Node 2'},
                     'position': {'x': 200, 'y': 200}},
                    {'data': {'source': 'one', 'target': 'two'}}
                ]
            ),

        ], className="col-sm-9"),
    ], className="row")




@app.callback([Output("in_node", "options"),
               Output("out_node", "options")],
              [Input("dataset_choice_network", "value")],
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

    return [options, options]


@app.callback([Output("cytoscape_network_graph", "elements"),
               Output('cytoscape_network_graph', 'layout')],
              [Input("in_node", "value"),
               Input("out_node", "value"),
               Input('dropdown-callbacks-1', 'value')],
              [State("user_id", "children"),
               State("dataset_choice_network", "value")])
def plot_network(innode, outnode, layout_choice, user_id,
                 dataset_choice_network):
    """
        This callback takes all available user choices and, if all
        are present, it returns the appropriate plot.
    """

    if any(x is None for x in [innode, outnode, layout_choice,
                               dataset_choice_network]):
        raise PreventUpdate

    # This doesn't seem to be able to handle more than 100
    # https://github.com/cytoscape/cytoscape.js/issues/858
    # TODO: Consider adding clustering
    df = get_data(dataset_choice_network, user_id).sample(n=100)

    node_list = []
    for node in chain(df[innode].values, df[outnode].values):
        node_list.append({"data": {
            "id": node, "label": node,
        }})

    edge_list = []
    for i, row in df[[innode, outnode]].iterrows():
        edge_list.append({"data": {
            "source": row[innode], "target": row[outnode],
        }})

    # TODO: consider coloring nodes based on in/out-nodes
    return [node_list + edge_list, {'name': layout_choice}]
