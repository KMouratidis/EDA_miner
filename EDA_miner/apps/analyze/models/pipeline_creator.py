"""
This module collects function to traverse the ModelBuilder graph.

Functions:
    - create_pipelines: Create pipelines from cytoscape elements and a \
                        dict that maps a node type to relevant parameters.
    - find_pipeline_input: Given a goal creates a function that searches \
                           a pipeline for nodes of that type (or its \
                           subclasses). Essentially goes the reverse way \
                           of `create_pipelines`.

Notes to others:
    Feel free to add or modify stuff here, but be cautious. You probably \
    need experience with graphs and/or trees and traversal algorithms. \
    The current implementation (unless I'm mistaken) are Breadth-First.
"""

import networkx as nx
from sklearn.pipeline import Pipeline, FeatureUnion
from apps.analyze.models import pipeline_classes, graph_structures


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


def create_pipelines(data, node_options):
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

        # Get the default params for the model (we want this because we
        # want to set the defaults at the server-side).
        default_node_params = {}
        for param, options in node_info["func"].modifiable_params.items():
            default_node_params[param] = options[0]

        # Update the defaults with the given params
        default_node_params.update(**node["data"]["func_params"])
        # Save it to the mapper
        mapper[node["data"]["id"]] = node_info["func"](**default_node_params)

    for edge in edges:
        G.add_edge(edge["data"]["source"], edge["data"]["target"])

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
        """Find the input node of the graph"""

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


def find_input_node(elems):
    elements = [elem for elem in elems if (("source" in elem["data"]) or
                                           ("parent" in elem["data"]))]

    pipelines, _ = create_pipelines(elements, graph_structures.node_options)

    current_pipeline = None
    for pipe in pipelines:
        feature_node = find_pipeline_node(
            pipeline_classes.FeatureMaker
        )(pipe)

        if feature_node is not None:
            current_pipeline = pipe
            break

    return find_pipeline_node(
        pipeline_classes.BaseInput
    )(current_pipeline)