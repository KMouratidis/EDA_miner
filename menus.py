"""
    This module will collect all unchanging views and dash
    components (buttons, sidemenus, etc) so that the code
    in index.py is cleaner and abstracted.

    You should probably not write code here.
"""

import dash_core_components as dcc
import dash_html_components as html

import dash_table

from server import app
from utils import mapping, cleanup, r, encode_image

import uuid




SideBar = [

    html.Img(id="app_logo", src=encode_image("assets/images/y2d.png")),
    html.Br(),

    html.H2("Sidemenu1"),
    html.Button('Dark/Light theme', id="dark_theme"),

    # Collapsible button with external links
    html.Button([
        html.Span('External links'),
        html.I("", className="fa fa-caret-down", style={"fontSize":"24px",
                                                 "verticalAlign":"middle",
                                                 "paddingLeft":"5px"}),
    ], id='button_collapse', n_clicks=0),
    html.Div(id='sidebar_collapsible_button', children=[
        html.Ul([
            html.Li(html.A([
                    html.Span("GitHub repo  "),
                    html.I(className="fab fa-github", style={"fontSize":"28px",
                                                             "verticalAlign":"bottom",
                                                             "paddingTop":"5px"}),

                    ], href="https://github.com/KMouratidis/EDA_miner",
                   target="_blank"),
                ),
            html.Li('I am just padded text'),
        ])
    ]),

    # Placeholder for low-level submenus, if needed
    html.H2("Sidemenu2"),
    html.Div(children=[], id="low_level_tabs_submenu")
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
    ], style={"display":"none"}),

]


def serve_layout():
    """
        The layout of our app needs to be inside a function
        so that every time some new session starts a new
        session_id is generated.
    """

    session_id = f"python_generated_ssid_{uuid.uuid4()}"

    return html.Div(children=[

        html.H2(session_id, id="user_id", style={"display":"none"}),

        # Sidebar / menu
        html.Div(children=SideBar, className="two columns", id="sidebar"),

        # main Div
        html.Div(children=MainMenu, className="nine columns", id="mainmenu"),

    ], className="row",
                    id="main_page")
