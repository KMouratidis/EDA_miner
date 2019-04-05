"""
    This module contains the implementations of graphing
    functions. Every graph has its own line in the config
    which indicates if the graph needs both X and Y variables
    and whether the Y variables should be multiple.

    You can freely write code in this module, without worries.
"""

import plotly.graph_objs as go
import numpy as np


# TODO: add layout parameters


########## Helper functions ##########

def _simple_scatter(x, y, **params):
    default_options = {
        "opacity": 0.7,
        "marker": {'size': 15,
                'line': {'width': 0.5,
                         'color': 'white'}
            },
        "mode":"markers",
    }

    default_options.update(params)

    return go.Scatter(x=x, y=y, **default_options)


## Graph_type: [needs_yvar, allows_multi]
# specify one line per chart, if the first is False,
# set the second to False too
graph_configs = {
    'line_chart': (True, True),
    'scatterplot': (True, True),
    'histogram': (False, False),
    'heatmap': (True, False),
    'bubble_chart': (True, False),
    'pie': (False, False),
    'filledarea': (True, True),
    'errorbar': (True, True),
    'density2d': (True, False),
 }


########## Graph functions ##########
## Functions below here implement the various graphs
## These should return plotly traces (i.e. lists of `go` objects)

def scatterplot(x, y, **kwargs):
    return [_simple_scatter(x, y, mode="markers", **kwargs)]

def line_chart(x, y, **kwargs):
    return [_simple_scatter(x, y, mode="line", **kwargs)]

def histogram(x, **kwargs):
    return [go.Histogram(x=x, **kwargs)]

def heatmap(x, y, **kwargs):

    if not (len(x.shape)>1 and x.shape[1] <2):
        x = np.atleast_2d(x).T

    if not (len(y.shape)>1 and y.shape[1] <2):
        y = np.atleast_2d(y).T


    data = np.concatenate([x,y], 1)
    return [go.Heatmap(z=np.corrcoef(data.T), **kwargs)]

def bubble_chart(x, y, size, **kwargs):
    marker = dict(size=size,
                  sizemode='area',
                  sizeref=2.*max(size)/(40.**2),
                  sizemin=4)

    return [_simple_scatter(x,y, mode="markers", marker=marker, **kwargs)]

def filledarea(x, y, **kwargs):
    return [_simple_scatter(x, y, mode=None, fill='tonexty', **kwargs)]

def errorbar(x, y, **kwargs):
    std = np.zeros(y.shape) + y.std()

    error_y = dict(
        type='data',
        symmetric=False,
        array=std,
        arrayminus=std
    )

    return [_simple_scatter(x, y, mode=None, error_y=error_y, **kwargs)]

def density2d(x, y, **kwargs):
    marker = {
        "color": 'rgb(102,0,0)',
        "size": 2,
        "opacity": 0.2,
    }
    histogram_params = {
        "name": "density",
        "ncontours": 20,
        "colorscale": "Hot",
        "reversescale": True,
        "showscale": False
    }

    return [
        _simple_scatter(x, y, mode='markers', marker=marker),
        go.Histogram2dContour(x=x, y=y, **histogram_params, **kwargs),
    ]
