"""
The main app is here. It takes the base menus from menus.py \
and puts them in the app.layout, then defines callbacks \
and finally has the if-name-main block necessary to run the app.

Dash callbacks:
    - high_level_tabs: On high-level tab selection, render \
                       the appropriate layout.
    - update_sidebar_menus: For the second level of tabs, show \
                            different sidebar menu.

Notes to others:
    You should probably not write code here, unless:
        - working on side-menus,
        - working on login system,
        - adding a new-high-level tab, or other new feature.
"""


from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

from server import app
from utils import cleanup, r
from menus import serve_layout
from apps import data_view, exploration_view, analyze_view
from apps.exploration import Exploration, KPIs, Exploration3D
from apps.analyze import Model_Builder


app.layout = html.Div([

    # for exporting figures aimed at PDF report generation
    dcc.Graph(id="saved_graph_configs1", style={"display": "none"}),
    dcc.Graph(id="saved_graph_configs2", style={"display": "none"}),

    serve_layout(),
])




# Input and Output defined in MainMenu
@app.callback(Output('selected_subpage', 'children'),
              [Input('high_level_tabs', 'value')])
def high_level_tabs(tab):
    """
    On high-level tab selection, render the appropriate layout.
    """

    if tab == 'EDA':
        return exploration_view.layout
    elif tab == "modelling":
        return analyze_view.layout
    elif tab == "data":
        return data_view.layout
    else:
        return '404'


@app.callback(Output('low_level_tabs_submenu', 'children'),
              [Input('level2_tabs', 'value')])
def update_sidebar_menus(level2_tabs):
    """
    For the second level of tabs, show different sidebar menu.
    """

    if level2_tabs is not None:
        if level2_tabs == 'kpi':
            return Exploration.Graphs_Export + KPIs.Sidebar

        elif level2_tabs == "exploration":
            return Exploration.Graphs_Export + Exploration.Sidebar

        elif level2_tabs == "graphs3d":
            return Exploration.Graphs_Export + Exploration3D.Sidebar

        elif level2_tabs == 'model_builder':
            return Model_Builder.SideBar_modelBuilder

        elif level2_tabs == 'pipelines':
            return [html.H4(f"Tab is {level2_tabs}")]

        else:
            return [html.H4(f"Tab is {level2_tabs}")]

    else:
        return []


if __name__ == "__main__":
    # TODO: Implement user_id correctly:
    #       create a Redis entry with all `user_id`s that
    #       joined the session and cleanup for each of them

    # TODO: Consider making this an executable
    #       https://community.plot.ly/t/convert-dash-to-executable-file-exe/14222

    try:
        app.run_server(debug=True, host='0.0.0.0')

    finally:
        cleanup(r)

else:
    # Probably a deployment (we need it here because of Dash)
    # not having a layout defined in server.py
    server = app.server