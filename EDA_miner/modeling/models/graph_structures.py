"""
This module collects function to traverse the ModelBuilder graph.

Functions:
    - create_pipelines: Create pipelines from cytoscape elements and a \
                        dict that maps a node type to relevant parameters.
    - find_pipeline_input:

Classes:
    - Node: A class to hold data for the nodes. Validation and advanced \
            functionality may be added later.

Global variables:
    - ml_options (list(dict)): The available sklearn-like classes for use \
                               with the ModelBuilder.
    - node_options (dict): Reverse mapping of ml_options.
    - orders (dict): The vertical ordering (position) of groups of nodes.

Notes to others:
    Feel free to add or modify stuff here, but be cautious. You probably \
    need experience with graphs and/or trees and traversal algorithms. \
    The current implementation (unless I'm mistaken) are Breadth-First.
"""

from . import pipeline_classes

import random
import numpy as np
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from itertools import combinations
from collections import defaultdict


orders = {
    "input": 0,
    "cleaning": 1,
    "preprocessing": 2,
    "dim_red": 3,
    "models": 4,
}

# TODO: add ensemble models as last-step models (voting, ensembles, etc)
# DO NOT ADD NEURAL NETWORK MODELS YET
ml_options = [
    # Inputs
    {"label": "Input file", "node_type": "input_file",
     "parent": "input", "model_class": pipeline_classes.InputFile,
     "url": "/assets/images/icons/files.png"},

    # Cleaners
    {"label": "Data Cleaner", "node_type": "data_cleaner",
     "parent": "cleaning", "model_class": pipeline_classes.DataCleaner,
     "url": "/assets/images/icons/Cleaning.png"},
    {"label": "Fill missing: impute", "node_type": "simple_missing",
     "parent": "cleaning", "model_class": pipeline_classes.SimpleImputer},
    {"label": "Fill missing: indicator", "node_type": "ind_missing",
     "parent": "cleaning", "model_class": pipeline_classes.MissingIndicator},

    # Preprocessors
    {"label": "Standardization", "node_type": "stdsc",
     "parent": "preprocessing", "model_class": pipeline_classes.StandardScaler},
    {"label": "Bag of Words", "node_type": "bow",
     "parent": "preprocessing", "model_class": pipeline_classes.CountVectorizer},
    {"label": "TF-IDF", "node_type": "tfidf",
     "parent": "preprocessing", "model_class": pipeline_classes.TfidfVectorizer},
    {"label": "Min-Max scaling", "node_type": "minmax_scale",
     "parent": "preprocessing", "model_class": pipeline_classes.MinMaxScaler},
    {"label": "Label Binarizer", "node_type": "lbinarizer",
     "parent": "preprocessing", "model_class": pipeline_classes.LabelBinarizer},

    {"label": "Max-Abs scaling", "node_type": "maxabs_scale",
     "parent": "preprocessing", "model_class": pipeline_classes.MaxAbsScaler},
    {"label": "Binarizer", "node_type": "binarizer",
     "parent": "preprocessing", "model_class": pipeline_classes.Binarizer},
    {"label": "Normalizer", "node_type": "normalizer",
     "parent": "preprocessing", "model_class": pipeline_classes.Normalizer},
    {"label": "One-Hot Encoding", "node_type": "ohe",
     "parent": "preprocessing", "model_class": pipeline_classes.OneHotEncoder},
    {"label": "Polynomial features", "node_type": "polyfeats",
     "parent": "preprocessing", "model_class": pipeline_classes.PolynomialFeatures},

    # Decomposition / Dimensionality reduction
    {"label": "Principal Component Analysis", "node_type": "pca",
     "parent": "dim_red", "model_class": pipeline_classes.PCA},
    {"label": "Non-negative Matrix Factorization", "node_type": "nmf",
     "parent": "dim_red", "model_class": pipeline_classes.NMF},
    {"label": "Truncated SVD", "node_type": "tsvd",
     "parent": "dim_red", "model_class": pipeline_classes.TruncatedSVD},

    # models
    # Regression
    {"label": "Linear Regression", "node_type": "linr",
     "parent": "models", "model_class": pipeline_classes.LinearRegression,
     "url": "/assets/images/icons/linear_regression.png",
     "problem": "regression"},
    {"label": "SVM Regression", "node_type": "svr",
     "parent": "models", "model_class": pipeline_classes.SVR,
     "url": "/assets/images/icons/svm.png",
     "problem": "regression"},
    {"label": "KNN Regression", "node_type": "knnr",
     "parent": "models", "model_class": pipeline_classes.KNeighborsRegressor,
     "url": "https://i.imgur.com/U9EFqYj.png",
     "problem": "regression"},
    {"label": "Decision Tree Regression", "node_type": "dtr",
     "parent": "models", "model_class": pipeline_classes.DecisionTreeRegressor,
     "url": "/assets/images/icons/decision_tree.png",
     "problem": "regression"},
    {"label": "Dummy model: regression", "node_type": "dummyreg",
     "parent": "models", "model_class": pipeline_classes.DummyRegressor,
     "problem": "regression"},
    {"label": "Random Forests Regression", "node_type": "rfr",
     "parent": "models", "model_class": pipeline_classes.RandomForestRegressor,
     "url": "/assets/images/icons/random_forests.png",
     "problem": "regression"},
    {"label": "Ridge Regression", "node_type": "ridge",
     "parent": "models", "model_class": pipeline_classes.Ridge,
     "url": "/assets/images/icons/ridge_regression.png",
     "problem": "regression"},
    {"label": "Lasso Regression", "node_type": "lasso",
     "parent": "models", "model_class": pipeline_classes.Lasso,
     "problem": "regression"},
    {"label": "SGD Regression", "node_type": "sgdreg",
     "parent": "models", "model_class": pipeline_classes.SGDRegressor,
     "problem": "regression"},
    {"label": "Linear SVR Regression", "node_type": "lsvrreg",
     "parent": "models", "model_class": pipeline_classes.LinearSVR,
     "problem": "regression"},
    {"label": "Nu-SVR", "node_type": "nusvrreg",
     "parent": "models", "model_class": pipeline_classes.NuSVR,
     "problem": "regression"},
    {"label": "Extra Tree Regression", "node_type": "extrareg",
     "parent": "models", "model_class": pipeline_classes.ExtraTreeRegressor,
     "problem": "regression"},


    # Classification
    {"label": "Logistic Regression", "node_type": "logr",
     "parent": "models", "model_class": pipeline_classes.LogisticRegression,
     "url": "/assets/images/icons/logistic_regression.png",
     "problem": "classification"},
    {"label": "KNN Classifier", "node_type": "knnc",
     "parent": "models", "model_class": pipeline_classes.KNeighborsClassifier,
     "url": "https://i.imgur.com/U9EFqYj.png",
     "problem": "classification"},
    {"label": "XGBoost Classifier", "node_type": "xgb",
     "parent": "models", "model_class": pipeline_classes.XGBClassifier,
     "url": "https://i.imgur.com/x4mpozp.png",
     "problem": "classification"},
    {"label": "Random Forest Classifier", "node_type": "rfc",
     "parent": "models", "model_class": pipeline_classes.RandomForestClassifier,
     "url": "https://i.imgur.com/x4mpozp.png",
     "problem": "classification"},
    {"label": "Dummy model: classification", "node_type": "dummyclf",
     "parent": "models", "model_class": pipeline_classes.DummyClassifier,
     "problem": "classification"},
    {"label": "SGD classifier", "node_type": "sgdclf",
     "parent": "models", "model_class": pipeline_classes.SGDClassifier,
     "problem": "classification"},
    {"label": "Linear SVC", "node_type": "lsvcclf",
     "parent": "models", "model_class": pipeline_classes.LinearSVC,
     "problem": "classification"},
    {"label": "Support Vector Classifier", "node_type": "svcclf",
     "parent": "models", "model_class": pipeline_classes.SVC,
     "problem": "classification"},
    {"label": "Nu-SVC", "node_type": "nusvcclf",
     "parent": "models", "model_class": pipeline_classes.NuSVC,
     "problem": "classification"},
    {"label": "Decision Tree Classifier", "node_type": "dtclf",
     "parent": "models", "model_class": pipeline_classes.DecisionTreeClassifier,
     "problem": "classification"},
    {"label": "Extra Tree Classifier", "node_type": "extraclf",
     "parent": "models", "model_class": pipeline_classes.ExtraTreeClassifier,
     "problem": "classification"},

    # Clustering
    {"label": "K-Means Clustering", "node_type": "kmc",
     "parent": "models", "model_class": pipeline_classes.KMeans,
     "url": "/assets/images/icons/knn.png",
     "problem": "clustering"},
    {"label": "DBSCAN Clustering", "node_type": "dbscan",
     "parent": "models", "model_class": pipeline_classes.DBSCAN,
     "problem": "clustering"},
    {"label": "Birch Clustering", "node_type": "birch",
     "parent": "models", "model_class": pipeline_classes.Birch,
     "problem": "clustering"},
    {"label": "Birch Clustering", "node_type": "birch",
     "parent": "models", "model_class": pipeline_classes.MeanShift,
     "problem": "clustering"},
    {"label": "MeanShift Clustering", "node_type": "meanshift",
     "parent": "models", "model_class": pipeline_classes.AgglomerativeClustering,
     "url": "/assets/images/icons/hierarchical_clustering.png",
     "problem": "clustering"},
    # Naive Bayes models
    {"label": "Naive Bayes: Bernoulli", "node_type": "bernoulli_nb",
     "parent": "models", "model_class": pipeline_classes.BernoulliNB,
     "problem": "clustering"},
    {"label": "Naive Bayes: Gaussian", "node_type": "gauss_nb",
     "parent": "models", "model_class": pipeline_classes.GaussianNB,
     "problem": "clustering"},
    {"label": "Naive Bayes: Multinomial", "node_type": "multi_nb",
     "parent": "models", "model_class": pipeline_classes.MultinomialNB,
     "problem": "clustering"},
    # Others
    {"label": "Sentiment Analysis", "node_type": "sentiment",
     "parent": "models", "model_class": pipeline_classes.SentimentAnalyzer,
     "problem": "clustering"},

]

node_options = {options["node_type"]: options
                for options in ml_options}


class Node:
    """
    A class to hold data for a node. Validation and advanced functionality \
    may be added later.

    Create the node either by supplying `options` or `node_type` and \
    a `note_id`.

        Args:
            options (dict): A cytoscape element.
            node_type (str): One of the keys of node_options.
            node_id (str): Unique node identifier.
    """

    __slots__ = ('id', 'node_type', 'model_class', 'parent', 'url',
                 'label', 'order', 'params', 'xpos', 'ypos')

    def __init__(self, node_type, node_id):
        self.id = node_id
        self.node_type = node_type

        # The Model Class and the parent can be retrieved from the
        # node_options dictionary. Same for the other parameters
        self.model_class = node_options[node_type]["model_class"]
        self.parent = node_options[node_type]["parent"]
        self.url = node_options[node_type].get("url", "/static/images"
                                                      "/icons/layers.png")
        self.label = node_options[node_type]["label"]

        # The order signifies the precedence in a pipeline
        self.order = orders[self.parent]

        # Get the default model params
        self.params = {param: values[0] for (param, values)
                       in self.model_class.modifiable_params.items()}

        # Initial positions of nodes on the graph
        self.xpos = 100 + self.order * 250
        self.ypos = 150 + random.randint(-50, 200)

    def render(self):
        return {
            "data": {
                "label": self.label,
                "node_type": self.node_type,
                "id": self.id,
                "parent": self.parent,
                "url": self.url,
            },
            "position": {
                'x': self.xpos,
                'y': self.ypos,
            },
            "classes": "withimage",
        }


class NodeCollection:
    """
    A collection of nodes with some added functionality for rendering them.

    Args:
        nodes (list(dict)): A list of Cytoscape elements.
        graph (`_Graph`): The parent instance.

    Attributes:
        parent_nodes (list(dict)): Cytoscape elements that function as \
                                   parent/group nodes.
    """

    # TODO: These probably need their own positioning!
    # The parent nodes are the groupings of individual nodes,
    # i.e. the rectangles that hold the other nodes.
    # Make them non-selectable so that the user cannot connect
    # a node to a group directly (might be revised later)
    parent_nodes = [
        {"data": {"label": "Inputs", "id": "input"},
         'selectable': False, 'classes': "parents"},
        {"data": {"label": "Cleaning", "id": "cleaning"},
         'selectable': False, 'classes': "parents"},
        {"data": {"label": "User-defined features", "id": "features"},
         'selectable': False, 'classes': "parents"},
        {"data": {"label": "Preprocessing", "id": "preprocessing"},
         'selectable': False, 'classes': "parents"},
        {"data": {"label": "Dimensionality Reduction", "id": "dim_red"},
         'selectable': False, 'classes': "parents"},
        {"data": {"label": "Estimators", "id": "models"},
         'selectable': False, 'classes': "parents"},
    ]

    def __init__(self, graph):
        # node_max is a dictionary to keep track of the maximum
        # id per node_type (so ids don't grow arbitrarily large)
        self.node_max_id = {node_type: f"{node_type}_000"
                            for node_type in node_options}
        self.nodes = []

        # Point to the graph that holds the NodeCollection
        self.graph = graph

        # Counts how many children a parent node holds
        self.group_counts = defaultdict(int)

    def __getitem__(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                return node

        return None

    def create_node(self, node_type):
        # Get the id of the last node of the same type
        max_id = self.node_max_id[node_type]

        # Add +1 to that id
        node_id = f"{node_type}_{str(int(max_id[-3:]) + 1).zfill(3)}"

        # Create a new node and add it to the collection
        return Node(node_type, node_id)

    def add_node(self, new_node):
        self.nodes.append(new_node)

        # Update the counts / max_id
        self.group_counts[new_node.parent] += 1
        self.node_max_id[new_node.node_type] = new_node.id

    def remove_node(self, node_id):
        """
        Remove a node and its edges.

        Args:
            node_id (str): ID of the node to be removed.

        Returns:
            None

        Notes on implementation:
            Consider whether connecting the nodes that were connected to \
            the removed node.
        """

        to_be_removed = self[node_id]

        if to_be_removed is not None:
            self.nodes.remove(to_be_removed)

            # Decrease the count of its parent
            self.group_counts[to_be_removed.parent] -= 1

            # Also remove (filter) edges that this node is connected to
            # but don't reconnect, let the user do it (for now at least)
            self.graph.edge_collection.edges = [
                edge for edge in self.graph.edge_collection.edges
                if ((to_be_removed.id != edge.src_node.id) and
                    (to_be_removed.id != edge.dest_node.id))]

            return to_be_removed

    def render(self):
        # Render nodes and remove parents without children
        return [node.render() for node in self.nodes] + [
            parent for parent in self.parent_nodes
            if self.group_counts[parent["data"]["id"]] > 0
        ]


class Edge:

    def __init__(self, source, target, bidirectional=False):
        self.src_node = source
        self.dest_node = target

    def render(self):
        return {"data": {
            "source": self.src_node.id,
            "target": self.dest_node.id
        }}


class EdgeCollection:
    """
    A collection of edges with some added functionality for rendering them.

    Args:
        edges (list(dict)): A list of Cytoscape elements.
        graph (`_Graph`): The parent instance.
    """

    def __init__(self, graph):
        self.graph = graph
        self.edges = []

    # TODO: This probably needs a better implementation
    def create_edges(self, selected):
        """
        Add edges between the selected nodes.

        Args:
            selected (list(dict)): A list of Cytoscape elements.

        Returns:
            None

        Notes on implementation:
            Currently, edges take their direction according to the \
            order in which the nodes where clicked, not allowing \
            going back but allowing connections within the same level.
        """

        new_edges = []
        # For all 2-way combinations of edges
        for n1, n2 in combinations(selected, 2):
            # Get get the node with that id from the node collection.
            # These are dictionaries following the cytoscape specs
            # so the id is inside a nested dictionary.
            node1 = self.graph.node_collection[n1["id"]]
            node2 = self.graph.node_collection[n2["id"]]

            if node1.order > node2.order:
                new_edge = Edge(source=node2, target=node1)

            # node1.order <= node2.order
            else:
                new_edge = Edge(source=node1, target=node2)

            new_edges.append(new_edge)

        return new_edges

    def add_edges(self, edges):
        for edge in edges:
            self.edges.append(edge)

    def render(self):
        return [edge.render() for edge in self.edges]


class _Graph:
    """
    A Graph to hold collections of nodes and edges and perform functions \
    on them. INTERNAL REPRESENTATION.
    """

    def __init__(self):

        self.node_collection = NodeCollection(self)
        self.edge_collection = EdgeCollection(self)

    def render_graph(self):
        """
        Calculates positions for all nodes in the graph and render it.

        Returns:
            list(dict): A list of Cytoscape elements.
        """

        # TODO: find a better way to estimate positions
        # Convert to networkx: Create a Directed Graph
        # and add the nodes and edges
        nx_graph = nx.DiGraph()
        for node in self.node_collection.nodes:
            nx_graph.add_node(node.id)
        for edge in self.edge_collection.edges:
            nx_graph.add_edge(edge.src_node.id, edge.dest_node.id)

        # Use graphviz to calculate positions for the nodes
        positions = graphviz_layout(nx_graph)
        x_values, y_values = zip(*positions.values())

        # Get the border coordinates for the X dimension
        x_max = max(x_values) + 100
        x_min = min(x_values) - 100

        # A dictionary that holds value counts of elements sharing
        # the same level / parent
        Ys = {}

        # Separate the pixels in groups of equal width
        n_levels = len(orders)
        widths = np.linspace(20, 700, n_levels + 1)

        for node in self.node_collection.nodes:
            # the horizontal position depends only
            # on which is the parent
            x = widths[node.order]

            # the vertical position depends only
            # on how many elements share the same parent
            Ys[node.order] = Ys.get(node.order, 0) + 1
            y = (n_levels - Ys[node.order]) * 200  # (x_max - x_min)

            # for every second parent make all elements go
            # a bit higher to avoid arrows passing through
            # unconnected nodes
            if node.order % 2 == 0:
                y -= 50

            # this fix is necessary due to our viewport
            x = x * 2
            y = y / 2

            # Update the nodes' coordinates
            node.xpos = x
            node.ypos = y

        return self.node_collection.render() + self.edge_collection.render()


class Graph:

    def __init__(self, prebuilt=None):
        self.graph = _Graph()

        # Keep track of input and output nodes for future use
        self.input_nodes = []
        self.output_nodes = []

        if prebuilt is not None:
            self.prebuilt(model_choice=prebuilt)

    def dispatch(self, action, *args):
        func = getattr(self, action)
        if action == "connect":
            func(selected=args[0])
        elif action == "update":
            func(*args[:-1], tapped_node=args[-1])
        else:
            func(*args)

    def add(self, new_node_type):
        new_node = self.graph.node_collection.create_node(new_node_type)
        self.graph.node_collection.add_node(new_node)

        # Also add the node to the appropriate group, if any
        if new_node.parent == "input":
            self.input_nodes.append(new_node)
        elif new_node.parent == "models":
            self.output_nodes.append(new_node)

    def remove(self, old_node_name):
        old_node = self.graph.node_collection.remove_node(old_node_name)

        # Also remove the node from any other categories it was before
        if old_node.parent == "input":
            self.input_nodes.remove(old_node)
        elif old_node.parent == "models":
            self.output_nodes.remove(old_node)

    def update(self, parameters, parameter_values, *, tapped_node):
        node_id = tapped_node["id"]
        new_params = {parameters: parameter_values}
        self.graph.node_collection[node_id].params.update(new_params)

    def prebuilt(self, model_choice):
        # Create the graph anew
        self.graph = _Graph()

        # Get the corrent prebuilt pipeline
        prebuilt = prebuilt_graphs.get(model_choice, None)

        # Add the nodes and edges from the prebuilt pipeline
        if prebuilt is not None:
            for node in prebuilt.nodes:
                self.graph.node_collection.add_node(node)

                # Also add it to inputs / outputs
                if node.parent == "input":
                    self.input_nodes.append(node)
                elif node.parent == "models":
                    self.output_nodes.append(node)

            self.graph.edge_collection.add_edges(prebuilt.edges)

    # Make selected a keyword-only argument so it doesn't
    # auto-create a state in the callbacks-generation loop
    def connect(self, *, selected=None):
        new_edges = self.graph.edge_collection.create_edges(selected)
        self.graph.edge_collection.add_edges(new_edges)

    def available_nodes_for_removal(self):
        return [{"value": node.id, "label": node.label}
                for node in self.graph.node_collection.nodes]

    def render(self):
        return self.graph.render_graph()


# A class for no reason other than it looks simplest to me.
# Could be done on the global scope too. May revise later on.
class DefaultPipeline:
    input_file = Node("input_file", "input_file_001")
    data_cleaner = Node("data_cleaner", "data_cleaner_001")
    stdsc = Node("stdsc", "stdsc_001")
    pca = Node("pca", "pca_001")
    linr = Node("linr", "linr_001")

    nodes = [input_file, data_cleaner, stdsc, pca, linr]

    edges = [Edge(input_file, data_cleaner),
             Edge(data_cleaner, stdsc),
             Edge(stdsc, pca),
             Edge(pca, linr)]


class ScaleReduceKMeans:
    input_file = Node("input_file", "input_file_001")
    stdsc = Node("stdsc", "stdsc_001")
    pca = Node("pca", "pca_001")
    kmc = Node("kmc", "kmc_001")

    nodes = [input_file, stdsc, pca, kmc]

    edges = [Edge(input_file, stdsc),
             Edge(stdsc, pca),
             Edge(pca, kmc)]


class TwitterSentiment:
    input_file = Node("input_file", "input_file_001")
    simple_missing = Node("simple_missing", "simple_missing_001")
    data_cleaner = Node("data_cleaner", "data_cleaner_001")
    sentiment = Node("sentiment", "sentiment_001")

    nodes = [input_file, simple_missing, data_cleaner, sentiment]

    edges = [Edge(input_file, simple_missing),
             Edge(simple_missing, data_cleaner),
             Edge(data_cleaner, sentiment)]


# Name of pipeline and list of dash.cytoscape elements
prebuilt_graphs = {
    "default": DefaultPipeline,
    "scale_reduce_kmeans": ScaleReduceKMeans,
    "twitter_sentiment": TwitterSentiment,
}
