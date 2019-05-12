"""
This module will collect all unchanging views and dash components
(buttons, sidemenus, etc) so that the code in index.py is cleaner
and abstracted.

Global variables:
    - SideBar: The left sidebar, meant to house the logo, and \
               a few extra buttons for non-app functionality.
    - MainMenu: The high-level tabs, and two placeholders for the \
                low-level tabs plus a `dash_table.DataTable`.
    - SideBar: The right sidebar, meant to be used for elements \
               that interact with the important parts of dash and \
               providing any interactivity, customization, and \
               other options.

Functions:
    - serve_layout: The layout of our app. Defined in a function \
                    so as to generate different `session_id`s.

Dash callbacks:
    - button_toggle: On click show/hide the external links.

Notes to others:
    You should probably not write code here, unless you're:
        - adding a new button, external link, or similar to the sidebar,
        - creating a login functionality,
        - adding a new top-level menu tab, or other new feature.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import encode_image

import dash_table

import uuid




SideBar = [

    html.Img(id="app_logo", src=encode_image("assets/images/y2d.png")),
    html.Br(),

    html.Button('Dark/Light theme', id="dark_theme"),

    # Collapsible button with external links
    html.Button([
        html.Span('External links'),
        html.I("", className="fa fa-caret-down", id="external_links_caret"),
    ], id='button_collapse', n_clicks=0),
    # Stuff inside the collapsible
    html.Div(id='sidebar_collapsible_button', children=[
        html.Ul([
            html.Li(html.A([
                        html.Span("GitHub repo  "),
                        html.I(className="fab fa-github", id="github_link"),
            ], href="https://github.com/KMouratidis/EDA_miner_public",
                target="_blank")),
            html.Li(html.A([
                    html.Span("Dash docs  "),
                    html.I(className="fas fa-external-link-square-alt",
                           id="dash_link")
            ], href="https://dash.plot.ly/",
                target="_blank")),

            html.Li(html.A([
                    html.Span("Our docs  "),
                    html.I(className="fas fa-external-link-square-alt",
                           id="dev_link")
            ], href="https://kmouratidis.github.io/EDA_miner_public/docs/",
                target="_blank")),
        ])
    ]),
]


MainMenu = [

    # Tabs, level-1
    html.Div(children=[
        dcc.Tabs(id="high_level_tabs", value='data', children=[
            dcc.Tab(label='Data view', value='data',
                    id="data"),
            dcc.Tab(label='Explore & Visualize', value='EDA',
                    id="EDA"),
            dcc.Tab(label='Analyze & Predict', value='modelling',
                    id="modelling"),
        ]),
    ]),

    # Placeholder for level-2 tabs
    html.Div(id="selected_subpage"),

    # Due to a known Dash bug, the table
    # must be present in the first layout
    html.Div(id="table_container", children=[
        dash_table.DataTable(id='table',),
    ], style={"display": "none"}),
]


SideBar2 = [
    html.H3("Tab menu"),
    # Placeholder for low-level submenus, if needed
    html.Div(children=[], id="low_level_tabs_submenu")
]


# When the sidebar button is clicked, collapse the div
@app.callback(Output('sidebar_collapsible_button', 'style'),
              [Input('button_collapse', 'n_clicks')],)
def button_toggle(n_clicks):
    """
    On click show/hide the external links.

    Args:
        n_clicks: int, number of times the button was clicked.

    Returns:
        A style dict modifying the display CSS attribute.
    """

    if n_clicks % 2 == 1:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


def serve_layout():
    """
    The layout of our app needs to be inside a function
    so that every time some new session starts a new
    session_id is generated.
    """

    session_id = f"python_generated_ssid_{uuid.uuid4()}"

    return html.Div(children=[

        html.H2(session_id, id="user_id", style={"display": "none"}),


        html.Div([
            # Sidebar / menu
            html.Div(children=SideBar, className="col-sm-2 ml-auto",
                     id="sidebar",
                     style={"display": "inline-block"}),

            # main Div
            html.Div(children=MainMenu, className="col-sm-9 ml-auto",
                     id="mainmenu",
                     style={"display": "inline-block"}),

            # Sidebar / menu
            html.Div(children=SideBar2, className="col-sm-1 ml-auto",
                     id="sidebar2",
                     style={"display": "inline-block"}),

        ], className="row")


    ], className="container",
                    id="main_page")
