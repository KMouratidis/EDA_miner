"""
This module contains the implementations of graphing functions. \
I skipped adding docstrings for every function since most of them \
are one-liners anyway and should be pretty obvious.

Functions:
    - scatterplot: Create a 2D scatterplot.
    - line_chart: Create a lineplot.
    - bubble_chart: Create a bubble chart.
    - filledarea: Create a lineplot with filled areas.
    - errorbar: Create a lineplot with error bars (currently fixed).
    - histogram: Create a histogram.
    - heatmap: Create a heatmap of column correlations.
    - density2d: Create a heatmap.

Notes to others:
    Feel free to write code here either to improve current or to add \
    new functionality. Also feel free to add or tamper with styles \
    and/or helper functions.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.tools as tls
import plotly.graph_objs as go


########## Helper functions ##########

def _simple_scatter(x, y, **kwargs):
    """
    Internal function used to create a lot of other plots.
    """

    default_options = {
        "opacity": 0.7,
        "marker": {'size': 15,
                   'line': {'width': 0.5,
                            'color': 'white'}
                   },
        "mode": "markers",
    }

    default_options.update(kwargs)

    return go.Scatter(x=x, y=y, **default_options)


## Graph_type: [needs_yvar, allows_multi]
# specify one line per chart, if the first is False,
# set the second to False too
graph_configs = {
    'line_chart': (True, True),
    'scatterplot': (True, True),
    'histogram': (False, False),
    'heatmap': (True, False),
    'bubble_chart': (True, True),
    'pie': (False, False),
    'filledarea': (True, True),
    'errorbar': (True, True),
    'density2d': (True, False),
    'pairplot': (True, True)
 }


########## Graph functions ##########
# Functions below here implement the various graphs
# These should return plotly traces (i.e. lists of `go` objects)

def scatterplot(x, y, **kwargs):
    """
    Create a 2D scatterplot.

    Args:
        x (iterable): Values for x-axis.
        y (iterable): Values for y-axis.
        **params: Any other keyword argument passed to `go.Scatter`.

    Returns:
        `go.Scatter`
    """

    return _simple_scatter(x, y, mode="markers", **kwargs)


def line_chart(x, y, **kwargs):
    """
    Create a lineplot.

    Args:
        x (iterable): Values for x-axis.
        y (iterable): Values for y-axis.
        **kwargs: Any other keyword argument passed to `go.Scatter`.

    Returns:
        `go.Scatter`
    """

    return _simple_scatter(x, y, mode="lines", **kwargs)


def bubble_chart(x, y, size, **kwargs):
    """
    Create a bubble chart.

    Args:
        x (iterable): Values for x-axis.
        y (iterable): Values for y-axis.
        size (iterable): Sized of bubbles.
        **kwargs: Any other keyword argument passed to `go.Scatter`.

    Returns:
        `go.Scatter`
    """

    marker = dict(size=size,
                  sizemode='area',
                  sizeref=2. * max(size) / (40. ** 2),
                  sizemin=4)

    return _simple_scatter(x, y, mode="markers", marker=marker, **kwargs)


def filledarea(x, y, **kwargs):
    """
    Create a lineplot with filled areas.

    Args:
        x (iterable): Values for x-axis.
        y (iterable): Values for y-axis.
        **kwargs: Any other keyword argument passed to `go.Scatter`.

    Returns:
        `go.Scatter`
    """

    return _simple_scatter(x, y, mode=None, fill='tonexty', **kwargs)


def errorbar(x, y, **kwargs):
    """
    Create a lineplot with error bars (currently fixed).

    Args:
        x (iterable): Values for x-axis.
        y (iterable): Values for y-axis.
        **kwargs: Any other keyword argument passed to `go.Scatter`.

    Returns:
        `go.Scatter`
    """

    std = np.zeros(y.shape) + y.std()

    error_y = dict(
        type='data',
        symmetric=False,
        array=std,
        arrayminus=std
    )

    return _simple_scatter(x, y, mode=None, error_y=error_y, **kwargs)


def histogram(x, **kwargs):
    """
    Create a histogram.

    Args:
        x (iterable): Values for the histogram.
        **kwargs: Any other keyword argument passed to `go.Histogram`.

    Returns:
        `go.Histogram`
    """

    return go.Histogram(x=x, **kwargs)


def heatmap(x, y, **kwargs):
    """
    Create a histogram.

    Args:
        x (iterable): Values for x-axis.
        y (iterable): Values for y-axis.
        **kwargs: Any other keyword argument passed to `go.Histogram`.

    Returns:
        `go.Heatmap`
    """

    # Make sure they are in the appropriate shape
    if not (len(x.shape) > 1 and x.shape[1] < 2):
        x = np.atleast_2d(x).T
    if not (len(y.shape) > 1 and y.shape[1] < 2):
        y = np.atleast_2d(y).T

    data = np.concatenate([x, y], 1)
    return go.Heatmap(z=np.corrcoef(data.T), **kwargs)


def density2d(x, y, **kwargs):
    """
    Create a histogram.

    Args:
        x (iterable): Values for the histogram.
        **kwargs: Any other keyword argument passed to `go.Histogram2dContour`.

    Returns:
        list[`go.Scatter`, `go.Histogram2dContour`]
    """

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

    histogram_params.update(kwargs)

    return [
        _simple_scatter(x, y, mode='markers', marker=marker),
        go.Histogram2dContour(x=x, y=y, **histogram_params),
    ]


def pairplot(x):
    size = x.shape[1]
    fig, axes = plt.subplots(size, size)

    for i in range(size):
        for j in range(size):
            ax = axes[i][j]
            if i == j:
                ax.hist(x.iloc[:, j])
            else:
                ax.scatter(x.iloc[:, i], x.iloc[:, j])

    plotly_fig = tls.mpl_to_plotly(fig)
    plt.clf()

    return plotly_fig
