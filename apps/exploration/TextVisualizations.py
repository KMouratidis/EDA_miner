"""
This module is about visualizing text data.

Global Variables:
    - Sidebar: To be used for creating side-menus.

Functions:
    - TextViz_Options: Generate the layout of the dashboard.

Dash callbacks:
    - plot_graph_text: Currently only word cloud visualizations are
                       supported, from given text.

Notes to others:
    Contributions are encouraged here. Main functionality is still
    lacking in this part. You can use this module to add new buttons,
    input, or other interface-related, element, or maybe a new type
    of text visualizations (in which case implement it in a new file
    `graphs.textviz.py`). Like with other modules, working on exporting
    network graphs is encouraged. Finally, adding new visualization types
    is very welcome as well, but avoid loading huge word vectors files
    at this stage of development.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import encode_image
from apps.exploration.graphs import word_cloud


Sidebar = []


def TextViz_Options(options, results):
    return html.Div(children=[

        html.Div([
            html.Div([
                dcc.Textarea(id="text_area"),
                html.Button("Create wordcloud", id="make_wordcloud"),
            ], className="three columns"),

            html.Div([
                # The graph itself
                html.Img(id='wordcloud_img',
                         src=encode_image("default_wordcloud.png")),
            ], className="seven columns")
        ], className="row"),
    ])


@app.callback(
    Output("wordcloud_img", "src"),
    [Input("make_wordcloud", "n_clicks")],
    [State("text_area", "value"),
     State("user_id", "children")])
def plot_graph_text(n_clicks, text, user_id):
    """
    Currently only word cloud visualizations are supported,
    from given text.

    Args:
        n_clicks (int): Number of button clicks.
        text (str): User-provided text used to create a word cloud.
        user_id (str): Session/user id.

    Returns:
        str: the image encoded appropriately to be set as the 'src'
             value of the `img` element
    """

    if text is not None and len(text.split()) > 1:
        word_cloud.create_wordcloud(text, user_id)
        return encode_image(f"static/images/{user_id}_wordcloud.png")

    else:
        # invalid arguments or Dash's first pass
        return encode_image("default_wordcloud.png")
