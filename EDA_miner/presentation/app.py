import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from redis import Redis
import dill


redis_conn = Redis()

external_stylesheets = []
app = dash.Dash(__name__, requests_pathname_prefix="/graphs/",
                assets_external_path="http://127.0.0.1:8000/static/")


app.layout = html.Div(children=[
    dcc.Location(id="url", refresh=False),

    html.Div(id="main_app"),
])


@app.callback(Output("main_app", "children"),
              [Input("url", "pathname")])
def render_graph(pathname):

    if pathname == "/Lunch break":
        return [html.Div(html.Img(src="https://ssl-static.libsyn.com/p/assets/f/9/b/e"
                                      "/f9be4c0c8437f1aa/LunchBreakLogo.jpg"),
                         style={"textAlign": "center"})]

    elif pathname is not None:
        pathname = pathname.replace("/graphs/", "")
        pathname = pathname.replace("__", " ").replace('---', '#')

    redis_data = redis_conn.get(f"{pathname}")
    if redis_data is not None:
        figure = dill.loads(redis_data)

    else:
        figure = {
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization',
            }
        }

    return [
        html.H1(children=f'Hello Dash, {pathname}'),
        dcc.Graph(id='example-graph', figure=figure)
    ]


if __name__ == '__main__':
    app.run_server(port=8081, debug=True)
