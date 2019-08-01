"""

"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
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
