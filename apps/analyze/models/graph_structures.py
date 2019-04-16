# import custom models
from apps.analyze.models.pipeline_classes import TwitterAPI, InputFile
from apps.analyze.models.pipeline_classes import DataCleaner, DataImputater
from apps.analyze.models.pipeline_classes import CustomClassifier

import random
from itertools import combinations
from xgboost import XGBClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.linear_model import Ridge, Lasso
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.cluster import KMeans, DBSCAN, Birch, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, NMF, TruncatedSVD
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.impute import SimpleImputer, MissingIndicator
from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler, LabelBinarizer


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
    {"label": "Twitter API", "node_type": "twitter_api",
     "parent": "input", "func": TwitterAPI},
    {"label": "Input file", "node_type": "input_file",
     "parent": "input", "func": InputFile},

    # Cleaners
    {"label": "Data Cleaner", "node_type": "data_cleaner",
     "parent": "cleaning", "func": DataCleaner,
     "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Broom.svg/200px-Broom.svg.png"},
    {"label": "Fill missing: impute", "node_type": "simple_missing",
     "parent": "cleaning", "func": SimpleImputer},
    {"label": "Fill missing: indicator", "node_type": "ind_missing",
     "parent": "cleaning", "func": MissingIndicator},

    # Preprocessors
    {"label": "Standardization", "node_type": "stdsc",
     "parent": "preprocessing", "func": StandardScaler},
    {"label": "Bag of Words", "node_type": "bow",
     "parent": "preprocessing", "func": CountVectorizer},
    {"label": "TF-IDF", "node_type": "tfidf",
     "parent": "preprocessing", "func": TfidfVectorizer},
    {"label": "Min-Max scaling", "node_type": "minmax_scale",
     "parent": "preprocessing", "func": MinMaxScaler},
    {"label": "Label Binarizer", "node_type": "lbinarizer",
     "parent": "preprocessing", "func": LabelBinarizer},

    # Decomposition / Dimensionality reduction
    {"label": "Principal Component Analysis", "node_type": "pca",
     "parent": "dim_red", "func": PCA},
    {"label": "Non-negative Matrix Factorization", "node_type": "nmf",
     "parent": "dim_red", "func": NMF},
    {"label": "Truncated SVD", "node_type": "tsvd",
     "parent": "dim_red", "func": TruncatedSVD},

    # models
    # Regression
    {"label": "Linear Regression", "node_type": "linr",
     "parent": "models", "func": LinearRegression,
     "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Linear_regression.svg/200px-Linear_regression.svg.png"},
    {"label": "SVM Regression", "node_type": "svr",
     "parent": "models", "func": SVR},
    {"label": "KNN Regression", "node_type": "knnr",
     "parent": "models", "func": KNeighborsRegressor},
    {"label": "Decision Tree Regression", "node_type": "dtr",
     "parent": "models", "func": DecisionTreeRegressor},
    {"label": "Dummy model: regression", "node_type": "dummyreg",
     "parent": "models", "func": DummyRegressor},
    {"label": "Random Forests Regression", "node_type": "rfr",
     "parent": "models", "func": RandomForestRegressor},
    {"label": "Ridge Regression", "node_type": "ridge",
     "parent": "models", "func": Ridge},
    {"label": "Lasso Regression", "node_type": "lasso",
     "parent": "models", "func": Lasso},
    # Classification
    {"label": "Logistic Regression", "node_type": "logr",
     "parent": "models", "func": LogisticRegression},
    {"label": "KNN Classifier", "node_type": "knnc",
     "parent": "models", "func": KNeighborsClassifier},
    {"label": "XGBoost Classifier", "node_type": "xgb",
     "parent": "models", "func": XGBClassifier},
    {"label": "Random Forest Classifier", "node_type": "rfc",
     "parent": "models", "func": RandomForestClassifier},
    {"label": "Dummy model: classification", "node_type": "dummyclf",
     "parent": "models", "func": DummyClassifier},
    # Clustering
    {"label": "K-Means Clustering", "node_type": "kmc",
     "parent": "models", "func": KMeans},
    {"label": "DBSCAN Clustering", "node_type": "dbscan",
     "parent": "models", "func": DBSCAN},
    {"label": "Birch Clustering", "node_type": "birch",
     "parent": "models", "func": Birch},
    {"label": "Agglomerative Clustering", "node_type": "agglomerative",
     "parent": "models", "func": AgglomerativeClustering},
    # Naive Bayes models
    {"label": "Naive Bayes: Bernoulli", "node_type": "bernoulli_nb",
     "parent": "models", "func": BernoulliNB},
    {"label": "Naive Bayes: Gaussian", "node_type": "gauss_nb",
     "parent": "models", "func": GaussianNB},
    {"label": "Naive Bayes: Multinomial", "node_type": "multi_nb",
     "parent": "models", "func": MultinomialNB},

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

        self.url = node_options[options["node_type"]].get("url",
                        "https://lh3.googleusercontent.com/lRUKBMe6NXaKbXifj6lL3IFml1gqgY8etG2ylMC5OoVVHllgAh-_NXVca182gvoXN4U")

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

    # Make them non-selectable so that the user cannot connect
    # a node to a group directly (might be revised later)
    parent_nodes = [
        {"data": {"label": "Inputs", "id": "input"},
         'selectable': False, 'classes': "parents"},
        {"data": {"label": "Cleaning", "id": "cleaning"},
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

        if len(to_be_removed):
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

    # TODO: This needs a better implementation to allow
    #       chaining of models in the same step
    def add_edges(self, selected):

        for combination in combinations(selected, 2):
            node1 = Node(options=combination[0])
            node2 = Node(options=combination[1])

            # TODO: It is these 3 ifs that need changing.
            #       We need a new way to define order
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