"""
This module collects every model class, including input and transformers.

Notes to others:
    Feel free to tamper with anything or add your own models and classes. \
    Everything should implement an sklearn-like API providing a fit and \
    (more importantly) a transform method. It should also have a \
    `modifiable_params` dictionary with the names of attributes that can \
    be modified and a list of possible values (keep them limited, for now). \
    Input classes should subclass `GenericInput`. If you add new classes \
    remember to modify `ml_options` in `graph_structures.py`.
"""

from dash.exceptions import PreventUpdate

from utils import r, get_data

import dill
import pickle
import sympy
import numpy as np
from textblob import TextBlob

from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
from sklearn.base import RegressorMixin
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


# All custom classes should subclass these ones.
# This is done for checks down the line that
# determine properties of nodes of the Graph
# which in turn is useful for selecting dataset
# and being able to create custom features or
# handle outputs

class BaseInput(BaseEstimator, TransformerMixin):
    """
    Base class for ALL input nodes. Important for pipeline creation. \
    If you define your own input class you MUST subclass this at least \
    indirectly. For now, use GenericInput if you are dealing with files \
    or dataframes, else use directly.

    This may become an abstract base class, or it may be discarded in \
    favor of GenericInput.
    """
    pass


class GenericInput(BaseInput):
    """
    Base class for dataset/file loaders.
    """
    modifiable_params = {}


# TODO: This might be necessary, review carefully.
class TerminalNode(BaseEstimator):
    modifiable_params = {}


class InputFile(GenericInput):
    """
    An input node used for selecting a user-uploaded dataset.
    """

    modifiable_params = {}

    def __init__(self, dataset=None):
        self.dataset = dataset

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


# TODO: I changed my mind. This implementation SUCKS HARD.
#       Rework the whole Twitter dataset idea by getting
#       the data in the Data View tab and treat Twitter
#       as regular datasets. Should not subclass GenericInput !
class TwitterAPI(GenericInput):
    """
    An input node used for working on Twitter data.
    """

    modifiable_params = {}

    def __init__(self, dataset=None):
        if dataset is None:
            self.dataset = dataset
        elif dataset == "*":
            raise NotImplementedError()
        else:
            self.dataset = pickle.loads(r.get(dataset))

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # TODO: Sort based on date
        return np.array([status.text for status in self.dataset],
                        dtype=object).reshape((-1, 1))


# TODO: Actually implement this.
class DataCleaner(BaseEstimator, TransformerMixin):
    modifiable_params = {}

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


# TODO: Actually implement this, OR delete.
class DataImputer(BaseEstimator, TransformerMixin):
    modifiable_params = {}

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


# Template for creating your own node classes
class CustomClassifier(BaseEstimator, ClassifierMixin):
    modifiable_params = {}

    def fit(self, X, y=None):
        return self

    def predict(self, X):
        return np.ones(X.shape[0])


# parameters to be used for eval and exec statements later on
sympy_funcs = {f"{f}": eval(f"sympy.{f}") for f in dir(sympy)}
global_scope = {"sympy": sympy, "__builtins__": None}


class FeatureMaker(BaseEstimator, TransformerMixin):
    """
    A node that helps the user create combinations and transformations \
    of features by selecting columns from the input dataset and writing \
    a mathematical function as text, using whatever is available to sympy.

    Args:
        func_name:
        cols:
        dataset_choice:
        user_id:
    """

    modifiable_params = {}

    def __init__(self, func_name="", cols=None, dataset_choice=None,
                 user_id=None):
        self.query = r.get(func_name)
        self.cols = cols
        self.func = lambda x: x
        self.dataset_choice = dataset_choice
        self.user_id = user_id

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if self.cols is None:
            return self.func(X)

        else:
            # Evaluate the user-defined function
            if self.query is not None:
                # http: // lybniz2.sourceforge.net / safeeval.html
                symbols, f, func = dill.loads(self.query)

                exec(symbols, global_scope,
                     sympy_funcs)
                exec(f, global_scope, sympy_funcs)
                self.func = eval(func, global_scope,
                                 sympy_funcs)

            try:
                # TODO: This needs a better implementation than re-loading
                #       the whole dataset from Redis. Can probably be fixed
                #       if edge params are implemented.
                # Overwrite X with the original DataFrame
                X = get_data(self.dataset_choice, self.user_id)
                cols = [X[col] for col in self.cols]

            except IndexError as e:
                raise IndexError((str(e)+", probably incorrect input cols: " +
                                  str(self.cols)))

            return self.func(*cols).values.reshape((-1, 1))


# TODO: do an actual implementation
class SentimentAnalyzer(BaseEstimator, RegressorMixin):
    modifiable_params = {}

    def predict(self, X):
        if isinstance(X, np.ndarray):
            return np.array([TextBlob(x[0]).polarity for x in X])
        else:
            return np.array([TextBlob(x).polarity for x in X])


# For EVERY model that is expected to have parametrization
# you are expected to give its class a `modifiable_params`
# dict with keys being the function argument and values the
# allowed set of values (make it limited, i.e. few choices)
# Also, the first is assumed to be the default value which
# will be passed to the model upon the creation of pipelines.

LinearRegression.modifiable_params = {
    "fit_intercept": [True, False],
}

LogisticRegression.modifiable_params = {
    "penalty": ["l2", "l1"],
    "fit_intercept": [True, False],
    "C": [1, 0.1, 0.2, 0.5, 2, 5, 10],
    "multi_class": ["ovr", "multinomial", "auto"],
}

Ridge.modifiable_params = {
    "alpha": [1, 0.1, 0.2, 0.5, 2, 5, 10],
    "fit_intercept": [True, False],
}

Lasso.modifiable_params = {
    "alpha": [1, 0.1, 0.2, 0.5, 2, 5, 10],
    "fit_intercept": [True, False],
}

SVR.modifiable_params = {
    "alpha": [1, 0.1, 0.2, 0.5, 2, 5, 10],
    "kernel": ["rbf", "poly", "linear"],
    "degree": [3, 1, 2, 5, 7, 10],
    "C": [1, 0.1, 0.2, 0.5, 2, 5, 10],
}

DecisionTreeRegressor.modifiable_params = {
    "max_depth": [None, 3, 5, 7, 9, 12],
}

DummyClassifier.modifiable_params = {
    "strategy": ["stratified", "most_frequent", "prior", "uniform"],
}

DummyRegressor.modifiable_params = {
    "strategy": ["mean", "median"],
}

KMeans.modifiable_params = {
    "n_clusters": [8, 2, 3, 4, 5, 6, 7, 9, 10, 15, 20],
}

DBSCAN.modifiable_params = {
    "eps": [0.5, 0.01, 0.05, 0.1, 0.2, 1, 2, 5],
}

Birch.modifiable_params = {
    "threshold": [0.5, 0.1, 0.2, 0.75, 0.95],
}

AgglomerativeClustering.modifiable_params = {
    "n_clusters": [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20],
    "linkage": ["ward", "complete", "average", "single"]
}

StandardScaler.modifiable_params = {
    "with_mean": [True, False],
    "with_std": [True, False]
}

MinMaxScaler.modifiable_params = {}

LabelBinarizer.modifiable_params = {}

KNeighborsRegressor.modifiable_params = {
    "n_neighbors": [5, 3, 7, 9]
}

KNeighborsClassifier.modifiable_params = {
    "n_neighbors": [5, 3, 7, 9]
}

BernoulliNB.modifiable_params = {
    "alpha": [1, 0.1, 0.2, 0.5, 0.7, 0.85],
}

XGBClassifier.modifiable_params = {}

GaussianNB.modifiable_params = {}

MultinomialNB.modifiable_params = {
    "alpha": [1, 0.1, 0.2, 0.5, 0.7, 0.85],
}

SimpleImputer.modifiable_params = {
    "strategy": ["most_frequent", "mean", "median"]
}

MissingIndicator.modifiable_params = {}

CountVectorizer.modifiable_params = {
    "stop_words": [None, "english"],
    "analyzer": ["word", "char", "char_wb"],
    "max_features": [None, 1000, 2000, 5000, 10000, 15000, 25000],
    "max_df": [1, 0.1, 0.2, 0.5, 0.75, 0.95],
    "min_df": [1, 0.1, 0.2, 0.5, 0.75, 0.95],
}

TfidfVectorizer.modifiable_params = {
    "stop_words": [None, "english"],
    "analyzer": ["word", "char", "char_wb"],
    "max_features": [None, 1000, 2000, 5000, 10000, 15000, 25000],
    "max_df": [1, 0.1, 0.2, 0.5, 0.75, 0.95],
    "min_df": [1, 0.1, 0.2, 0.5, 0.75, 0.95],
}

PCA.modifiable_params = {
    "n_components": [None, 2, 3, 5, 10, 20, 50, 100, 300],
    "whiten": [False, True],
}

NMF.modifiable_params = {
    "n_components": [None, 2, 3, 5, 10, 20, 50, 100, 300],
}

TruncatedSVD.modifiable_params = {
    "n_components": [2, None, 3, 5, 10, 20, 50, 100, 300],
}

RandomForestRegressor.modifiable_params = {
    "n_estimators": [10, 20, 50, 100, 200, 500],
    "max_depth": [None, 3, 5, 7, 9, 12, 15],
    "max_features": ["auto", 0.1, 0.2, 0.5, 0.7, 0.9, 1]
}

RandomForestClassifier.modifiable_params = {
    "n_estimators": [10, 20, 50, 100, 200, 500],
    "max_depth": [None, 3, 5, 7, 9, 12, 15],
    "max_features": ["auto", 0.1, 0.2, 0.5, 0.7, 0.9, 1]
}