"""
This module collects functions and utilities for KPI visualization
but may also be used to add other options and core implementation logic.

Functions:
    - baseline_graph: Creates a baseline graph: a lineplot for the \
                        timeseries and its baseline, and a barchart.

Notes to others:
    Feel free to write code here either to improve current or to add
    new functionality. This part is in need of both customization and
    presets.
"""

from utils import hard_cast_to_float
from apps.analyze.models.utils import baseline

import plotly.graph_objs as go


########## Helper functions ##########


# Similar to graphs2d, but might need
# three or more values in the tuple
graph_configs = {
    'baseline': (True, True),
 }


########## Graph functions ##########
# Functions below here implement the various graphs
# These should return plotly traces (i.e. lists of `go` objects)

def baseline_graph(df, xvars, yvars, secondary_yvars):
    """
    Creates a baseline graph: a lineplot for the timeseries and
    its baseline, and a barchart.

    Args:
        df (`pd.DataFrame`): The data.
        xvars (str): Column of `df`; `x-axis`.
        yvars (str or list(str)): Column(s) of `df`; lineplot(s).
        secondary_yvars (str):  Column of `df`; bar-chart.

    Returns:
        list: Plotly traces.
    """

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
