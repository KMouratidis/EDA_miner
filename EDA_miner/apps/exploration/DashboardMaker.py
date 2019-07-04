"""

"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc

from server import app
import layouts
from utils import create_dropdown
from apps.data.View import get_data
from apps.exploration.graphs import graphs2d

import plotly.graph_objs as go

import dash_rnd


Dashboard_Options = [

    html.Div([], style={
        'width': '95%',
        'height': '650px',
        'backgroundColor': '#DDCC33',
        'border': "3px solid"
    }, id="dashboard"),

    html.Button("Add component", id="add_dashboard_component", n_clicks=0)
]


@app.callback(Output('dashboard', 'children'),
              [Input('add_dashboard_component', 'n_clicks')],
              [State('dashboard', 'children')])
def display_output(n_clicks, children):
    children.append(
        dash_rnd.ResizeDraggable(
            id='some_id',
            children=[
                html.H4("Hello"),
                html.H5("This is still under active development."),
                html.H5("This prototype has trouble with Dash graphs."),
            ],
            label='mah cool label',
            style={"border": "3px dashed", "width": "200px",
                   "height": "200px"},
            x=20*len(children),
            y=20*len(children),
            minWidth=100,
            minHeight=100
        ))

    return children