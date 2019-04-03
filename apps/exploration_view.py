"""
    This module takes care of the menu and choices provided when the
    "Explore & Visualize" level-1 tab is selected.

    You should probably not write code here, UNLESS you are defining
    a new level-2 tab.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import r

from apps.exploration import Exploration, KPIs

from apps.exploration import Exploration_Options, KPI_Options, PDF_report_options
from apps.exploration import Exploration3D_Options, Network_Options
from apps.data.View import get_available_choices

import plotly.graph_objs as go
import peakutils



layout = html.Div(children=[
    html.Div(children=[
        dcc.Tabs(id="viz_tabs", value='exploration', children=[
            dcc.Tab(label='Exploratory analysis', value='exploration',
                    id="exploration"),
            dcc.Tab(label='Key performance indicators', value='kpi',
                    id="kpi"),
            dcc.Tab(label='3D graphs', value='graphs3d',
                    id="graphs3d"),
            dcc.Tab(label='Network graphs', value='networks',
                    id="networks"),
            dcc.Tab(label='PDF report', value='pdf_report',
                    id="pdf_report"),
        ]),
    ]),
    html.Div(id="visuals-content"),
])


@app.callback(Output('visuals-content', 'children'),
              [Input('viz_tabs', 'value')],
              [State("user_id", "children")])
def tab_subpages(tab, user_id):

    options, results = get_available_choices(r, user_id)

    #
    if all(v is None for k,v in results.items()):
        return html.H4("No data currently uploaded")

    # each view should handle on its own how chaning
    # the dataset it handled
    if tab == 'exploration':
        return Exploration_Options(options, results)

    elif tab == 'kpi':
        return KPI_Options(options, results)

    elif tab == "graphs3d":
        return Exploration3D_Options(options, results)

    elif tab == "networks":
        return Network_Options(options, results)

    elif tab == "pdf_report":
        return PDF_report_options(options, results)
