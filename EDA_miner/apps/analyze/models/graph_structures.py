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

from apps.analyze.models import pipeline_classes

import random
import numpy as np
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from itertools import combinations
from collections import defaultdict


orders = {
    "input": 0,
    "cleaning": 1,
    "features": 2,
    "preprocessing": 3,
    "dim_red": 4,
    "models": 5,
}

# TODO: add ensemble models as last-step models (voting, ensembles, etc)
# DO NOT ADD NEURAL NETWORK MODELS YET
ml_options = [
    # Inputs
    {"label": "Twitter API", "node_type": "twitter_api",
     "parent": "input", "func": pipeline_classes.TwitterAPI,
     "url": "/assets/images/icons/new_name.png"},
    {"label": "Input file", "node_type": "input_file",
     "parent": "input", "func": pipeline_classes.InputFile,
     "url": "/assets/images/icons/files.png"},

    # Cleaners
    {"label": "Data Cleaner", "node_type": "data_cleaner",
     "parent": "cleaning", "func": pipeline_classes.DataCleaner,
     "url": "/assets/images/icons/Cleaning.png"},
    {"label": "Fill missing: impute", "node_type": "simple_missing",
     "parent": "cleaning", "func": pipeline_classes.SimpleImputer},
    {"label": "Fill missing: indicator", "node_type": "ind_missing",
     "parent": "cleaning", "func": pipeline_classes.MissingIndicator},

    # Feature makers
    {"label": "Feature constructor", "node_type": "feat_maker",
     "parent": "features", "func": pipeline_classes.FeatureMaker},

    # Preprocessors
    {"label": "Standardization", "node_type": "stdsc",
     "parent": "preprocessing", "func": pipeline_classes.StandardScaler},
    {"label": "Bag of Words", "node_type": "bow",
     "parent": "preprocessing", "func": pipeline_classes.CountVectorizer},
    {"label": "TF-IDF", "node_type": "tfidf",
     "parent": "preprocessing", "func": pipeline_classes.TfidfVectorizer},
    {"label": "Min-Max scaling", "node_type": "minmax_scale",
     "parent": "preprocessing", "func": pipeline_classes.MinMaxScaler},
    {"label": "Label Binarizer", "node_type": "lbinarizer",
     "parent": "preprocessing", "func": pipeline_classes.LabelBinarizer},

    {"label": "Max-Abs scaling", "node_type": "maxabs_scale",
     "parent": "preprocessing", "func": pipeline_classes.MaxAbsScaler},
    {"label": "Binarizer", "node_type": "binarizer",
     "parent": "preprocessing", "func": pipeline_classes.Binarizer},
    {"label": "Normalizer", "node_type": "normalizer",
     "parent": "preprocessing", "func": pipeline_classes.Normalizer},
    {"label": "One-Hot Encoding", "node_type": "ohe",
     "parent": "preprocessing", "func": pipeline_classes.OneHotEncoder},
    {"label": "Polynomial features", "node_type": "polyfeats",
     "parent": "preprocessing", "func": pipeline_classes.PolynomialFeatures},

    # Decomposition / Dimensionality reduction
    {"label": "Principal Component Analysis", "node_type": "pca",
     "parent": "dim_red", "func": pipeline_classes.PCA},
    {"label": "Non-negative Matrix Factorization", "node_type": "nmf",
     "parent": "dim_red", "func": pipeline_classes.NMF},
    {"label": "Truncated SVD", "node_type": "tsvd",
     "parent": "dim_red", "func": pipeline_classes.TruncatedSVD},

    # models
    # Regression
    {"label": "Linear Regression", "node_type": "linr",
     "parent": "models", "func": pipeline_classes.LinearRegression,
     "url": "/assets/images/icons/linear_regression.png"},
    {"label": "SVM Regression", "node_type": "svr",
     "parent": "models", "func": pipeline_classes.SVR,
     "url": "/assets/images/icons/svm.png"},
    {"label": "KNN Regression", "node_type": "knnr",
     "parent": "models", "func": pipeline_classes.KNeighborsRegressor,
     "url": "https://i.imgur.com/U9EFqYj.png"},
    {"label": "Decision Tree Regression", "node_type": "dtr",
     "parent": "models", "func": pipeline_classes.DecisionTreeRegressor,
     "url": "/assets/images/icons/decision_tree.png"},
    {"label": "Dummy model: regression", "node_type": "dummyreg",
     "parent": "models", "func": pipeline_classes.DummyRegressor},
    {"label": "Random Forests Regression", "node_type": "rfr",
     "parent": "models", "func": pipeline_classes.RandomForestRegressor,
     "url": "/assets/images/icons/random_forests.png"},
    {"label": "Ridge Regression", "node_type": "ridge",
     "parent": "models", "func": pipeline_classes.Ridge,
     "url": "/assets/images/icons/ridge_regression.png"},
    {"label": "Lasso Regression", "node_type": "lasso",
     "parent": "models", "func": pipeline_classes.Lasso},
    {"label": "SGD Regression", "node_type": "sgdreg",
     "parent": "models", "func": pipeline_classes.SGDRegressor},
    {"label": "Linear SVR Regression", "node_type": "lsvrreg",
     "parent": "models", "func": pipeline_classes.LinearSVR},
    {"label": "Nu-SVR", "node_type": "nusvrreg",
     "parent": "models", "func": pipeline_classes.NuSVR},
    {"label": "Extra Tree Regression", "node_type": "extrareg",
     "parent": "models", "func": pipeline_classes.ExtraTreeRegressor},


    # Classification
    {"label": "Logistic Regression", "node_type": "logr",
     "parent": "models", "func": pipeline_classes.LogisticRegression,
     "url": "/assets/images/icons/logistic_regression.png"},
    {"label": "KNN Classifier", "node_type": "knnc",
     "parent": "models", "func": pipeline_classes.KNeighborsClassifier,
     "url": "https://i.imgur.com/U9EFqYj.png"},
    {"label": "XGBoost Classifier", "node_type": "xgb",
     "parent": "models", "func": pipeline_classes.XGBClassifier,
     "url": "https://i.imgur.com/x4mpozp.png"},
    {"label": "Random Forest Classifier", "node_type": "rfc",
     "parent": "models", "func": pipeline_classes.RandomForestClassifier,
     "url": "https://i.imgur.com/x4mpozp.png"},
    {"label": "Dummy model: classification", "node_type": "dummyclf",
     "parent": "models", "func": pipeline_classes.DummyClassifier},
    {"label": "SGD classifier", "node_type": "sgdclf",
     "parent": "models", "func": pipeline_classes.SGDClassifier},
    {"label": "Linear SVC", "node_type": "lsvcclf",
     "parent": "models", "func": pipeline_classes.LinearSVC},
    {"label": "Support Vector Classifier", "node_type": "svcclf",
     "parent": "models", "func": pipeline_classes.SVC},
    {"label": "Nu-SVC", "node_type": "nusvcclf",
     "parent": "models", "func": pipeline_classes.NuSVC},
    {"label": "Decision Tree Classifier", "node_type": "dtclf",
     "parent": "models", "func": pipeline_classes.DecisionTreeClassifier},
    {"label": "Extra Tree Classifier", "node_type": "extraclf",
     "parent": "models", "func": pipeline_classes.ExtraTreeClassifier},

    # Clustering
    {"label": "K-Means Clustering", "node_type": "kmc",
     "parent": "models", "func": pipeline_classes.KMeans,
     "url": "/assets/images/icons/knn.png"},
    {"label": "DBSCAN Clustering", "node_type": "dbscan",
     "parent": "models", "func": pipeline_classes.DBSCAN},
    {"label": "Birch Clustering", "node_type": "birch",
     "parent": "models", "func": pipeline_classes.Birch},
    {"label": "Birch Clustering", "node_type": "birch",
     "parent": "models", "func": pipeline_classes.MeanShift},
    {"label": "MeanShift Clustering", "node_type": "meanshift",
     "parent": "models", "func": pipeline_classes.AgglomerativeClustering,
     "url": "/assets/images/icons/hierarchical_clustering.png"},
    # Naive Bayes models
    {"label": "Naive Bayes: Bernoulli", "node_type": "bernoulli_nb",
     "parent": "models", "func": pipeline_classes.BernoulliNB},
    {"label": "Naive Bayes: Gaussian", "node_type": "gauss_nb",
     "parent": "models", "func": pipeline_classes.GaussianNB},
    {"label": "Naive Bayes: Multinomial", "node_type": "multi_nb",
     "parent": "models", "func": pipeline_classes.MultinomialNB},
    # Others
    {"label": "Sentiment Analysis", "node_type": "sentiment",
     "parent": "models", "func": pipeline_classes.SentimentAnalyzer},

]

node_options = {options["node_type"]: options
                for options in ml_options}


class Node:
    """
    A class to hold data for the nodes. Validation and advanced \
    functionality may be added later.

    Create the node either by supplying `options` or `node_type` and \
    a `note_id`.

        Args:
            options (dict): A cytoscape element.
            node_type (str): One of the keys of node_options.
            node_id (str): Unique node identifier.
    """
    # TODO: Consider using slots, and/or refactoring the class.

    def __init__(self, *, options=None, node_type=None, node_id=None):

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

        self.url = node_options[options["node_type"]].get("url",
                                            "/assets/images/icons/layers.png")

        self.label = options["label"]

        self.node_type = options["node_type"]
        self.order = orders[self.parent]

        self.options = {
            "data": {
                "label": self.label,
                "node_type": self.node_type,
                "id": self.id,
                "parent": self.parent,
                "url": self.url,
                "func_params": options.get("func_params", {})
            },
            "position": {
                'x': 100 + self.order * 250,
                'y': 150 + random.randint(-50, 200)
            },
            "classes": "withimage",
        }

    def render(self):
        return self.options


class NodeCollection:
    """
    A collection of nodes with some added functionality for rendering them.

    Args:
        nodes (list(dict)): A list of Cytoscape elements.
        graph (`Graph`): The parent instance.

    Attributes:
        parent_nodes (list(dict)): Cytoscape elements that function as \
                                   parent/group nodes.
    """

    # TODO: These probably need their own positioning!
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

    def __init__(self, nodes=[], graph=None):
        self.node_max = {node_type: f"{node_type}_000"
                         for node_type in node_options}
        self.nodes = []
        self.graph = graph

        self.group_counts = defaultdict(int)

        # If nodes are given, parse them into an internal
        # representation and increase the relevant counts
        # (nodes originally are dictionaries of attributes)
        for n in nodes:
            node = Node(options=n)

            # keep the maximum id (e.g. 'linr_002')
            self.node_max[node.node_type] = max(self.node_max[node.node_type],
                                                node.id)
            self.nodes.append(node)
            self.group_counts[node.parent] += 1

    def add_node(self, node_type):
        """
        Add a new node given a node_type. Generate the ID based on \
        the previous max for ID for the selected node type.

        Args:
            node_type(str): One of the keys of node_options.

        Returns:
            None
        """

        max_id = self.node_max[node_type]
        node_id = f"{node_type}_{str(int(max_id[-3:]) + 1).zfill(3)}"

        new_node = Node(node_type=node_type, node_id=node_id)
        self.nodes.append(new_node)

        self.group_counts[new_node.parent] += 1

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

        to_be_removed = [n for n in self.nodes if n.id == node_id]

        if len(to_be_removed):
            self.nodes.remove(to_be_removed[0])

            # Also removed edges that this node is connected to (but don't)
            # reconnect, let the user do it (for now at least)
            self.graph.edge_collection.edges = [
                edge for edge in self.graph.edge_collection.edges
                if ((to_be_removed[0].id != edge["data"]["source"]) and
                    (to_be_removed[0].id != edge["data"]["target"]))]

    def render(self):
        # Render nodes and remove parents without children
        return [node.render() for node in self.nodes] + [
            parent for parent in self.parent_nodes
            if self.group_counts[parent["data"]["id"]] > 0
        ]


class EdgeCollection:
    """
    A collection of edges with some added functionality for rendering them.

    Args:
        edges (list(dict)): A list of Cytoscape elements.
        graph (`Graph`): The parent instance.
    """

    def __init__(self, edges=[], graph=None):
        self.edges = edges
        self.graph = graph

    # TODO: This probably needs a better implementation
    def add_edges(self, selected):
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

        for combination in combinations(selected, 2):
            node1 = Node(options=combination[0])
            node2 = Node(options=combination[1])

            if node1.order > node2.order:
                new_edge = {"data": {
                    "source": node2.id,
                    "target": node1.id
                }}

                self.edges.append(new_edge)

            elif node1.order <= node2.order:
                new_edge = {"data": {
                    "source": node1.id,
                    "target": node2.id
                }}

                self.edges.append(new_edge)

    def render(self):
        return self.edges


class Graph:
    """
    A Graph to hold collections of nodes and edges and perform functions \
    on them.

    Args:
        elems (list(dict)): A list of Cytoscape elements.
    """

    def __init__(self, elems):

        edges = [elem for elem in elems if "source" in elem["data"]]
        # Don't add parent nodes, they will be added by default
        nodes = [elem for elem in elems if (("source" not in elem["data"]) and
                                            ("parent" in elem["data"]))]

        self.node_collection = NodeCollection(nodes, self)
        self.edge_collection = EdgeCollection(edges, self)

    def render_graph(self):
        """
        Calculates positions for all nodes in the graph and render it.

        Returns:
            list(dict): A list of Cytoscape elements.
        """

        # TODO: find a better way to estimate positions
        # Convert to networkx so we can use its functionality
        # for determining positions
        nx_graph = nx.DiGraph()
        for node in self.node_collection.nodes:
            nx_graph.add_node(node.id)
        for edge in self.edge_collection.edges:
            nx_graph.add_edge(edge["data"]["source"], edge["data"]["target"])

        # We then use it to get min/max values.
        # The intended use to use it for more, but
        # it seems to be causing many overlaps
        positions = graphviz_layout(nx_graph)
        x_values, y_values = zip(*positions.values())
        x_max = max(x_values) + 100
        x_min = min(x_values) - 100

        # A dictionary that holds value counts of elements sharing
        # the same level / parent
        Ys = {}
        # linspace for how many different parents exist
        n_levels = 5
        widths = np.linspace(20, 700, n_levels + 1)
        for node in self.node_collection.nodes:
            # the horizontal position depends only
            # on which is the parent
            x = widths[node.order]

            # the vertical position depends only
            # on how many elements share the same parent
            Ys[node.order] = Ys.get(node.order, 0) + 1
            y = (n_levels - Ys[node.order]) * (x_max - x_min)

            # for every second parent make all elements go
            # a bit higher to avoid arrows to pass through
            # unconnected nodes
            if node.order % 2 == 0:
                y -= 50

            # this fix is necessary due to our viewport
            node.options["position"] = {"x": x * 2,
                                        "y": y / 2}

        # TODO: Remove parents that don't have children
        return self.node_collection.render() + self.edge_collection.render()


class GraphUtils:
    """
    To be used for default layouts. This definitely needs a better \
    implementation to be able to handle more advanced pipelines, and/or \
    provide better interface.

    Args:
        steps (list(tuples): Pipeline steps in the following format: \
                             (order, node_type, description).
    """

    def __init__(self, steps):
        self.G = Graph([])
        for step in steps:
            self.G.node_collection.add_node(step[1])
        for s1, s2 in zip(self.G.node_collection.nodes[:-1],
                          self.G.node_collection.nodes[1:]):
            self.G.edge_collection.add_edges([s1.render(), s2.render()])

    def render_graph(self):
        return self.G.render_graph()


# TODO: This probably needs to go inside GraphUtils
# Name of pipeline and list of dash.cytoscape elements
prebuilt_pipelines = {

    # Standard scaling, dimensionality reduction, model
    "default": [
        (0, "input_file", "Input data"),
        (1, "data_cleaner", "Data cleaning"),
        (2, "feat_maker", "Feature Maker"),
        (3, "stdsc", "Standardization"),
        (4, "pca", "Principal Components Analysis"),
        (5, "linr", "Linear Regression"),
    ],

    "scale_reduce_kmeans": [
        (0, "input_file", "Input data"),
        (3, "stdsc", "Standardization"),
        (4, "pca", "Principal Components Analysis"),
        (5, "kmc", "K-Means Clustering"),
    ],

    "twitter_sentiment": [
        (0, "twitter_api", "Twitter API"),
        (1, "simple_missing", "Fill missing: impute"),
        (2, "data_cleaner", "Data Cleaner"),
        (3, "sentiment", "Sentiment Analysis"),
    ]

}
