"""
This module will collect all unchanging views and dash components \
(buttons, sidemenus, etc) so that the code in index.py is cleaner \
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
import dash_html_components as html
import dash_table

from server import app
from utils import encode_image, r

import sd_material_ui
import visdcc

import uuid
import pickle
import pandas as pd
import os



static_dir = os.path.dirname(__file__)


SideBar = [

    html.Img(id="app_logo",
             src=encode_image(os.path.join(static_dir, "assets/images/y2d.png"))),

    html.Br(),

    visdcc.Run_js(id='theme_javascript'),
    html.Div(html.A('Dark/Light theme'), id="dark_theme", n_clicks=0,
             className="nav_item"),

    # Collapsible button with external links
    html.Div(html.A([
        html.Span('External links'),
        html.I(className="fa fa-caret-down", id="external_links_caret"),
    ]), id='button_collapse', n_clicks=0, className="nav_item"),
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
            ], href="http://docs.edaminer.com/",
                target="_blank")),
        ])
    ]),

    html.Br(),

    # Tabs, level-1
    html.Div(children=[

        html.Div(html.A([
            html.I(className="fas fa-database"),
            html.Span("Data view"),
        ]), n_clicks=0, id="data_link", className="nav_links"),

        html.Div(html.A([
            html.I(className="fas fa-eye"),
            html.Span("Explore & Visualize"),
        ]), n_clicks=0, id="explore_link", className="nav_links"),

        html.Div(html.A([
            html.I(className="fas fa-laptop-code"),
            html.Span("Analyze & Predict"),
        ]), n_clicks=0, id="analyze_link", className="nav_links")

    ]),

    html.Br(),

    html.Div(html.A([
        html.Span("Tab menu  "),
        html.I(className="fas fa-angle-double-right"),
    ]), n_clicks=0, id="open_drawer", className="nav_item")
]


@app.callback(Output("drawer", "open"),
              [Input("open_drawer", "n_clicks"),
               Input("minimize", "n_clicks")],
              [State("drawer", "open")])
def open_helper_menu(n_clicks, n_clicks2, is_open):
    return not is_open


MainMenu = [

    # Placeholder for level-2 tabs
    html.Div(id="selected_subpage"),

    # Due to a known Dash bug, the table
    # must be present in the first layout
    html.Div(id="table_container", children=[
        dash_table.DataTable(id='table',),
    ]),
]


SideBar2 = [
    html.H3("Tab menu"),
    html.Div(html.A([
        html.Span("Close menu  "),
        html.I(className="fas fa-angle-double-left"),
    ]), id="minimize", n_clicks=0),

    html.Br(),

    # Placeholder for low-level submenus, if needed
    html.Div(children=[], id="low_level_tabs_submenu"),
]


@app.callback(Output("theme_javascript", "run"),
              [Input("dark_theme", "n_clicks")])
def toggle_colors(n_clicks):
    """
    Embeds a javascript function in a dash component to allow changing the theme.

    Args:
        n_clicks (int): Number of times the theme button was clicked.

    Returns:
        str: Ties the JS script to the button.
    """

    if n_clicks % 2:
        change_color = "document.getElementsByTagName('body')[0].style.backgroundColor = 'black'"
    else:
        change_color = "document.getElementsByTagName('body')[0].style.backgroundColor = 'white'"

    # https://stackoverflow.com/a/16239245/6655150
    return """
        function change_theme () { 
        // the css we are going to inject
        var css = 'html {-webkit-filter: invert(100%);' +
            '-moz-filter: invert(100%);' + 
            '-o-filter: invert(100%);' + 
            '-ms-filter: invert(100%); }',

        head = document.getElementsByTagName('head')[0],
        style = document.createElement('style');

        // a hack, so you can "invert back" clicking the bookmarklet again
        if (!window.counter) { window.counter = 1;} else  { window.counter ++;
        if (window.counter % 2 == 0) { var css ='html {-webkit-filter: invert(0%); -moz-filter:    invert(0%); -o-filter: invert(0%); -ms-filter: invert(0%); }'}
         };

        style.type = 'text/css';
        if (style.styleSheet){
        style.styleSheet.cssText = css;
        } else {
        style.appendChild(document.createTextNode(css));
        }

        //injecting the css to the head
        head.appendChild(style);
        }

        let theme_button = document.getElementById("dark_theme");
        theme_button.onclick = change_theme;
        
    """ + change_color


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

    if n_clicks % 2 == 0:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


def serve_layout():
    """
    The layout of our app needs to be inside a function \
    so that every time some new session starts a new \
    session_id is generated.
    """

    session_id = f"python_generated_ssid_{uuid.uuid4()}"

    # TODO: This should probably be moved to `utils.startup`
    # load some data for all users
    for file in os.listdir("../data"):
        if file.endswith("csv"):
            df = pd.read_csv("../data/" + file)
            r.set(f"{session_id}_user_data_example_{file[:-4]}",
                  pickle.dumps(df))

    return html.Div(children=[

        html.H2(session_id, id="user_id", style={"display": "none"}),


        html.Div([
            # Sidebar / menu
            html.Div(children=SideBar, className="col-sm-4 col-md-3 col-xl-2",
                     id="sidebar",
                     style={"display": "inline-block"}),

            # main Div
            html.Div(children=MainMenu, className="col-sm-8  col-md-9 col-xl-10",
                     id="mainmenu",
                     style={"display": "inline-block"}),

            # Sidebar / menu
            html.Div(children=[
                sd_material_ui.Drawer(SideBar2, id="drawer", open=True,
                                      docked=True, openSecondary=True),
            ], className="",
                id="sidebar2",
                style={"display": "inline-block"}),

        ], className="row", id="main_content")


    ], className="container", style={"display": "inline"}, id="main_page")
