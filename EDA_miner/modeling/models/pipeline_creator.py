"""
This module collects function to traverse the ModelBuilder graph.

Functions:
    - create_pipelines: Create pipelines from cytoscape elements and a \
                        dict that maps a node type to relevant parameters.
    - find_pipeline_node: Given a goal creates a function that searches a \
                          pipeline for nodes of that type (or its \
                          subclasses). Essentially goes the reverse way \
                          of `create_pipelines`.
    - find_input_node: Find the input node of a pipeline containing \
                       a `FeatureMaker`.

Notes to others:
    Feel free to add or modify stuff here, but be cautious. You probably \
    need experience with graphs and/or trees and traversal algorithms. \
    The current implementation (unless I'm mistaken) are Breadth-First.
"""

import networkx as nx
from sklearn.pipeline import Pipeline, FeatureUnion


def _traverse_graph(curr_node, G, mapper):
    parents = list(G.predecessors(curr_node))

    if len(parents) == 0:
        return mapper[curr_node]
    else:
        # TODO: Maybe skip the FeatureUnion if `len(parents)==1` ?
        return Pipeline([
            ("union", FeatureUnion([
                (f"{name}", _traverse_graph(name, G, mapper))
                for name in parents
                if name in mapper
            ])),
            (curr_node, mapper[curr_node])
        ])


def create_pipelines(graph):
    """
    Create pipelines from cytoscape elements and a dict that maps a node \
    type to relevant parameters.

    Args:
        data (list(dict)): Cytoscape elements.
        node_options (dict): Parameters to be passed at the classes as \
                             they are instantiated for the pipeline(s).

    Returns:
        list, list: The pipelines and the terminal nodes.

    Notes on implementation:
        This uses networkx for easier traversal. Feel free to implement \
        your own travel if you want to.
    """

    G = nx.DiGraph()
    terminal_nodes = []

    edges = graph.edge_collection.edges
    nodes = graph.node_collection.nodes

    mapper = {}
    for node in nodes:
        G.add_node(node.id)
        # From each of these we will start a reverse search to construct the
        # pipeline. We check to see if the node is a model (in contrast to
        # transformers, input, etc)
        if node.parent == "models":
            terminal_nodes.append(node.id)

        # Instantiate the model and save it to the mapper
        mapper[node.id] = node.model_class(**node.params)

    for edge in edges:
        G.add_edge(edge.src_node.id, edge.dest_node.id)

    pipelines = []
    for terminal_node in terminal_nodes:
        pipelines.append(_traverse_graph(terminal_node, G, mapper))

    return pipelines, terminal_nodes


# TODO: THIS MIGHT NOT WORK CORRECTLY IF MORE THAN ONE PIPELINES ARE
#       SIMULTANEOUSLY DEFINED. THIS PROBABLY NEEDS AN EXTRA SENTINEL.
def find_pipeline_node(GOAL):
    """
    Given a goal creates a function that searches a pipeline for nodes of \
    that type (or its subclasses). Essentially goes the reverse way of \
    `create_pipelines`.

    Args:
        GOAL (sklearn-like class): Stopping criteria / node for the recursion.

    Returns:
        The node of type `GOAL`, if found, else `None`.
    """

    def _find_pipeline_input(pipe):

        # TODO: This needs a better / cleaner implementation
        if isinstance(pipe, Pipeline):
            steps = [step[1] for step in pipe.steps]

        elif isinstance(pipe, FeatureUnion):
            steps = [transformer[1] for transformer in pipe.transformer_list]
        else:
            if isinstance(pipe, GOAL):
                return pipe

            steps = []

        for step in steps:
            ret = _find_pipeline_input(step)
            if isinstance(ret, GOAL):
                return ret

    return _find_pipeline_input
