"""
This module takes care of the menu and choices provided when the
"Explore & Visualize" high-level tab is selected.

Dash callbacks:
    - tab_subpages: Given the low-level tab choice, render the \
                    appropriate view.

Notes to others:
    You should probably not write code here, unless you are defining
    a new level-2 tab. Here you can find all visuals-generating
    functionality. Implementations go to their own modules down the
    package hierarchy, in `apps.exploration`
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import r
from apps.exploration import TextViz_Options, PDF_report_options
from apps.exploration import Exploration_Options, KPI_Options
from apps.exploration import Exploration3D_Options, Network_Options
from apps.data.View import get_available_choices


layout = html.Div(children=[
    html.Div(children=[
        dcc.Tabs(id="level2_tabs", value='exploration', children=[
            dcc.Tab(label='Exploratory analysis', value='exploration',
                    id="exploration"),
            dcc.Tab(label='Key performance indicators', value='kpi',
                    id="kpi"),
            dcc.Tab(label='3D graphs', value='graphs3d',
                    id="graphs3d"),
            dcc.Tab(label='Network graphs', value='networks',
                    id="networks"),
            dcc.Tab(label='Text visualizations', value='textviz',
                    id="textviz"),
            dcc.Tab(label='PDF report', value='pdf_report',
                    id="pdf_report"),
        ]),
    ]),

    # Placeholder div for actual contents
    html.Div(id="visuals-content"),
])


@app.callback(Output('visuals-content', 'children'),
              [Input('level2_tabs', 'value')],
              [State("user_id", "children")])
def tab_subpages(tab, user_id):
    """
    Given the low-level tab choice, render the appropriate view.

    Args:
        tab (str): the low-level tab.
        user_id (str): the user/session uid.

    Returns:
        A list of HTML-dash components, usually within a div.
    """

    # TODO: This check for data existence might be slow.
    #       It would be good to test/review and improve it.
    options, results = get_available_choices(r, user_id)
    if all(v is None for k,v in results.items()):
        return [html.H4("No data currently uploaded")]

    # each view should handle on its own how changing
    # the dataset is handled
    if tab == 'exploration':
        return Exploration_Options(options, results)

    elif tab == 'kpi':
        return KPI_Options(options, results)

    elif tab == "graphs3d":
        return Exploration3D_Options(options, results)

    elif tab == "networks":
        return Network_Options(options, results)

    elif tab == "textviz":
        return TextViz_Options(options, results)

    elif tab == "pdf_report":
        return PDF_report_options(options, results)

    else:
        # In case someone messes with the underlying HTML/JS
        # and chooses a non-allowed tab
        return [html.H4("Invalid choice")]
