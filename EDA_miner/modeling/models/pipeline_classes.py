"""
This module collects every model class, including input and transformers.

Notes to others:
    Feel free to tamper with anything or add your own models and classes. \
    Everything should implement an sklearn-like API providing a fit and \
    (more importantly) a transform method. It should also have a \
    `modifiable_params` dictionary with the names of attributes that can \
    be modified and a list of possible values (keep them limited, for now). \
    Input classes should subclass `GenericInput`. If you add new classes \
    remember to modify `ml_options` in `graph_structures.py`. \
    DO NOT ADD NEURAL NETWORK MODELS YET!

TODO:
    Add ensemble models as last-step models (voting, ensembles, etc).

"""

import numpy as np
import textblob
import sys
import inspect

import xgboost
from sklearn import base
from sklearn import cluster
from sklearn import decomposition
from sklearn import dummy
from sklearn import ensemble
from sklearn import impute
from sklearn import linear_model
from sklearn import naive_bayes
from sklearn import neighbors
from sklearn import preprocessing
from sklearn import svm
from sklearn import tree
from sklearn.feature_extraction import text

#

"""
======== Custom classes ========

All custom classes should subclass these ones.
This is done for checks down the line that
determine properties of nodes of the Graph
which in turn is useful for selecting dataset
and being able to create custom features or
handle outputs
"""


class InputFile(base.BaseEstimator, base.TransformerMixin):
    """
    An input node used for selecting a user-uploaded dataset.
    """

    label = "Input File"
    node_type = "input_file"
    parent = "input"
    url = "/static/images/icons/files.png"
    modifiable_params = {"dataset": [None]}

    def __init__(self, dataset=None):
        self.dataset = dataset

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


# TODO: Actually implement this.
class DataCleaner(base.BaseEstimator, base.TransformerMixin):
    label = "Data Cleaner"
    node_type = "data_cleaner"
    parent = "cleaning"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {}

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


# Template for creating your own node classes
class CustomClassifier(base.BaseEstimator, base.ClassifierMixin):
    label = "Custom classifier"
    node_type = "data_cleaner"
    parent = "models"
    problem = "classification"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {}

    def fit(self, X, y=None):
        return self

    def predict(self, X):
        return np.ones(X.shape[0])


# TODO: do an actual implementation
class SentimentAnalyzer(base.BaseEstimator, base.RegressorMixin):
    label = "Sentiment Analysis"
    node_type = "sentiment"
    parent = "models"
    problem = "classification"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {}

    def predict(self, X):
        if isinstance(X, np.ndarray):
            return np.array([textblob.TextBlob(x[0]).polarity for x in X])
        else:
            return np.array([textblob.TextBlob(x).polarity for x in X])


"""
======== Prebuilt classes ========

For EVERY model that is expected to have parametrization
you are expected to give its class a `modifiable_params`
dict with keys being the function argument and values the
allowed set of values (make it limited, i.e. few choices)
Also, the first is assumed to be the default value which
will be passed to the model upon the creation of pipelines.
And of course it must have `fit` and transform methods.
"""


"""
======== Cleaners ========
"""


class SimpleImputer(impute.SimpleImputer):
    label = "Fill missing: impute"
    node_type = "simple_missing"
    parent = "cleaning"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "strategy": ["most_frequent", "mean", "median"]
    }


class MissingIndicator(impute.MissingIndicator):
    label = "Fill missing: indicator"
    node_type = "ind_missing"
    parent = "cleaning"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {}


"""
======== Transformers / preprocessors ========
"""


class StandardScaler(preprocessing.StandardScaler):
    label = "Standardization"
    node_type = "stdsc"
    parent = "preprocessing"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "with_mean": [True, False],
        "with_std": [True, False]
    }


class MinMaxScaler(preprocessing.MinMaxScaler):
    label = "Min-Max scaling"
    node_type = "minmax_scale"
    parent = "preprocessing"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {}


class MaxAbsScaler(preprocessing.MaxAbsScaler):
    label = "Max-Abs scaling"
    node_type = "maxabs_scale"
    parent = "preprocessing"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {}


# TODO: Add threshold as numeric input
class Binarizer(preprocessing.Binarizer):
    label = "Binarizer"
    node_type = "binarizer"
    parent = "preprocessing"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {}


class Normalizer(preprocessing.Normalizer):
    label = "Normalizer"
    node_type = "normalizer"
    parent = "preprocessing"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "norm": ["l2", "l1", "max"]
    }


class LabelBinarizer(preprocessing.LabelBinarizer):
    label = "Label Binarizer"
    node_type = "lbinarizer"
    parent = "preprocessing"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {}


class OneHotEncoder(preprocessing.OneHotEncoder):
    label = "One-Hot Encoding"
    node_type = "ohe"
    parent = "preprocessing"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "drop": ["first", None]
    }


class PolynomialFeatures(preprocessing.PolynomialFeatures):
    label = "Polynomial features"
    node_type = "polyfeats"
    parent = "preprocessing"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "degree": [2, 3, 4, 5],
        "interaction_only": [False, True],
        "include_bias": [True, False]
    }


class CountVectorizer(text.CountVectorizer):
    label = "Bag of Words"
    node_type = "bow"
    parent = "preprocessing"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "stop_words": [None, "english"],
        "analyzer": ["word", "char", "char_wb"],
        "max_features": [None, 1000, 2000, 5000, 10000, 15000, 25000],
        "max_df": [1, 0.1, 0.2, 0.5, 0.75, 0.95],
        "min_df": [1, 0.1, 0.2, 0.5, 0.75, 0.95],
    }


class TfidfVectorizer(text.TfidfVectorizer):
    label = "TF-IDF"
    node_type = "tfidf"
    parent = "preprocessing"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "stop_words": [None, "english"],
        "analyzer": ["word", "char", "char_wb"],
        "max_features": [None, 1000, 2000, 5000, 10000, 15000, 25000],
        "max_df": [1, 0.1, 0.2, 0.5, 0.75, 0.95],
        "min_df": [1, 0.1, 0.2, 0.5, 0.75, 0.95],
    }


"""
======== Dimensionality reducers ========
"""


class PCA(decomposition.PCA):
    label = "Principal Component Analysis"
    node_type = "pca"
    parent = "dim_red"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "n_components": [None, 2, 3, 5, 10, 20, 50, 100, 300],
        "whiten": [False, True],
    }


class NMF(decomposition.NMF):
    label = "Non-negative Matrix Factorization"
    node_type = "nmf"
    parent = "dim_red"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "n_components": [None, 2, 3, 5, 10, 20, 50, 100, 300],
    }


class TruncatedSVD(decomposition.TruncatedSVD):
    label = "Truncated SVD"
    node_type = "tsvd"
    parent = "dim_red"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "n_components": [2, None, 3, 5, 10, 20, 50, 100, 300],
    }


"""
======== Regression ========
"""


class LinearRegression(linear_model.LinearRegression):
    label = "Linear Regression"
    node_type = "linr"
    parent = "models"
    problem = "regression"
    url = "/static/images/icons/linear_regression.png"
    modifiable_params = {
        "fit_intercept": [True, False],
    }


class Ridge(linear_model.Ridge):
    label = "Ridge Regression"
    node_type = "ridge"
    parent = "models"
    problem = "regression"
    url = "/static/images/icons/ridge_regression.png"
    modifiable_params = {
        "alpha": [1, 0.1, 0.2, 0.5, 2, 5, 10],
        "fit_intercept": [True, False],
    }


class Lasso(linear_model.Lasso):
    label = "Lasso Regression"
    node_type = "lasso"
    parent = "models"
    problem = "regression"
    url = "/static/images/icons/files.png"
    modifiable_params = {
        "alpha": [1, 0.1, 0.2, 0.5, 2, 5, 10],
        "fit_intercept": [True, False],
    }


class SVR(svm.SVR):
    label = "SVM Regression"
    node_type = "svr"
    parent = "models"
    problem = "regression"
    url = "/static/images/icons/svm.png"
    modifiable_params = {
        "alpha": [1, 0.1, 0.2, 0.5, 2, 5, 10],
        "kernel": ["rbf", "poly", "linear"],
        "degree": [3, 1, 2, 5, 7, 10],
        "C": [1, 0.1, 0.2, 0.5, 2, 5, 10],
    }


class DecisionTreeRegressor(tree.DecisionTreeRegressor):
    label = "Decision Tree Regression"
    node_type = "dtr"
    parent = "models"
    problem = "regression"
    url = "/static/images/icons/decision_tree.png"
    modifiable_params = {
        "max_depth": [None, 3, 5, 7, 9, 12],
    }


class ExtraTreeRegressor(tree.ExtraTreeRegressor):
    label = "Extra Tree Regression"
    node_type = "extrareg"
    parent = "models"
    problem = "regression"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "max_depth": [None, 3, 5, 7, 9, 12],
    }


class DummyRegressor(dummy.DummyRegressor):
    label = "Dummy model: regression"
    node_type = "dummyreg"
    parent = "models"
    problem = "regression"
    url = "/static/images/icons/linear_regression.png"
    modifiable_params = {
        "strategy": ["mean", "median"],
    }


class KNeighborsRegressor(neighbors.KNeighborsRegressor):
    label = "KNN Regression"
    node_type = "knnr"
    parent = "models"
    problem = "regression"
    url = "/static/images/icons/knn.png"
    modifiable_params = {
        "n_neighbors": [5, 3, 7, 9]
    }


class RandomForestRegressor(ensemble.RandomForestRegressor):
    label = "Random Forests Regression"
    node_type = "rfr"
    parent = "models"
    problem = "regression"
    url = "/static/images/icons/random_forests.png"
    modifiable_params = {
        "n_estimators": [10, 20, 50, 100, 200, 500],
        "max_depth": [None, 3, 5, 7, 9, 12, 15],
        "max_features": ["auto", 0.1, 0.2, 0.5, 0.7, 0.9, 1]
    }


class SGDRegressor(linear_model.SGDRegressor):
    label = "SGD Regression"
    node_type = "sgdreg"
    parent = "models"
    problem = "regression"
    url = "/static/images/icons/linear_regression.png"
    modifiable_params = {
        "loss": ["squared_loss", "huber", "epsilon_insensitive",
                 "squared_epsilon_insensitive"],
        "penalty": ["none", "l2", "l1", "elasticnet"],
        "l1_ratio": [0.15, 0.01, 0.05, 0.1, 0.2, 0.5, 0.75, 0.9],
        "learning_rate": ["optimal", "constant", "invscaling", "adaptive"]
    }


class LinearSVR(svm.LinearSVR):
    label = "Linear SVR Regression"
    node_type = "lsvrreg"
    parent = "models"
    problem = "regression"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "C": [1, 0.01, 0.1, 0.5, 2, 5, 10],
        "fit_intercept": [True, False],
        "max_iter": [200, 50, 100, 500, 1000]
    }


class NuSVR(svm.NuSVR):
    label = "Nu-SVR"
    node_type = "nusvr"
    parent = "models"
    problem = "regression"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "nu": [0.5, 0.01, 0.1, 0.2, 0.7, 0.85, 1],
        "C": [1, 0.01, 0.1, 0.5, 2, 5, 10],
        "gamma": [1, 0.01, 0.1, 0.5, 2, 5, 10],
        "degree": [3, 1, 2, 5],
        "kernel": ["rbf", "linear", "poly", "sigmoid"],
        "max_iter": [200, 50, 100, 500, 1000]
    }


"""
======== Classification ========
"""


class LogisticRegression(linear_model.LogisticRegression):
    label = "Logistic Regression"
    node_type = "logr"
    parent = "models"
    problem = "classification"
    url = "/static/images/icons/logistic_regression.png"
    modifiable_params = {
        "penalty": ["l2", "l1"],
        "fit_intercept": [True, False],
        "C": [1, 0.1, 0.2, 0.5, 2, 5, 10],
        "multi_class": ["ovr", "multinomial", "auto"],
    }


class DummyClassifier(dummy.DummyClassifier):
    label = "Dummy model: classification"
    node_type = "dummyclf"
    parent = "models"
    problem = "classification"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "strategy": ["stratified", "most_frequent", "prior", "uniform"],
    }


class KNeighborsClassifier(neighbors.KNeighborsClassifier):
    label = "KNN Classifier"
    node_type = "knnc"
    parent = "models"
    problem = "classification"
    url = "https://i.imgur.com/U9EFqYj.png"
    modifiable_params = {
        "n_neighbors": [5, 3, 7, 9]
    }


class XGBClassifier(xgboost.XGBClassifier):
    label = "XGBoost Classifier"
    node_type = "xgbclf"
    parent = "models"
    problem = "classification"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {}


class RandomForestClassifier(ensemble.RandomForestClassifier):
    label = "Random Forest Classifier"
    node_type = "rfc"
    parent = "models"
    problem = "classification"
    url = "/static/images/icons/random_forests.png"
    modifiable_params = {
        "n_estimators": [10, 20, 50, 100, 200, 500],
        "max_depth": [None, 3, 5, 7, 9, 12, 15],
        "max_features": ["auto", 0.1, 0.2, 0.5, 0.7, 0.9, 1]
    }


class SGDClassifier(linear_model.SGDClassifier):
    label = "SGD classifier"
    node_type = "sgdclf"
    parent = "models"
    problem = "classification"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "loss": ["hinge", "log", "modified_huber",
                 "perceptron", "squared_loss", "huber"],
        "penalty": ["none", "l2", "l1", "elasticnet"],
        "l1_ratio": [0.15, 0.01, 0.05, 0.1, 0.2, 0.5, 0.75, 0.9],
        "learning_rate": ["optimal", "constant", "invscaling", "adaptive"]
    }


class LinearSVC(svm.LinearSVC):
    label = "Linear SVC"
    node_type = "lsvcclf"
    parent = "models"
    problem = "classification"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "penalty": ["l2", "l1"],
        "C": [1, 0.01, 0.1, 0.5, 2, 5, 10],
        "fit_intercept": [True, False],
        "max_iter": [200, 50, 100, 500, 1000],
    }


class SVC(svm.SVC):
    label = "Support Vector Classifier"
    node_type = "svcclf"
    parent = "models"
    problem = "classification"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "gamma": [1, 0.01, 0.1, 0.5, 2, 5, 10],
        "degree": [3, 1, 2, 5],
        "C": [1, 0.01, 0.1, 0.5, 2, 5, 10],
        "kernel": ["rbf", "poly", "sigmoid"],
        "max_iter": [200, 50, 100, 500, 1000],
    }


class NuSVC(svm.NuSVC):
    label = "Nu-SVC"
    node_type = "nusvcclf"
    parent = "models"
    problem = "classification"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "nu": [0.5, 0.01, 0.1, 0.2, 0.7, 0.85, 1],
        "gamma": [1, 0.01, 0.1, 0.5, 2, 5, 10],
        "degree": [3, 1, 2, 5],
        "kernel": ["rbf", "linear", "poly", "sigmoid"],
        "max_iter": [200, 50, 100, 500, 1000]
    }


class DecisionTreeClassifier(tree.DecisionTreeClassifier):
    label = "Decision Tree Classifier"
    node_type = "dtclf"
    parent = "models"
    problem = "classification"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "max_depth": [None, 3, 5, 7, 9, 12],
    }


class ExtraTreeClassifier(tree.ExtraTreeClassifier):
    label = "Extra Tree Classifier"
    node_type = "extraclf"
    parent = "models"
    problem = "classification"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "max_depth": [None, 3, 5, 7, 9, 12],
    }


"""
======== Clustering ========
"""


class KMeans(cluster.KMeans):
    label = "K-Means Clustering"
    node_type = "kmc"
    parent = "models"
    problem = "clustering"
    url = "/static/images/icons/knn.png"
    modifiable_params = {
        "n_clusters": [8, 2, 3, 4, 5, 6, 7, 9, 10, 15, 20],
    }


class DBSCAN(cluster.DBSCAN):
    label = "DBSCAN Clustering"
    node_type = "dbscan"
    parent = "models"
    problem = "clustering"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "eps": [0.5, 0.01, 0.05, 0.1, 0.2, 1, 2, 5],
    }


class Birch(cluster.Birch):
    label = "Birch Clustering"
    node_type = "birch"
    parent = "models"
    problem = "clustering"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "threshold": [0.5, 0.1, 0.2, 0.75, 0.95],
    }


class AgglomerativeClustering(cluster.AgglomerativeClustering):
    label = "Agglomerative Clustering"
    node_type = "agglomerative"
    parent = "models"
    problem = "clustering"
    url = "/static/images/icons/hierarchical_clustering.png"
    modifiable_params = {
        "n_clusters": [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20],
        "linkage": ["ward", "complete", "average", "single"]
    }


class MeanShift(cluster.MeanShift):
    label = "MeanShift Clustering"
    node_type = "meanshift"
    parent = "models"
    problem = "clustering"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "bandwidth": [0.5, 0.05, 0.1, 0.2, 1, 2, 5, 10],
        "min_bin_freq": [1, 2, 3, 5, 10, 20],
        "cluster_all": [True, False]
    }


class BernoulliNB(naive_bayes.BernoulliNB):
    label = "Naive Bayes: Bernoulli"
    node_type = "bernoulli_nb"
    parent = "models"
    problem = "clustering"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "alpha": [1, 0.1, 0.2, 0.5, 0.7, 0.85],
    }


class GaussianNB(naive_bayes.GaussianNB):
    label = "Naive Bayes: Gaussian"
    node_type = "gauss_nb"
    parent = "models"
    problem = "clustering"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {}


class MultinomialNB(naive_bayes.MultinomialNB):
    label = "Naive Bayes: Multinomial"
    node_type = "multi_nb"
    parent = "models"
    problem = "clustering"
    url = "/static/images/icons/Cleaning.png"
    modifiable_params = {
        "alpha": [1, 0.1, 0.2, 0.5, 0.7, 0.85],
    }


# Get the list of all the classes defined here
# https://stackoverflow.com/a/1796247/6655150
all_classes = [obj for (name, obj) in
               inspect.getmembers(sys.modules[__name__],
                                  inspect.isclass)]
