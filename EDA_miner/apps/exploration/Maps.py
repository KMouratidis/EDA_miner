"""
TBW...
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

import dash_cytoscape as cyto

from server import app
from utils import r, create_dropdown
from apps.data.View import get_data

import plotly.graph_objs as go
import pycountry


Sidebar = []


def Map_Options(options):
    """
    Generate the layout of the dashboard.

    Args:
        options (list(dict)): Available datasets as options for `dcc.Dropdown`.

    Returns:
        A Dash element or list of elements.
    """

    return html.Div(children=[

        html.Div([
            # Choose a dataset
            html.Div(create_dropdown("Available datasets", options,
                                     multi=False, id="dataset_choice_maps"),
                     className="vertical_dropdowns"),

            # Available buttons and choices for plotting
            html.Div(create_dropdown("Latitude", options=[],
                                     multi=False, id="lat_var"),
                     className="vertical_dropdowns"),
            html.Div(create_dropdown("Longitude", options=[],
                                     multi=False,
                                     id="lon_var"),
                     className="vertical_dropdowns"),
            html.Div(create_dropdown("Country", options=[],
                                     multi=False,
                                     id="country"),
                     className="vertical_dropdowns"),
        ], className="col-sm-3"),

        # The graph itself
        html.Div([
            dcc.Graph(id="map_graph", style={"minHeight": "650px"})
        ], className="col-sm-9"),
    ], className="row")




@app.callback([Output("lat_var", "options"),
               Output("lon_var", "options"),
               Output("country", "options")],
              [Input("dataset_choice_maps", "value")],
              [State("user_id", "children")])
def render_variable_choices_maps(dataset_choice, user_id):
    """
        Create a menu of dcc components for the user to choose \
        plotting options.

    Args:
        dataset_choice (str): Name of dataset.
        user_id (str): Session/user id.

    Returns:
        list(list(dict)): Key-value pairs to be input as \
                          `dcc.Dropdown` options.
    """


    df = get_data(dataset_choice, user_id)

    # Make sure all variables have a value before returning choices
    if any(x is None for x in [df, dataset_choice]):
        raise PreventUpdate()

    options = [{'label': col[:35], 'value': col} for col in df.columns]

    return [options, options, options]


# TODO: This probably needs to interface with the schema
def country2code(value):
    """
    Country(alpha_2='DE', alpha_3='DEU', name='Germany', numeric='276',
            official_name='Federal Republic of Germany')
    """
    for key in ["alpha_2", "alpha_3", "name", "numeric", "official_name"]:
        matched_country = pycountry.countries.get(**{key: value})

        if matched_country is not None:
            # Usually the 3-letter code
            return matched_country.alpha_3



@app.callback(Output("map_graph", "figure"),
              [Input("lat_var", "value"),
               Input("lon_var", "value"),
               Input("country", "value")],
              [State("user_id", "children"),
               State("dataset_choice_maps", "value")])
def plot_map(lat_var, lon_var, country, user_id, dataset_choice_maps):
    """
    Plot the map according to user choices.

    Args:
        in_node (str): Column name containing the values of \
                      nodes from where links start.
        out_node (str): Column name for nodes where links end.
        layout_choice (str): One of the layouts available in \
                             Cytoscape.
        user_id (str): Session/user id.
        dataset_choice_maps (str): Name of dataset.

    Returns:
        [list(dict), dict]: A list of elements (dicts for Cytoscape) \
                            and the layout for the graph.
    """


    if any(x is None for x in [lat_var, lon_var, country,
                               dataset_choice_maps]):
        raise PreventUpdate()

    df = get_data(dataset_choice_maps, user_id)

    df["codes"] = df[country].apply(lambda x: country2code(x))
    countries = df["codes"].dropna().unique()

    return {
        "data": [
            go.Scattergeo(
                locationmode='country names',
                lat=df[lat_var],
                lon=df[lon_var],
            ),
            go.Choropleth(
                locations=countries,
                # we need to mask the counts
                z=df.groupby("codes").count().loc[countries, lat_var].dropna().values
            )
        ],
        "layout": {
            'automargin': True,
            'margin': {
                        'l': 10, 'r': 10, 'b': 0, 't': 40
                    },
            "projection": {
                "type": 'orthographic'
            },
        }
    }
