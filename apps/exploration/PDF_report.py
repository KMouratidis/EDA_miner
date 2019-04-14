"""
    To be implemented.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
import layouts

import visdcc
import dill
import dash_daq as daq


def PDF_report_options(options, results):

    return html.Div([

        html.Button("Render & Finalise!", id="render_PDF"),

        html.Div([

            # header
            html.Div([
                dcc.Textarea(id="header_input"),
            ], className="row", id="header_text"),

            # first row
            html.Div([
                html.Div([
                    dcc.Textarea(id="row1_header_input"),
                ], className="col-sm-12 col_header", id="row1_header_text"),

                # first four columns of row
                html.Div([
                        dcc.Textarea(id="row1col1_input"),
                    ], className="col-sm-4", id="row1col1"),

                # second eight columns of row
                html.Div([
                    dcc.Graph(id="graph12",
                              figure={
                                    'data': [],
                                    'layout': layouts.PDF_Layout1.first_figure,
                                },
                              # hide upper plotly menu
                              config={'displayModeBar': False}),
                ], className="col-sm-8"),

            ], className="row"),

            # second row
            html.Div([
                html.H3("Row2 header", className="col-sm-12 col_header"),

                # first sub-row
                # first eight columns of row
                html.Div([
                    dcc.Graph(id="graph21",
                              figure={
                                    'data': [],
                                    'layout': layouts.PDF_Layout1.second_figure,
                                },
                              # hide upper plotly menu
                              config={'displayModeBar': False}),
                ], className="col-sm-8"),

                # last four columns of row, (1st subrow)
                html.Div([
                        html.P("Lorem ipsum dolor sit amet, consectetur "
                               " adipisicing elit, sed do eiusmod tempor "
                               "incididunt ut labore et dolore magna aliqua. "
                               " Ut enim ad minim veniam, quis nostrud "
                               "exercitation ullamco laboris nisi ut aliquip "
                               "ex ea commodo consequat. Duis aute irure "
                               "dolor in reprehenderit in voluptate velit "
                               "esse cillum dolore eu fugiat nulla "
                               "pariatur. Excepteur sint occaecat cupidatat "
                               "non proident, sunt in culpa qui officia "
                               "deserunt mollit anim id est laborum."),
                    ], className="col-sm-4"),

                # second sub-row
                html.Br(),
                # first eight columns of row, (1st subrow)
                html.Div([
                        html.P("Lorem ipsum dolor sit amet, consectetur "
                               "adipisicing elit, sed do eiusmod tempor "
                               "incididunt ut labore et dolore magna aliqua. "
                               "Ut enim ad minim veniam, quis nostrud "
                               "exercitation ullamco laboris nisi ut aliquip "
                               "ex ea commodo consequat. Duis aute irure "
                               "dolor in reprehenderit in voluptate velit esse "
                               " cillum dolore eu fugiat nulla "
                               "pariatur. Excepteur sint occaecat cupidatat "
                               "non proident, sunt in culpa qui officia "
                               "deserunt mollit anim id est laborum."),
                    ], className="col-sm-8"),

                # last four columns of row
                html.Div([
                    daq.Knob(
                      id='my-daq-knob',
                      max=10,
                      min=0
                    )
                ], className="col-sm-4"),

            ], className="row"),

            # footer
            html.Div([
                html.H4("Nothing in the footer",
                        className="col-sm-12 col_header")
            ], className="row", style={"backgroundColor": "red"}),
        ], className="container", id="printablePDF")
    ])


@app.callback([Output("graph12", "figure"),
               Output("graph21", "figure"),
               Output("row1col1", "children"),
               Output("header_text", "children"),
               Output("row1_header_text", "children")],
              [Input("render_PDF", "n_clicks")],
              [State("saved_graph_configs1", "figure"),
               State("saved_graph_configs2", "figure"),
               State("row1col1_input", "value"),
               State("header_input", "value"),
               State("row1_header_input", "value")])
def render_pdf_func(n_clicks, exported_figure1, exported_figure2,
                    row1col1_text, header_input, row1_header_input):

    if n_clicks is not None and n_clicks >= 1:

        new_figs = []
        for exported_fig in [exported_figure1, exported_figure2]:
            new_fig = exported_fig.copy()

            x_axis = exported_fig["layout"]["xaxis"]
            y_axis = exported_fig["layout"]["yaxis"]

            new_fig["layout"] = layouts.PDF_Layout1.render(x_axis, y_axis)

            new_figs.append(new_fig)

        return [
            new_figs[0],
            new_figs[1],
            [dcc.Markdown(row1col1_text)],
            [html.H1(header_input)],
            [html.H3(row1_header_input)]
        ]

    else:
        # when dash layout is initially loaded
        return [
            exported_figure1,
            exported_figure2,
            [dcc.Textarea(id="row1col1_input")],
            [dcc.Textarea(id="header_input")],
            [dcc.Textarea(id="row1_header_text")]
        ]


