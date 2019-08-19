"""
This module *will* contain the DashboardMaker, a tool that helps you make \
your own dashboards, or at least get graphs and text in, move them around \
and resize them.

Global Variables:
    - Dashboard_Options: Generate the layout of the dashboard.

Dash callbacks:
    - display_output: Currently dummy function to create the dashboard.

Notes to others:
    Feel free to work both here and in the `dash_rnd`, we really need it.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from .server import app
from dash_rnd import ResizeDraggable


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
    """
    Currently dummy function to create the dashboard.

    Args:
        n_clicks (int): Number of button clicks.
        children (list): Current items on the dashboard.

    Returns:
        A Dash element or list of elements.
    """

    children.append(
        ResizeDraggable(
            id=f'some_id_{len(children)}',
            children=[
                dcc.Graph(
                    id=f'example-graph_{len(children)}',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar',
                             'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Dash Data Visualization',
                        }
                    },
                )
            ],
            label='mah cool label',
            style={"border": "3px dashed", "width": "200px",
                   "height": "200px"},
            x=20*len(children),
            y=20*len(children),
            minWidth=400,
            minHeight=300
        ))

    return children
