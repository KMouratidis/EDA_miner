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
from utils import r
from styles import cyto_stylesheet
from apps.analyze.models import pipeline_creator
# import custom models
from apps.analyze.models.pipeline_classes import TwitterAPI, InputFile
from apps.analyze.models.pipeline_classes import DataCleaner, DataImputater
from apps.analyze.models.pipeline_classes import CustomClassifer

import random
import dill
from itertools import combinations
from xgboost import XGBClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler


orders = {
    "input": 0,
    "cleaning": 1,
    "preprocessing": 2,
    "models": 3,
}

ml_options = [
    # Inputs
    {"label": "Twitter API", "node_type": "twitter_api",
     "parent": "input", "func": TwitterAPI},
    {"label": "Input file", "node_type": "input_file",
     "parent": "input", "func": InputFile},

    # Cleaners
    {"label": "Data Cleaner", "node_type": "data_cleaner",
     "parent": "cleaning", "func": DataCleaner},
    # Preprocessors
    {"label": "Standardization", "node_type": "stdsc",
     "parent": "preprocessing", "func": StandardScaler},

    # models
    {"label": "Linear Regression", "node_type": "linr",
     "parent": "models", "func": LinearRegression},
    {"label": "Logistic Regression", "node_type": "logr",
     "parent": "models", "func": LogisticRegression},
    {"label": "K-Means Clustering", "node_type": "kmc",
     "parent": "models", "func": KMeans},
    {"label": "SVM Regression", "node_type": "svr",
     "parent": "models", "func": SVR},
    {"label": "Decision Tree Regression", "node_type": "dtr",
     "parent": "models", "func": DecisionTreeRegressor},
    {"label": "XGBoost Regression", "node_type": "xgb",
     "parent": "models", "func": XGBClassifier},
]

node_options = {options["node_type"]: options
                for options in ml_options}


class Node:
    """This class just holds data for nodes, nothing else"""
    ## TODO: Consider using slots

    def __init__(self, *, options=None, node_type=None, node_id=None):
        """
            When called with options={} it expects a dictionary
            as the ones returned by cytoscape.
        """

        if (options is None) and (node_type is None):
            raise ValueError("Provide at least one!")
        elif (options is not None) and (node_type is not None):
            raise ValueError("Provide at most one!")

        elif (node_type is not None) and (node_id is not None):
            # no options given, create a default node
            options = node_options[node_type]
            self.id = node_id
            self.func = options["func"]
            self.parent = options["parent"]

        elif options is not None:
            # if the data are nested, get only them
            options = options.get("data", options)
            self.id = options["id"]
            self.func = node_options[options["node_type"]]["func"]
            self.parent = node_options[options["node_type"]]["parent"]

        else:
            raise ValueError("Something went wrong, and we need to investigate")

        self.label = options["label"]

        self.node_type = options["node_type"]
        self.order = orders[self.parent]

        self.options = {"data": {
                            "label": self.label,
                            "node_type": self.node_type,
                            "id": self.id,
                            "parent": self.parent
                        },
                        "position": {
                            'x': 100 + self.order*200,
                            'y': 150 + random.randint(-50, 200)
                        }}

    def render(self):
        return self.options


class NodeCollection:

    # Make them non-selectable so that the user cannot connect
    # a node to a group directly (might be revised later)
    parent_nodes = [
        {"data": {"label": "Inputs", "id": "input"},
         'selectable': False},
        {"data": {"label": "Cleaning", "id": "cleaning"},
         'selectable': False},
        {"data": {"label": "Preprocessing", "id": "preprocessing"},
         'selectable': False},
        {"data": {"label": "Estimators", "id": "models"},
         'selectable': False},
    ]

    def __init__(self, nodes=[], graph=None):
        self.node_max = {node_type: f"{node_type}_000"
                           for node_type in node_options}
        self.nodes = []
        self.graph = graph

        # If nodes are given, parse them into an internal
        # representation and increase the relevant counts
        # (nodes originally are dictionaries of attributes)
        for n in nodes:
            node = Node(options=n)

            # keep the maximum id (e.g. 'linr_002')
            self.node_max[node.node_type] = max(self.node_max[node.node_type],
                                                   node.id)

            self.nodes.append(node)

    def add_node(self, node_type):
        # Generate the ID based on previous max
        max_id = self.node_max[node_type]
        node_id = f"{node_type}_{str(int(max_id[-3:]) + 1).zfill(3)}"

        new_node = Node(node_type=node_type, node_id=node_id)
        self.nodes.append(new_node)

    def remove_node(self, node_id):
        to_be_removed = [n for n in self.nodes if n.id == node_id]
        self.nodes.remove(to_be_removed[0])

        # Also removed edges that this node is connected to (but don't)
        # reconnect, let the user do it (for now at least)
        self.graph.edge_collection.edges = [
            edge for edge in self.graph.edge_collection.edges
            if ((to_be_removed[0].id != edge["data"]["source"]) and
                (to_be_removed[0].id != edge["data"]["target"]))]

    def render(self):
        return [node.render() for node in self.nodes] + self.parent_nodes


class EdgeCollection:
    def __init__(self, edges=[], graph=None):
        self.edges = edges
        self.graph = graph

    def add_edges(self, selected):

        for combination in combinations(selected, 2):
            node1 = Node(options=combination[0])
            node2 = Node(options=combination[1])

            if node1.order == node2.order:
                continue

            elif node1.order > node2.order:
                new_edge = {"data": {
                    "source": node2.id,
                    "target": node1.id
                }}

                self.edges.append(new_edge)

            elif node1.order < node2.order:
                new_edge = {"data": {
                    "source": node1.id,
                    "target": node2.id
                }}

                self.edges.append(new_edge)

    def render(self):
        return self.edges


class Graph:

    def __init__(self, elems):
        edges = [elem for elem in elems if "source" in elem["data"]]
        # Don't add parent nodes, they will be added by default
        nodes = [elem for elem in elems if (("source" not in elem["data"]) and
                                            ("parent" in elem["data"]))]

        self.node_collection = NodeCollection(nodes, self)
        self.edge_collection = EdgeCollection(edges, self)

    def render_graph(self):
        return self.node_collection.render() + self.edge_collection.render()


class GraphUtils:
    """To be used for default layouts"""
    def __init__(self, steps):
        self.G = Graph([])
        for step in steps:
            self.G.node_collection.add_node(step[1])
        for s1, s2 in zip(self.G.node_collection.nodes[:-1],
                          self.G.node_collection.nodes[1:]):
            self.G.edge_collection.add_edges([s1.render(), s2.render()])

    def render_graph(self):
        return self.G.render_graph()


# Layout definition for the initial setup
default_steps = [
    (0, "input_file", "Input data"),
    (1, "data_cleaner", "Data cleaning"),
    (2, "stdsc", "Standardization"),
    (3, "linr", "Linear Regression")
]

initial_graph = GraphUtils(default_steps).render_graph()


Model_Builder_Layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-graph',
        layout={'name': "preset"},
        style={"width": "95%", "height": "600px"},
        elements=initial_graph,
        stylesheet=cyto_stylesheet,
    ),

    html.Div(id="output_div", children=[

        html.Div([
            html.Button("Remove a node", id="remove_node",
                        n_clicks_timestamp=0,),
            dcc.Dropdown(options=[{"value": elem["data"]["id"],
                                   "label": elem["data"]["label"]}
                                  for elem in initial_graph[:-3]],
                         className="eight columns",
                         id="delete_options"),
        ], className="three columns", style={"display": "inline-block"}),

        html.Div([
            html.Button("Add a new node", id="add_node",
                        n_clicks_timestamp=0,),
            dcc.Dropdown(options=[{"label": option["label"],
                                   "value": option["node_type"]}
                                  for option in ml_options],
                         className="eight columns",
                         id="ml_options"),
        ], className="three columns", style={"display": "inline-block"}),

        html.Div([
            html.Button("Connect selected nodes",
                        n_clicks_timestamp=0,
                        id="connect_selected_nodes"),
        ], className="three columns", style={"display": "inline-block"}),

        html.Div([
            html.Button("Convert to model",
                        id="convert"),
            html.Div(id="model_specs"),
        ], className="three columns", style={"display": "inline-block"}),

    ], className="row"),
    html.Div(id="inspector"),
])


@app.callback(Output("cytoscape-graph", "elements"),
              [Input("remove_node", "n_clicks_timestamp"),
               Input("add_node", "n_clicks_timestamp"),
               Input("connect_selected_nodes", "n_clicks_timestamp")],
              [State("cytoscape-graph", "elements"),
               State("ml_options", "value"),
               State("delete_options", "value"),
               State("cytoscape-graph", "selectedNodeData")])
def modify_graph(remove_clicked_time, added_clicked_time, connect_selected_time,
                 elems, add_node_type, to_be_deleted, selected):

    if all(x is None for x in [remove_clicked_time, added_clicked_time,
                               connect_selected_time]):
        if elems is not None:
            return elems
        else:
            return []

    G = Graph(elems)

    # Sort buttons based on clicked time (most recent first)
    buttons_and_clicks = sorted([
        (remove_clicked_time, "remove"),
        (added_clicked_time, "add"),
        (connect_selected_time, "connect")
    ], reverse=True)

    # Graph operations
    if buttons_and_clicks[0][1] == "remove":
        G.node_collection.remove_node(to_be_deleted)

    elif buttons_and_clicks[0][1] == "add":
        G.node_collection.add_node(add_node_type)

    elif buttons_and_clicks[0][1] == "connect":
        G.edge_collection.add_edges(selected)

    return G.render_graph()


@app.callback(Output("inspector", "children"),
              [Input("cytoscape-graph", "mouseoverNodeData")],
              [State("user_id", "children")])
def inspect_node(selected, user_id):
    return [
        html.Br(),
        html.Pre(str(selected))
    ]


@app.callback(Output("delete_options", "options"),
              [Input("cytoscape-graph", "elements")],
              [State("user_id", "children")])
def inspect_node(elements, user_id):
    return [{
        "value": elem["data"]["id"],
        "label": elem["data"]["label"]
        } for elem in elements if elem["data"].get("source") is None]


@app.callback(Output("model_specs", "children"),
              [Input("convert", "n_clicks")],
              [State("cytoscape-graph", "elements"),
               State("cytoscape-graph", "stylesheet"),
               State("user_id", "children")])
def convert_model(n_clicks, elements, layout, user_id):

    if user_id.startswith("python_generated_ssid"):
        # Trim id
        user_id = user_id.split("-")[-1]

    if n_clicks is None:
        return [html.H5("No specs defined yet")]

    else:
        # Keep elements that are either edges (have a source)
        # or elements that have a parent (nodes, not groups)
        elements = [elem for elem in elements if (("source" in elem["data"]) or
                                                  ("parent" in elem["data"]))]

        pipelines, classifiers = pipeline_creator.create_pipelines(elements,
                                                                   node_options)

        # Save pipelines to Redis (to be used in other modules)
        for pipe, clf in zip(pipelines, classifiers):
            r.set(f"{user_id}_pipeline_{clf}", dill.dumps(pipe))

        return [html.P(str(pipeline)) for pipeline in pipelines]
