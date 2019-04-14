"""
    TBW...
"""

from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
import numpy as np


class InputFile(BaseEstimator, TransformerMixin):
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
