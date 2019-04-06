"""
    This module will be used to show network data.

    You can write code in this module, but keep in
    mind that it may be moved later on to lower-level
    modules.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto

from server import app
from utils import r, create_dropdown

import plotly.graph_objs as go


def Network_Options(options, results):

    return [html.H4("Not implemented yet.")]
