"""
    This module contains the implementations of graphing
    functions, and will probably contain core logic for KPI
    creation. This should mirror the graphs2d module.

    You can freely write code in this module.
"""

from utils import hard_cast_to_float
from apps.analyze.models.utils import baseline

import plotly.graph_objs as go


########## Helper functions ##########

def _base_graph(x, y, **params):
    raise NotImplementedError


## Similar to graphs2d, but might need
## three or more values in the tuple
graph_configs = {
    'baseline': (True, True),
 }


########## Graph functions ##########
## Functions below here implement the various graphs
## These should return plotly traces (i.e. lists of `go` objects)

def baseline_graph(df, xvars, yvars, secondary_yvars):
    return [
        go.Scatter(
            x=df[xvars],
            y=baseline(df[yvar].apply(hard_cast_to_float)),
            mode='lines',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': (0,100,255)}
            },
            name=f"Baseline for {' '.join(yvar.split()[:2])}",
        ) for yvar in yvars] + [
        # one scatter for each y variable
        go.Scatter(x=df[xvars],
                   y=df[yvar].apply(hard_cast_to_float),
                   mode='lines+markers',
                   marker={
                       'size': 8,
                       'line': {
                           'width': 0.5,
                           'color': 'rgb(210, 40, 180)'
                        },
                       'color': 'rgb(180, 35, 180)'
                   },
                   name=yvar
            ) for yvar in yvars] + [
                # Bar plot for the second variable
                go.Bar(
                    x=df[xvars],
                    y=df[secondary_yvars].apply(hard_cast_to_float),
                    name="Bars"
                )
            ]

def other_graph(x, y):
    raise NotImplementedError
    return [_base_graph(x, y, mode="markers")]
