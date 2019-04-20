"""
    TBW...
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from sklearn.pipeline import Pipeline, FeatureUnion
import json


def _traverse_graph(curr_node, G, mapper):
    parents = list(G.predecessors(curr_node))

    if len(parents) == 0:
        return mapper[curr_node]
    else:
        return Pipeline([
            ("union", FeatureUnion([
                (f"name_{name}", _traverse_graph(name, G, mapper))
                for name in parents
                if name in mapper
            ])),
            (curr_node, mapper[curr_node])
        ])


def create_pipelines(data, node_options):
    """
        This function takes the data from the cytoscape graph and the node
        options (dicts as in `Model_Builder.py`) and returns a list of
        sklearn pipelines along with their terminal nodes. This uses
        networkx for easier traversal.
    """

    G = nx.DiGraph()
    terminal_nodes = []

    edges = [elem for elem in data if "source" in elem["data"]]
    nodes = [elem for elem in data if "source" not in elem["data"]]

    mapper = {}
    for node in nodes:
        G.add_node(node["data"]["id"])
        # From each of these we will start a reverse search to construct the
        # pipeline. We check to see if the node is a model (in contrast to
        # transformers, input, etc)
        if node_options[node["data"]["node_type"]]["parent"] == "models":
            terminal_nodes.append(node["data"]["id"])

        node_info = node_options[node["data"]["node_type"]]
        mapper[node["data"]["id"]] = node_info["func"]()

    for edge in edges:
        G.add_edge(edge["data"]["source"], edge["data"]["target"])

    pipelines = []
    for terminal_node in terminal_nodes:
        pipelines.append(_traverse_graph(terminal_node, G, mapper))

    return pipelines, terminal_nodes
