"""
    This module will be used to graphically create models.
    RapidMiner, Weka, Orange, etc, ain't got sh!t on us :)

    You should probably not write code here.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto

from server import app
from utils import r, create_dropdown, mapping

import re
import random
from itertools import combinations
import plotly.graph_objs as go
from sklearn.pipeline import Pipeline


def get_position():
    # random position in the range 180-220 for x and y
    return {'x': 200 + (0.5-random.random())*800,
    'y': 200 + (0.5-random.random())*800}


# TODO: Clean this by making rev_ml_options and this dictionaries
# and then create drowdown options in another list (or with a function)
ml_options = [
    {"label": "Input file", "value": "input_node"},
    {"label": "Linear Regression", "value": "linr"},
    {"label": "Standardization", "value": "stdsc"},
    {"label": "Data Cleaner", "value": "data_cleaner"},
    {"label": "Logistic Regression", "value": "logr"},
    {"label": "K-Means Clustering", "value": "kmc"},
    {"label": "Support Vector Machines Regression", "value": "svr"},
    {"label": "Decision Tree Regression", "value": "dtr"},
    {"label": "XGBoost Regression", "value": "xgb"},
]

rev_ml_options = {ml["value"]:ml["label"] for ml in ml_options}


initial_elements = [
    ## Input file(s)
    {
        'data': {
            'id': 'input_node0',
            'label': 'Input file',
        },
        'position': {'x': 50, 'y': 150}
    },

    ## Preprocessor(s)
    {
        'data': {
            "id":"data_cleaner0",
            "label": "Data Cleaner"
        },
        'position': {"x":200, "y": 100},
     },
    {
        'data': {
            "id":"stdsc0",
            "label": "Standardization"
        },
        'position': {"x":200, "y": 200},
     },

    ## Model(s)
    {
        'data': {
            'id': 'linr0',
            'label': 'Linear Regression',
            'parent': 'model'
        },
        'position': {'x': 400, 'y': 150}
    },

    ## Edges
    {"data": {"source":"input_node0", "target":"data_cleaner0"}},
    {"data": {"source":"data_cleaner0", "target":"stdsc0"}},
    {'data': {"source":"stdsc0", "target":"linr0"}},
]


Model_Builder_Layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-graph',
        layout={'name': "preset"},
        style={"width":"90%", "height":"600px"},
        elements=initial_elements,
    ),
    html.Div(id="output_div", children=[

        html.Div([
            html.Button("Remove a node", id="remove_node"),
            dcc.Dropdown(options=[{"value": elem["data"]["id"],
                                   "label": elem["data"]["label"]}
                                  for elem in initial_elements[:-3]],
                         className="eight columns",
                         id="delete_options"),
        ], className="three columns", style={"display":"inline-block"}),

        html.Div([
            html.Button("Add a new node", id="add_node"),
            dcc.Dropdown(options=ml_options,
                         className="eight columns",
                         id="ml_options"),
        ], className="three columns", style={"display":"inline-block"}),


        html.Div([
            html.Button("Connect selected nodes",
                        id="connect_selected_nodes"),
        ], className="three columns", style={"display":"inline-block"}),


        html.Div([
            html.Button("Convert to model",
                        id="convert"),
            html.Div(id="model_specs"),
        ], className="three columns", style={"display":"inline-block"}),


    ], className="row"),

    html.Div(id="inspector"),
])


def ever_incrasing_ids():
    i = 1
    while True:
        yield i
        i += 1

id_generator = ever_incrasing_ids()


@app.callback(Output("cytoscape-graph", "elements"),
              [Input("remove_node", "n_clicks_timestamp"),
               Input("add_node", "n_clicks_timestamp"),
               Input("connect_selected_nodes", "n_clicks_timestamp")],
              [State("cytoscape-graph", "elements"),
               State("ml_options", "value"),
               State("delete_options", "value"),
               State("cytoscape-graph", "selectedNodeData")])
def removeNode(remove_clicked_time, added_clicked_time,
                connect_selected_time,
               elems, add_node_type, to_be_deleted, selected):

    if all(x is None for x in [remove_clicked_time, added_clicked_time,
                               connect_selected_time]):
        if elems is not None:
            return elems
        else:
            return []
    else:
        # TRY ADDING THIS: `n_clicks_timestamp='0'` DEFAULT VALUE
        # TO THE BUTTONS ABOVE TO AVOID ALL THIS TYPE CHECKING
        if remove_clicked_time is None:
            remove_clicked_time = 0
        if added_clicked_time is None:
            added_clicked_time = 0
        if connect_selected_time is None:
            connect_selected_time = 0

    # Sort buttons based on clicked time (most recent first)
    buttons_and_clicks = sorted([
        (remove_clicked_time, "remove"),

        (added_clicked_time, "add"),
        (connect_selected_time, "connect")
    ], reverse=True)


    if buttons_and_clicks[0][1] == "remove":

        if len(elems):
            removed = [elem for elem in elems if elem["data"]["id"]==to_be_deleted][0]
            elems.remove(removed)
        return elems


    elif buttons_and_clicks[0][1] == "add":
        # TODO: THIS PROBABLY NEEDS A BETTER IMPLEMENTATION
        # THAN HAVING A GENERATOR IN THE GLOBAL SCOPE.
        return elems + [{'data': {'id': f"{add_node_type}{next(id_generator)}",
                                  'label': rev_ml_options[add_node_type]}}]

    elif buttons_and_clicks[0][1] == "connect":

        if len(elems) and selected is not None:
            for combination in combinations(selected, 2):
                # Connect all elements with each other
                elems.append({"data":{"source": combination[0]["id"],
                                      "target": combination[1]["id"]}})

        return elems

    else:
        return elems


@app.callback(Output("inspector", "children"),
              [Input("cytoscape-graph", "mouseoverNodeData")])
def inspect_node(selected):
    return [
        html.Br(),
        html.Pre(str(selected))
    ]


@app.callback(Output("delete_options", "options"),
              [Input("cytoscape-graph", "elements")])
def inspect_node(elements):
    return [{
        "value":elem["data"]["id"],
        "label": elem["data"]["label"]
        } for elem in elements if elem["data"].get("source") is None]


@app.callback(Output("model_specs", "children"),
              [Input("convert", "n_clicks")],
              [State("cytoscape-graph", "elements"),
               State("cytoscape-graph", "stylesheet")])
def convert_model(n_clicks, elements, layout):

    if n_clicks is None:
        return [html.H5("No specs defined yet")]

    else:
        pipeline_steps = []

        for g in elements:
            if any(g["data"].get("id", "<UKN>").startswith(x)
                   for x in mapping.keys()):
                clean_key = re.split("\d+", g["data"]["id"])[0]

                pipeline_steps.append((g["data"]["id"], mapping[clean_key]()))

        pipeline = Pipeline(pipeline_steps)

        return [html.P(str(pipeline))]
