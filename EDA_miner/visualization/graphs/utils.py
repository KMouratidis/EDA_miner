"""
Utilities for the visualization app. This file might later be merged with \
another; it is still in active development.

Functions:
    - create_button: Create an image-button for the selected graph type.
"""

import dash_html_components as html

graphs3d_choices = {
    "scatter3d": "3D Scatterplot"
}


def create_button(graph_type, graph_label, n):
    """
    Create an image-button for the selected graph type.

    Args:
        graph_type (str): The type of graph, and value of the button. See \
                          graphs2d_choices for options.
        graph_label (str): The label displayed on the button.
        n (int): The number/id of the button (needed when creating buttons \
                 per trace).

    Returns:
        A list of Dash elements.
    """

    img_name = "/static/images/graph_images/" + graph_type + ".png"

    return html.Div([

        html.P(graph_label,
               style={"marginBottom": "0",
                      "textAlign": "center"}),

        html.Button([html.Img(src=img_name, height=45, width=45)],
                    id=graph_type + f"_{n}",
                    style={"margin": "10px", "height": "60px",
                           "width": "70px"})

    ], style={"display": "inline-block", "margin": "10px"})
