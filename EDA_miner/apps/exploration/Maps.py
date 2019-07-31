"""
TBW...

TODO:
    Implement https://plot.ly/python/choropleth-maps/#choropleth-inset-map
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


colorscale_list = "Greys, YlGnBu, Greens, YlOrRd, Bluered, RdBu, Reds, " \
                  "Blues, Picnic, Rainbow, Portland, Jet, Hot, Blackbody, " \
                  "Earth, Electric, Viridis, Cividis".split(", ")


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
            # Choose a map type
            html.Div(create_dropdown("Map type", [
                {"label": "Choropleth", "value": "agg_choropleth"},
                {"label": "Simple geoscatter", "value": "geoscatter"},
                {"label": "Lines on map", "value": "maplines"},
            ], multi=False, id="map_type_choice"),
                     className="vertical_dropdowns"),

            # Available buttons and choices for plotting
            html.Div(create_dropdown("Colorscale", options=[
                {"label": v, "value": v}
                for v in colorscale_list
            ], multi=False, id="colorscale", value="Jet"),
                     className="vertical_dropdowns"),
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
            html.Div(create_dropdown("Z variable", options=[],
                                     multi=False, id="z_var"),
                     className="vertical_dropdowns"),
            html.Div(create_dropdown("Choose aggregation type", options=[
                {"label": "Sum", "value": "sum"},
                {"label": "Average", "value": "mean"},
                {"label": "Count", "value": "count"},
                {"label": "Max", "value": "max"},
                {"label": "Min", "value": "min"},
            ], multi=False, id="aggregator_field", value="count"),
                     className="vertical_dropdowns"),
            html.Div(create_dropdown("Destination latitude", options=[],
                                     multi=False, id="dest_lat"),
                     className="vertical_dropdowns"),
            html.Div(create_dropdown("Destination longitude", options=[],
                                     multi=False, id="dest_long"),
                     className="vertical_dropdowns"),
            html.Div(create_dropdown("Map projection style", options=[
                {"label": "Equirectangular", "value": "equirectangular"},
                {"label": "Azimuthal equal area", "value": "azimuthal equal area"},
                {"label": "Orthographic", "value": "orthographic"},

            ],
                                     multi=False, id="projection_type"),
                     className="vertical_dropdowns"),

        ], className="col-sm-3"),

        # The graph itself
        html.Div([
            dcc.Graph(id="map_graph", style={"minHeight": "650px"})
        ], className="col-sm-9"),
    ], className="row")


@app.callback([Output("lat_var", "options"),
               Output("lon_var", "options"),
               Output("dest_lat", "options"),
               Output("dest_long", "options"),
               Output("country", "options"),
               Output("z_var", "options")],
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

    return [options] * 6


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


@app.callback([Output("aggregator_field", "disabled"),
               Output("z_var", "disabled"),
               Output("dest_lat", "disabled"),
               Output("dest_long", "disabled")],
              [Input("map_type_choice", "value")])
def show_hide_aggregator_dropdown(map_type):
    if map_type == "agg_choropleth":
        return False, False, True, True
    elif map_type == "maplines":
        return True, True, False, False
    else:
        return True, True, True, True


@app.callback(Output("map_graph", "figure"),
              [Input("lat_var", "value"),
               Input("lon_var", "value"),
               Input("country", "value"),
               Input("z_var", "value"),
               Input("map_type_choice", "value"),
               Input("aggregator_field", "value"),
               Input("dest_lat", "value"),
               Input("dest_long", "value"),
               Input("colorscale", "value"),
               Input("projection_type", "value")],
              [State("user_id", "children"),
               State("dataset_choice_maps", "value")])
def plot_map(lat_var, lon_var, country, z_var, map_type, aggregator_type,
             dest_lat, dest_long, colorscale, projection_type, user_id,
             dataset_choice_maps):
    """
    Plot the map according to user choices.

    Args:
        lat_var (str): Column name for latitude.
        lon_var (str): Column name for latitude.
        country (str): Column name for the country. Accepted values \
                       include 3-letter country codes and full names \
                       or anything else pycountry can decode.
        z_var (str): Column name for choropleth colors.
        map_type (str): Type of math, one of three choices: Simple or \
                        Aggregated Choropleth, or Lines on map.
        aggregator_type (str): Type of aggregation to perform on the \
                               data (e.g. mean, max).
        dest_lat (str): Column name for destination latitude, if drawing \
                        lines on map chart.
        dest_long (str): Column name for destination longitude, if drawing \
                        lines on map chart.
        colorscale (str): Colorscale for the choropleth, one of several \
                          as defined in plotly.
        projection_type (str): Projection type, one of several as \
                               defined by plotly.
        user_id (str): Session/user id.
        dataset_choice_maps (str): Name of dataset.

    Returns:
        dict: The figure to draw.
    """


    if any(x is None for x in [lat_var, lon_var, country, map_type,
                               dataset_choice_maps, projection_type]):
        raise PreventUpdate()

    if colorscale is None:
        colorscale = "Jet"

    df = get_data(dataset_choice_maps, user_id)

    # Attempt conversion of the country column to country codes
    df["codes"] = df[country].apply(lambda x: country2code(x))
    countries = df["codes"].dropna().unique()

    if map_type == "maplines":

        if dest_long is None or dest_long is None:
            raise PreventUpdate()

        # make visualizations lighter
        df = df[:len(df)//2]

        traces = [go.Scattergeo(
            locationmode='country names',
            lat=[df[lat_var][i], df[dest_lat][i]],
            lon=[df[lon_var][i], df[dest_long][i]],
            mode='lines',
        ) for i in range(len(df))]
    else:
        traces = [go.Scattergeo(
            locationmode='country names',
            lat=df[lat_var],
            lon=df[lon_var],
        )]

    if "choropleth" in map_type:
        if z_var is None:
            raise PreventUpdate()

        if aggregator_type is None:
            aggregator_type = "count"

        try:
            # .loc is needed to correctly order the countries
            z = df.groupby("codes").agg(aggregator_type).loc[countries,
                                                    z_var].dropna().values
        except KeyError as e:
            print("Error! Probably bad z_var; usually due to incorrect "
                  "aggregate operation. Error: ", e)

            raise PreventUpdate()

        traces.append(go.Choropleth(locations=countries, z=z,
                                    colorscale=colorscale))


    return {
        "data": traces,
        "layout": {
            'automargin': True,
            'margin': {
                        'l': 10, 'r': 10, 'b': 0, 't': 40
                    },
            "geo": {
                "projection": {
                    "type": projection_type
                }
            },
        }
    }
