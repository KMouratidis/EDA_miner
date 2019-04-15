"""
    TBW...
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import encode_image
from apps.exploration.graphs import word_cloud


def TextViz_Options(options, results):
    return html.Div(children=[

        html.Div([

            html.Div([
                dcc.Textarea(id="text_area",
                             rows="100",
                             cols="25"),
                html.Button("Create wordcloud", id="make_wordcloud"),
            ], className="three columns offset-by-one.column"),


            html.Div([
                # The graph itself
                html.Img(id='returned_image',
                         src=encode_image("default_wordcloud.png"),
                         height=500,
                         width=700),
            ], className="seven columns")

        ], className="row"),

    ])



@app.callback(
    Output("returned_image", "src"),
    [Input("make_wordcloud", "n_clicks")],
    [State("text_area", "value"),
     State("user_id", "children")])
def plot_graph_text(n_clicks, text, user_id):

    if text is not None and len(text.split()) > 1:
        word_cloud.create_wordcloud(text, user_id)
        return encode_image(f"static/images/{user_id}_wordcloud.png")

    else:
        # invalid arguments or Dash's first pass
        return encode_image("default_wordcloud.png")
