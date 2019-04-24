"""
This module is about viewing network data.

Global Variables:
    - Sidebar: To be used for creating side-menus.

Functions:
    - Network_Options: Generate the layout of the dashboard.

Dash callbacks:
    - render_variable_choices_network: Create a menu of dcc components
                                       for the user to choose plotting
                                       options.
    - plot_network: Plot the network graph according to user choices.

Notes to others:
    Contributions are encouraged here, although you should consider
    starting with another part if you're new to dash or this project.
    Main functionality is still lacking in this part. You can use this
    module to add new buttons, input, or other interface-related,
    element, or maybe a new type of graph (in which case implement
    it in a new file `graphs.networks.py`). Like with other modules,
    working on exporting network graphs is encouraged.
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


Sidebar = []


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
def render_variable_choices_network(dataset_choice, user_id):
    """
        Create a menu of dcc components for the user to choose
        plotting options.

    Args:
        dataset_choice (str): Name of dataset.
        user_id (str): Session/user id.

    Returns:
        list(list(dict)): Key-value pairs to be input as
                          `dcc.Dropdown` options.
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
def plot_network(in_node, out_node, layout_choice, user_id,
                 dataset_choice_network):
    """
    Plot the network graph according to user choices.

    Args:
        in_node (str): Column name containing the values of
                      nodes from where links start.
        out_node (str): Column name for nodes where links end.
        layout_choice (str): One of the layouts available in
                             Cytoscape.
        user_id (str): Session/user id.
        dataset_choice_network (str): Name of dataset.

    Returns:
        [list(dict), dict]: A list of elements (dicts for Cytoscape)
                            and the layout for the graph.
    """

    if any(x is None for x in [in_node, out_node, layout_choice,
                               dataset_choice_network]):
        raise PreventUpdate

    # This doesn't seem to be able to handle more than 100
    # https://github.com/cytoscape/cytoscape.js/issues/858
    # TODO: Consider adding clustering
    df = get_data(dataset_choice_network, user_id).sample(n=100)

    node_list = []
    for node in chain(df[in_node].values, df[out_node].values):
        node_list.append({"data": {
            "id": node, "label": node,
        }})

    edge_list = []
    for i, row in df[[in_node, out_node]].iterrows():
        edge_list.append({"data": {
            "source": row[in_node], "target": row[out_node],
        }})

    # TODO: consider coloring nodes based on in/out-nodes
    return [node_list + edge_list, {'name': layout_choice}]
