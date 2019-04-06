import plotly.graph_objs as go
import numpy as np


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

def scatterplot(x, y, z, **kwargs):

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
