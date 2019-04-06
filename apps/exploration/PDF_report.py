"""
    To be implemented.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
from utils import r, create_dropdown

import plotly.graph_objs as go
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

                # first six columns of row
                html.Div([
                        dcc.Textarea(id="row1col1_input"),
                    ], className="col-sm-4", id="row1col1"),

                # second six columns of row
                html.Div([
                    dcc.Graph(id="graph12",

                              figure={
                                    'data': [],
                                    'layout': go.Layout(
                                        autosize = False,
                                        bargap = 0.35,
                                        font = {
                                          "family": "Raleway",
                                          "size": 10
                                        },
                                        height = 300,
                                        hovermode = "closest",
                                        legend = {
                                          "x": -0.0228945952895,
                                          "y": -0.189563896463,
                                          "orientation": "h",
                                          "yanchor": "top"
                                        },
                                        margin = {
                                          "r": 0,
                                          "t": 20,
                                          "b": 10,
                                          "l": 10
                                        },
                                        showlegend = True,
                                        title = "",
                                        width = 600,
                                        xaxis = {
                                          "autorange": True,
                                          "range": [-0.5, 4.5],
                                          "showline": True,
                                          "title": "",
                                          "type": "category"
                                        },
                                        yaxis = {
                                          "autorange": True,
                                          "range": [0, 22.9789473684],
                                          "showgrid": True,
                                          "showline": True,
                                          "title": "",
                                          "type": "linear",
                                          "zeroline": False
                                        }
                                    )
                                    },

                              # hide upper plotly menu
                              config={'displayModeBar': False}),
                ], className="col-sm-8"),

            ], className="row"),


            # second row
            html.Div([
                html.H3("Row2 header", className="col-sm-12 col_header"),

                html.Div([
                    dcc.Graph(id="graph21",

                              figure={
                                    'data': [],
                                    'layout': go.Layout(
                                        autosize = False,
                                        bargap = 0.35,
                                        font = {
                                          "family": "Raleway",
                                          "size": 10
                                        },
                                        height = 300,
                                        hovermode = "closest",
                                        legend = {
                                          "x": -0.0228945952895,
                                          "y": -0.189563896463,
                                          "orientation": "h",
                                          "yanchor": "top"
                                        },
                                        margin = {
                                          "r": 0,
                                          "t": 20,
                                          "b": 10,
                                          "l": 10
                                        },
                                        showlegend = True,
                                        title = "",
                                        width = 600,
                                        xaxis = {
                                          "autorange": True,
                                          "range": [-0.5, 4.5],
                                          "showline": True,
                                          "title": "",
                                          "type": "category"
                                        },
                                        yaxis = {
                                          "autorange": True,
                                          "range": [0, 22.9789473684],
                                          "showgrid": True,
                                          "showline": True,
                                          "title": "",
                                          "type": "linear",
                                          "zeroline": False
                                        }
                                    )
                                    },

                              # hide upper plotly menu
                              config={'displayModeBar': False}),
                ], className="col-sm-8"),

                html.Div([
                        html.P("Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                    ], className="col-sm-4"),

                html.Br(),

                html.Div([
                        html.P("Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                    ], className="col-sm-8"),

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
            ], className="row", style={"backgroundColor":"red"}),

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

    if n_clicks is not None and n_clicks>= 1:

        new_figs = []
        for exported_fig in [exported_figure1, exported_figure2]:
            new_fig = exported_fig.copy()

            x_axis = exported_fig["layout"]["xaxis"]
            y_axis = exported_fig["layout"]["yaxis"]

            new_fig["layout"] = go.Layout(
                autosize = False,
                bargap = 0.35,
                font = {
                  "family": "Raleway",
                  "size": 10
                },
                height = 300,
                hovermode = "closest",
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                showlegend = True,
                title = "",
                width = 600,
                xaxis = x_axis,
                yaxis = y_axis
            )

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

