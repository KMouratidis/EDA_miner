"""
This module contains the implementations of graphing functions. \
I skipped adding docstrings for every function since most of them \
are one-liners anyway and should be pretty obvious.

Functions:
    - scatterplot: Create a 2D scatterplot.
    - line_chart: Create a lineplot.
    - bubble_chart: Create a bubble chart.
    - bar: Create a bar chart.
    - filledarea: Create a lineplot with filled areas.
    - errorbar: Create a lineplot with error bars (currently fixed).
    - histogram: Create a histogram.
    - heatmap: Create a heatmap of column correlations.
    - density2d: Create a heatmap.
    - pie: Create a pie chart.
    - pairplot: Create a grid of plots with matplotlib.

Notes to others:
    Feel free to write code here either to improve current or to add \
    new functionality. Also feel free to add or tamper with styles \
    and/or helper functions.
"""

from utils import hard_cast_to_float

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


########## Graph functions ##########
# Functions below here implement the various graphs
# These should return plotly traces (i.e. lists of `go` objects)

def scatterplot(x, y, z=None, **kwargs):
    """
    Create a 2D scatterplot. Parameter `z` is for a unified API.

    Args:
        x (iterable): Values for x-axis.
        y (iterable): Values for y-axis.
        **params: Any other keyword argument passed to `go.Scatter`.

    Returns:
        `go.Scatter`
    """

    return _simple_scatter(x, y, mode="markers", **kwargs)


def line_chart(x, y, z=None, **kwargs):
    """
    Create a lineplot. Parameter `z` is for a unified API.

    Args:
        x (iterable): Values for x-axis.
        y (iterable): Values for y-axis.
        **kwargs: Any other keyword argument passed to `go.Scatter`.

    Returns:
        `go.Scatter`
    """

    return _simple_scatter(x, y, mode="lines", **kwargs)


def bubble_chart(x, y, size, z=None, **kwargs):
    """
    Create a bubble chart. Parameter `z` is for a unified API.

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


def bar(x, y, z=None, **kwargs):
    """
    Create a bar chart. Parameter `z` is for a unified API.

    Args:
        x (iterable): Values for x-axis.
        y (iterable): Values for y-axis.
        **kwargs: Any other keyword argument passed to `go.Bar`.

    Returns:
        `go.Bar`
    """

    return go.Bar(x=x, y=y.apply(hard_cast_to_float), name="Bars")


def filledarea(x, y, z=None, **kwargs):
    """
    Create a lineplot with filled areas. Parameter `z` is for a unified API.

    Args:
        x (iterable): Values for x-axis.
        y (iterable): Values for y-axis.
        **kwargs: Any other keyword argument passed to `go.Scatter`.

    Returns:
        `go.Scatter`
    """

    return _simple_scatter(x, y, mode=None, fill='tonexty', **kwargs)


def errorbar(x, y, z=None, **kwargs):
    """
    Create a lineplot with error bars (currently fixed). Parameter `z` is \
    for a unified API.

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


def histogram(x, y=None, z=None, **kwargs):
    """
    Create a histogram. Parameters `y` and `z` are for a unified API.

    Args:
        x (iterable): Values for the histogram.
        y: Not applicable.
        z: Not applicable.
        **kwargs: Any other keyword argument passed to `go.Histogram`.

    Returns:
        `go.Histogram`
    """

    return go.Histogram(x=x, **kwargs)


def heatmap(x, y, z=None, **kwargs):
    """
    Create a histogram. Parameter `z` is for a unified API.

    Args:
        x (iterable): Values for x-axis.
        y (iterable): Values for y-axis.
        z: Not applicable.
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


def density2d(x, y, z=None, **kwargs):
    """
    Create a histogram. Parameter `z` is for a unified API.

    Args:
        x (iterable): Values for the density x-axis.
        y (iterable): Values for the density y-axis.
        z: Not applicable.
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


def pie(x, y, z=None, **kwargs):
    """
    Create a pie chart. Parameter `z` is for a unified API.

    Args:
        x (iterable): The labels for the pie-chart regions.
        y (iterable): The values.
        z: Not applicable.
        **kwargs: Any other keyword argument passed to `go.Histogram2dContour`.

    Returns:
        `go.Pie`
    """

    return go.Pie(labels=x, values=y)


def pairplot(x, y=None, z=None, **kwargs):
    """
    Create a grid of plots with matplotlib. Each row/col represents one \
    column from the dataframe. For the main diagonal histograms are \
    plotted, and for everywhere else scatterplots.

    Args:
        x (`pd.DataFrame`): The dataset.
        y: Not applicable.
        z: Not applicable.

    Returns:
        A plotly figure.

    Implementation details:
        Clipping is needed because the histogram may be a float \
        and floats often have rounding errors (here the negative \
        throws a plotly error.

        The first two parameters returned by `ax.hist` are two arrays, \
        but the third causes the problem. It is a collection of patches, \
        which need to be updated. Example of what that looks like:
            `Rectangle(xy=(4.3, 0), width=0.36, height=9, angle=0)`

        I don't know why but it seems it ONLY accepts the first patch \
        to be changed. When I tried looping over all of them it threw \
        the same error.
    """

    size = x.shape[1]
    fig, axes = plt.subplots(size, size)

    for i in range(size):
        for j in range(size):
            ax = axes[i][j]
            if i == j:
                ax = ax.hist(x.iloc[:, j])

                prev_xy = getattr(ax[2][0], "xy")
                setattr(ax[2][0], "xy", (prev_xy[0] + 1e-8,
                                         prev_xy[1] + 1e-8))

                axes[i][j] = (ax[0], ax[1], ax[2])

            else:
                ax.scatter(x.iloc[:, i], x.iloc[:, j])

    plotly_fig = tls.mpl_to_plotly(fig)
    plt.clf()

    return plotly_fig


def scatterplot3d(x, y, z, **kwargs):
    """
    Create a 3D scatterplot.

    Args:
        x  (iterable): `x-axis` data.
        y  (iterable): `y-axis` data.
        z  (iterable): `z-axis` data.
        **kwargs: Anything accepted by `plotly.graph_objs.Scatter3d`.

    Returns:
        list: Plotly traces.
    """

    default_options = {
        "mode": 'markers',
        "marker": {
            "size": 12,
            "color": z,
            "colorscale": "Viridis",
            "opacity": 0.8
        }
    }

    default_options.update(kwargs)

    return go.Scatter3d(x=x, y=y, z=z, **default_options)



# Graph_type: [graph_name, needs_yvar, allows_multi, needs_zvar, func]
# specify one line per chart, if the first is False,
# set the second to False too
graph2d_configs = {
    'line_chart': ("Line Graph", True, True, False, line_chart),
    'scatterplot': ("Scatter Plot", True, True, False, scatterplot),
    'barchart': ("Bar chart", True, False, False, bar),
    'histogram': ("Histogram", False, False, False, histogram),
    'heatmap': ("Heatmap", True, False, False, heatmap),
    'bubble_chart': ("Bubble chart", True, True, False, bubble_chart),
    'pie': ("Pie chart", False, False, False, pie),
    'filledarea': ("Filled Area", True, True, False, filledarea),
    'errorbar': ("Error Bar", True, True, False, errorbar),
    'density2d': ("2D Density", True, False, False, density2d),
    'pairplot': ("Pair-plot (matplotlib)", True, True, False, pairplot),

    # 3D plots
    'scatterplot3d': ("Scatter 3D", True, False, True, scatterplot3d)
 }