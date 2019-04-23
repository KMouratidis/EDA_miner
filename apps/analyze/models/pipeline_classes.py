"""
    This module serves
"""

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin

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


class InputFile(BaseEstimator, TransformerMixin):
    modifiable_params = {}

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


class DataCleaner(InputFile):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


class DataImputater(InputFile):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


class TwitterAPI(InputFile):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


class CustomClassifier(BaseEstimator, ClassifierMixin):
    def fit(self, X, y=None):
        return self

    def predict(self, X):
        return np.ones(X.shape[0])


# For EVERY model that is expected to have parametrization
# you are expected to give its class a `modifiable_params`
# dict with keys being the function argument and values the
# allowed set of values (make it limited, i.e. few choices)
# Also, the first is assumed to be the default value

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

GaussianNB.modifiable_params = {}

MultinomialNB.modifiable_params = {
    "alpha": [1, 0.1, 0.2, 0.5, 0.7, 0.85],
}

SimpleImputer.modifiable_params = {
    "strategy": ["mean", "median", "most_frequent"]
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