"""
This module collects functions and utilities for 3D visualization.

Functions:
    - scatterplot3d: Create a 3D scatterplot.

Notes to others:
    Feel free to write code here either to improve current or to add \
    new functionality. What is particularly needed is new graph types.
"""

import plotly.graph_objs as go


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

    return [go.Scatter3d(x=x, y=y, z=z, **default_options)]
