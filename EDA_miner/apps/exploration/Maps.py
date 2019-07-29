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
                {"label": "Simple geoscatter", "value": "geoscatter"}
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

        ], className="col-sm-3"),

        # The graph itself
        html.Div([
            dcc.Graph(id="map_graph", style={"minHeight": "650px"})
        ], className="col-sm-9"),
    ], className="row")


@app.callback([Output("lat_var", "options"),
               Output("lon_var", "options"),
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

    return [options, options, options, options]


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
               Output("z_var", "disabled")],
              [Input("map_type_choice", "value")])
def show_hide_aggregator_dropdown(map_type):
    if map_type == "agg_choropleth":
        return False, False
    else:
        return True, True


@app.callback(Output("map_graph", "figure"),
              [Input("lat_var", "value"),
               Input("lon_var", "value"),
               Input("country", "value"),
               Input("z_var", "value"),
               Input("map_type_choice", "value"),
               Input("aggregator_field", "value"),
               Input("colorscale", "value")],
              [State("user_id", "children"),
               State("dataset_choice_maps", "value")])
def plot_map(lat_var, lon_var, country, z_var, map_type, aggregator_type,
             colorscale, user_id, dataset_choice_maps):
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


    if any(x is None for x in [lat_var, lon_var, country, map_type,
                               dataset_choice_maps]):
        raise PreventUpdate()

    if colorscale is None:
        colorscale = "Jet"

    df = get_data(dataset_choice_maps, user_id)

    # Attempt conversion of the country column to country codes
    df["codes"] = df[country].apply(lambda x: country2code(x))
    countries = df["codes"].dropna().unique()

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
            "projection": {
                "type": 'orthographic'
            },
        }
    }
