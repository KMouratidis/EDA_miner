"""
This module is about visualizing text data.

Global Variables:
    - Sidebar: To be used for creating side-menus.

Functions:
    - TextViz_Options: Generate the layout of the dashboard.

Dash callbacks:
    - plot_graph_text: Currently only word cloud visualizations are \
                       supported, from given text.

Notes to others:
    Contributions are encouraged here. Main functionality is still \
    lacking in this part. You can use this module to add new buttons, \
    input, or other interface-related, element, or maybe a new type \
    of text visualizations (in which case implement it in a new file \
    `graphs.textviz.py`). Like with other modules, working on exporting \
    network graphs is encouraged. Finally, adding new visualization types \
    is very welcome as well, but avoid loading huge word vectors files \
    at this stage of development.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from .server import app
from .graphs import textviz

from flask_login import current_user


Sidebar = []


def TextViz_Options():
    """
    Generate the layout of the dashboard.

    Optional Args:
        options (list(dict)): Not relevant; here only for API compatibility.

    Returns:
        A Dash element or list of elements.
    """

    return [

        # The main content
        html.Div([
            html.Div([
                dcc.Textarea(id="text_area"),
                html.Button("Create wordcloud", id="make_wordcloud"),
            ], className="col-sm-3"),

            html.Div([
                # The graph itself
                html.Img(id='wordcloud_img',
                         src="/static/images/default_wordcloud.png"),
            ], className="col-sm-8")
        ], className="row"),

        # The tab menu
        html.H4("No menu yet", id="textviz_menu")
    ]


@app.callback(
    Output("wordcloud_img", "src"),
    [Input("make_wordcloud", "n_clicks")],
    [State("text_area", "value")])
def plot_graph_text(n_clicks, text):
    """
    Currently only word cloud visualizations are supported,
    from given text.

    Args:
        n_clicks (int): Number of button clicks.
        text (str): User-provided text used to create a word cloud.

    Returns:
        str: the image encoded appropriately to be set as the 'src' \
             value of the `img` element
    """

    user_id = current_user.username

    if text is not None and len(text.split()) > 1:
        textviz.create_wordcloud(text, user_id)
        return f"static/images/{user_id}_wordcloud.png"

    else:
        # invalid arguments or Dash's first pass
        return "/static/images/default_wordcloud.png"
