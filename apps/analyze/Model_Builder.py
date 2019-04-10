"""
    This module will be used to graphically create models.
    RapidMiner, Weka, Orange, etc, ain't got sh!t on us :)

    You should probably not write code here.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto

from server import app, DEBUG
from utils import r, create_dropdown

import re
import random
from itertools import combinations
import plotly.graph_objs as go
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.linear_model import LinearRegression

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBClassifier
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler


def ever_incrasing_ids():
    i = 1
    while True:
        yield i
        i += 1

        ## This probably needs work, but I leave it here for
        ## development. We need to force the user to not abuse the
        ## node system or else the browser might get overburdened
        if i > 200 and DEBUG:
            raise StopIteration

class InputFile(LinearRegression):
    def fit(self):
        raise NotImplementedError

    def transform(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError


class DataCleaner(InputFile):
    pass

class DataImputater(InputFile):
    pass

class TwitterAPI(InputFile):
    pass


def make_options(label, func):
    return {"label": label, "func": func}

# problem_type: id, label, class
models = {
    "models": {
        "logr": make_options("Logistic Regression", LogisticRegression),
        "xgb": make_options("XGBoost Classifier", XGBClassifier),

        "linr": make_options("Linear Regression", LinearRegression),
        "dtr": make_options("Decision Tree Regression", DecisionTreeRegressor),
        "svr": make_options("Support Vector Regression", SVR),

        "kmc": make_options("K-Means Clustering", KMeans),
        "dbscan": make_options("DBSCAN", DBSCAN),
    },

    "input": {
        "file_node": make_options("File reader", InputFile),
        "twitter_node": make_options("Twitter API", TwitterAPI),

    },

    "cleaning": {
        "cleaner_node": make_options("Data Cleaner", DataCleaner),
        "imputer_node": make_options("Data Imputation", DataImputater)
    },

    "preprocessing": {
        "stdsc": make_options("Standardization", StandardScaler),
    },

    "utils": {
        "union": make_options("Combine data", FeatureUnion),
    }
}

mapping = {v:models[k][v]["func"] for (k,vs) in models.items()
            for v in vs}


children2parent_mapping = {model_cls:problem_type
                           for problem_type in models
                             for model_cls in models[problem_type]}

default_steps = {
    (0, "input", "Input data"): [
        "file_node",
    ],

    (1, "cleaning", "Data cleaning"): [
        "cleaner_node",
    ],

    (2, "preprocessing", "Data transformations"): [
        "stdsc",
    ],

    (3, "models", "Machine Learning Models"): [
        "linr",
    ],
}

orders = {
    "input": 0,
    "cleaning": 1,
    "preprocessing": 2,
    "models": 3,
}

def order_elements(elements):
    return sorted(elements,
                  key=lambda x: orders.get(x["data"].get("parent", 10), 10))


class Graph:

    def __init__(self, steps=default_steps):
        """
            Steps is about having a default pipeline at start. For the
            rest, this class is just about defining the basic layout.
        """

        # ("input", "Input file")
        self.parent_nodes = [{
            "data":{
                "id": key,
                "label": label,
            },
            "position": {"x": order*300, "y": 100},
        } for (order,key,label) in steps]

        # input -> cleaning -> preprocessing -> models
        self.pipeline_edges = [{"data":{
            "id": f"{src}_{dest}",
            "source": src[1],
            "target": dest[1],
        }} for (src,dest) in zip(sorted(steps)[:-1], sorted(steps)[1:])]

        # Add items/models within each step
        # This needs work in order to correctly connect steps
        self.graph_nodes = []

        for i, step in enumerate(steps):
            for j, type_ in enumerate(steps[step]):
                self.graph_nodes.append({
                "data":{
                    "id": type_,
                    "label": models[step[1]][type_]["label"],
                    "parent": step[1]
                },
                "position": {"x": orders[step[1]]*300, "y": j*100},
            })


    def render_graph(self):
        return self.graph_nodes + self.parent_nodes + self.pipeline_edges

    @staticmethod
    def create_node(node_id, height):
        parent = children2parent_mapping[node_id]

        return {
            "data": {
                "id": node_id,
                "label": models[parent][node_id]["label"],
                "parent": parent,
            },
            "position": {"x": orders[parent]*300, "y": height*100},
        }


# initial graph
G = Graph()


Model_Builder_Layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-graph',
        layout={'name': "preset"},
        style={"width":"100%", "height":"600px"},
        elements=G.render_graph()[::-1],
    ),
    html.Div(id="output_div", children=[

        html.Div([
            html.Button("Remove a node", id="remove_node"),
            dcc.Dropdown(options=[{"value": elem["data"]["id"],
                                   "label": elem["data"]["label"]+elem["data"]["id"][-3:]}
                                  for elem in G.graph_nodes],
                         className="eight columns",
                         id="delete_options"),
        ], className="three columns", style={"display":"inline-block"}),

        html.Div([
            html.Button("Add a new node", id="add_node"),
            dcc.Dropdown(options=[{"value": model_cls,
                                   "label": models[children2parent_mapping[model_cls]][model_cls]["label"]}
                                  for model_cls in children2parent_mapping],
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

        num_same_parent = len([elem for elem in elems
                if elem["data"].get("parent", 0) == children2parent_mapping[add_node_type]])

        new_node = Graph.create_node(add_node_type, height=num_same_parent)
        elems.append(new_node)

        # TODO: THIS PROBABLY NEEDS A BETTER IMPLEMENTATION
        # THAN HAVING A GENERATOR IN THE GLOBAL SCOPE.
        return elems

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
              [Input("cytoscape-graph", "elements")],
              [State("cytoscape-graph", "layout")])
def inspect_node(elements, layout):

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

        ordered_elements = order_elements(elements)
        for g in ordered_elements:
            if any(g["data"].get("id", "<UKN>").startswith(x)
                   for x in mapping.keys()):
                clean_key = re.split("\d+", g["data"]["id"])[0]

                pipeline_steps.append((g["data"]["id"], mapping[clean_key]()))


        pipeline = Pipeline(pipeline_steps)

        return [
            html.P(str(pipeline)),
        ] + [
            html.H4(step[0]) for step in pipeline.steps
        ]
