"""
This module takes care of the menu and choices provided when the \
"Explore & Visualize" high-level tab is selected.

Dash callbacks:
    - tab_subpages: Given the low-level tab choice, render the \
                    appropriate view.
    - render_sidemenu: Render the menu in the side-navbar.

Notes to others:
    You should probably not write code here, unless you are defining \
    a new level-2 tab. Here you can find all visuals-generating \
    functionality. Implementations go to their own modules down the \
    package hierarchy, in `apps.exploration`
"""

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from .server import app, redis_conn
from .chart_maker import Exploration_Options
from .networks import Network_Options
from .maps import Map_Options
from .kpis import KPI_Options
from .text_viz import TextViz_Options
from .dashboard_maker import Dashboard_Options
from utils import interactive_menu, get_dataset_options

from flask_login import login_required


app.layout = html.Div(children=[

    *interactive_menu(output_elem_id="sidenav2_contents"),

    html.Div(children=[
        dcc.Tabs(id="level2_tabs", value='chart_maker', children=[
            dcc.Tab(label='Chart Maker', value='chart_maker',
                    id="exploration"),
            dcc.Tab(label='Key performance indicators', value='kpi',
                    id="kpi"),
            dcc.Tab(label='Maps & Geoplotting', value='maps',
                    id="maps"),
            dcc.Tab(label='Network graphs', value='networks',
                    id="networks"),
            dcc.Tab(label='Text visualizations', value='textviz',
                    id="textviz"),
            dcc.Tab(label='Dashboard Maker', value='dashboard',
                    id="dashboard"),
        ]),

        # Placeholder div for actual contents
        html.Div(id="visuals-content"),
    ]),
])


# TODO: Any sidemenus, if any, should be added here.
# TODO: This probably needs to become one with the next callback.
@app.callback(Output("sidenav2_contents", "children"),
              [Input('level2_tabs', 'value')])
def render_sidemenu(tab):
    """
    Render the menu in the side-navbar.

    Args:
        tab (str): The tab the user is currently on.

    Returns:
        A Dash element or list of elements.
    """

    return html.H4(tab)


@app.callback(Output('visuals-content', 'children'),
              [Input('level2_tabs', 'value')])
@login_required
def tab_subpages(tab):
    """
    Given the low-level tab choice, render the appropriate view.

    Args:
        tab (str): The tab the user is currently on.

    Returns:
        A Dash element or list of elements.
    """

    options = get_dataset_options(redis_conn)

    # each view should handle on its own how changing
    # the dataset is handled
    if tab == 'chart_maker':
        return Exploration_Options(options)

    elif tab == 'kpi':
        return KPI_Options(options)

    elif tab == "maps":
        return Map_Options(options)

    elif tab == "networks":
        return Network_Options(options)

    elif tab == "textviz":
        return TextViz_Options()

    elif tab == "dashboard":
        return Dashboard_Options

    else:
        # In case someone messes with the underlying HTML/JS
        # and chooses a non-allowed tab
        return [html.H4("Invalid choice")]


if __name__ == "__main__":
    # Normally you would run from here. Now it doesn't work for a few
    # reasons: 1) The "login_required" above has not been initialized
    # at the app level but at the project level, so either remove it
    # or use login_manager = LoginManager(app.server), 2) Upon
    # defining the app (see .server) we passed "requests_pathname_prefix"
    # which cause Dash to look at the wrong place for the static files,
    # so remove that too, and 3) Imports are defined as relative imports
    # so you need to care care of that too.
    app.run_server()
