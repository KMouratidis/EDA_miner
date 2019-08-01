"""
This module will be used to graphically create models. \
RapidMiner, Weka, Orange, etc, ain't got sh!t on us :)

You should probably not write code here, UNLESS you know \
what you're doing.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

from server import app
from utils import r, create_dropdown, get_data
from styles import cyto_stylesheet
from apps.data.View import get_available_choices
from apps.analyze.models import pipeline_creator, pipeline_classes
from apps.analyze.models.graph_structures import Graph, GraphUtils, orders
from apps.analyze.models.graph_structures import node_options, ml_options
from apps.analyze.models.graph_structures import prebuilt_pipelines

import dill


# This is inserted in various parts to make sure all
# callbacks work correctly
debugger_layout = [
    dcc.Textarea(id="text_input", style={"display": "none"}),
    dcc.Store(id="mapping_store"),
    dcc.RadioItems(options=[], id="modify_node_params",
                   style={"display": "none"}),
]

# TODO: Add divider for categories with huge lists
items = [
    [dbc.DropdownMenuItem(model["label"], id=f"add_{model['node_type']}",
                          n_clicks_timestamp=0)
     for model in ml_options
     if model["parent"] == category]
    for category in orders
]

# Layout definition for the initial setup
default_steps = prebuilt_pipelines["default"]

initial_graph = GraphUtils(default_steps).render_graph()


Model_Builder_Layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-graph',
        layout={'name': "preset"},
        style={"width": "98%", "height": "600px"},
        elements=initial_graph,
        stylesheet=cyto_stylesheet,
    ),

    # PIPELINES INFO
    dbc.Modal([
        dbc.ModalHeader("Pipelines exported:"),
        dbc.ModalBody("No pipeline exported.", id="model_specs"),
        dbc.ModalFooter(
            dbc.Button("Close", id="close", className="ml-auto")
        ),
    ], id="modal"),

    # NODE OPTIONS
    dbc.Modal([
        dbc.ModalHeader("Node options"),
        dbc.ModalBody(children=[

            # Stuff inside the modal
            html.Div(id='sidebar_collapsible_button_modify_node', children=[
                html.Div(id="inspector", children=[
                    html.Div([
                        *create_dropdown("Options", [
                            {"label": "No node selected", "value": "none"}
                        ], id="modify_option_dropdown"),
                        dcc.RadioItems(options=[
                            {"label": "No node selected", "value": "none"}
                        ], id="modify_node_params",
                           labelStyle={
                               'display': 'inline-block',
                               'margin': '5px'
                           }
                        )
                    ])
                ]),

                *debugger_layout,

                html.Button("Update node", id="modify_node", n_clicks=0,
                            n_clicks_timestamp=0),
            ]),
        ], id="node_specs"),
        dbc.ModalFooter(
            dbc.Button("Close", id="close_node_options",
                       className="ml-auto")
        ),
    ], id="modal_node_options"),
])


SideBar_modelBuilder = [

    # Convert model
    html.Div([
        html.Button("Convert to model",
                    id="convert"),
    ], id="export_pipe_submenu"),

    # Load predefined pipeline
    html.Div([
        html.Button("Load prebuilt pipeline", id="load_prebuilt",
                    n_clicks_timestamp=0, ),
        dcc.Dropdown(options=[{"value": k, "label": k}
                              for (k, v) in prebuilt_pipelines.items()],
                     id="pipeline_options", value="default"),
    ], id="load_pipeline_submenu"),

    # Remove nodes
    html.Div([
        html.Button("Remove a node", id="remove_node",
                    n_clicks_timestamp=0, ),
        dcc.Dropdown(options=[{"value": elem["data"]["id"],
                               "label": elem["data"]["label"]}
                              for elem in initial_graph[:-4]
                              if "parent" in elem["data"]],
                     id="delete_options"),
    ], id="remove_node_submenu"),

    # Connect selected nodes
    html.Div([
        html.Button("Connect selected nodes",
                    n_clicks_timestamp=0,
                    id="connect_selected_nodes"),
    ], id="connect_nodes_submenu"),


    # Add nodes (collapsible)
    html.Div([
        html.Button([
            html.Span('Add node'),
        ], id='button_collapse_add_node', n_clicks=0),
        # Stuff inside the collapsible
        html.Div(id='sidebar_collapsible_button_add_node', children=[
            dbc.DropdownMenu(
                label=f"Category: {category}", children=item,
                className="mb-3"
            ) for (category, item) in zip(orders, items)
        ]),
    ], id="add_nodes_submenu"),


    # Modify nodes (modal)
    html.Div([
        html.Button([
            html.Span('Node options'),
        ], id='button_collapse_modify_node', n_clicks=0),
    ]),
]


# Callback for SYMPY 1
@app.callback(Output("data_holder", "children"),
              [Input("modify_option_dropdown", "value")],
              [State("modify_option_dropdown", "options")])
def button_adder(selected, options):

    if selected is None:
        return [
            html.Br(),
            html.Br(),

            *debugger_layout,
        ]

    # Looping over all the options enforces (hopefully the correct) order
    selected_columns = {col["value"]: col["value"] for col in options
                        if col["value"] in selected}
    all_columns = {col["value"]: col for col in options}

    return [
        html.Br(),
        html.Br(),

        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in ['Column name',
                                               'Assigned symbol']])] +
            # Body
            [html.Tr([
                html.Td(col),
                html.Td(col),
            ]) for col in selected]
        ),

        dcc.Textarea(id="text_input"),

        dcc.Store(id="mapping_store", data={"selected_columns": selected_columns,
                                            "all_columns": all_columns})
    ]


# When the sidebar button is clicked, collapse the div
@app.callback(Output('sidebar_collapsible_button_add_node', 'style'),
              [Input('button_collapse_add_node', 'n_clicks')],)
def button_toggle(n_clicks):
    if n_clicks is not None and n_clicks % 2 == 1:
        # Start with the menu open
        return {'display': 'none'}
    else:
        return {'display': 'block'}


@app.callback(Output("modal_node_options", "is_open"),
              [Input("modify_node", "n_clicks"),
               Input("close_node_options", "n_clicks"),
               Input("button_collapse_modify_node", "n_clicks")],
              [State("modal_node_options", "is_open")])
def toggle_modal(n1, n2, n3, is_open):
    if n1 or n2 or n3:
        return not is_open
    return is_open


@app.callback(Output("cytoscape-graph", "elements"),
              [Input("remove_node", "n_clicks_timestamp"),
               Input("connect_selected_nodes", "n_clicks_timestamp"),
               Input("modify_node", "n_clicks_timestamp"),
               Input("load_prebuilt", "n_clicks_timestamp")]+[
                  Input(f"add_{node_options[model]['node_type']}",
                        "n_clicks_timestamp")
                  for model in node_options
              ],
              [State("cytoscape-graph", "elements"),
               State("delete_options", "value"),
               State("cytoscape-graph", "selectedNodeData"),
               State("modify_option_dropdown", "value"),
               State("modify_node_params", "value"),
               State("cytoscape-graph", "tapNodeData"),
               State("text_input", "value"),
               State("mapping_store", "data"),
               State("pipeline_options", "value"),
               State("user_id", "children")])
def modify_graph(remove_clicked_time, connect_selected_time,
                 modify_node_time, load_prebuilt_time, *add_nodes):

    # This is necessary since Python cannot accept *args in the middle
    # of the function parameter list. The tapped node is used only for
    # altering parameters on the last-clicked node, while the selected
    # is used for connecting nodes. The modify_node_attribute refers to
    # the dropdown (sklearn kwarg) and modify_node_params is the value
    (elems, to_be_deleted, selected,
     modify_node_attribute, modify_node_params,
     tapped, user_text, mapping_store,
     pipeline_options, user_id) = add_nodes[-10:]


    add_nodes = add_nodes[:-10]

    if all(x is None for x in [remove_clicked_time, connect_selected_time,
                               modify_node_time, *add_nodes]):
        if elems is not None:
            return elems
        else:
            return []

    G = Graph(elems)

    # Create list of tuples, e.g.: (time_clicked, add_xgb)
    add_node_list = [(add_node, f"add_{model}")
                     for (add_node, model) in zip(add_nodes, node_options)]

    # Sort buttons based on clicked time (most recent first)
    buttons_and_clicks = sorted([
        (remove_clicked_time, "remove"),
        (connect_selected_time, "connect"),
        (modify_node_time, "modify"),
        (load_prebuilt_time, "prebuilt")
    ] + add_node_list, reverse=True)

    # Graph operations
    if buttons_and_clicks[0][1] == "remove":
        G.node_collection.remove_node(to_be_deleted)

    elif buttons_and_clicks[0][1] == "connect":
        G.edge_collection.add_edges(selected)

    elif buttons_and_clicks[0][1].startswith("add_"):
        # e.g.: (time_clicked, add_xgb) --> xgb
        G.node_collection.add_node(buttons_and_clicks[0][1][4:])

    elif buttons_and_clicks[0][1] == "prebuilt":
        pipeline_steps = prebuilt_pipelines[pipeline_options]

        return GraphUtils(pipeline_steps).render_graph()

    elif buttons_and_clicks[0][1] == "modify":
        if tapped is not None:
            for node in G.node_collection.nodes:
                # iterate over all the nodes to find the appropriate one
                # TODO: The fact that is is necessary means that `Graph`
                #       should implement a __get__ method (or w/e it is)
                if node.id == tapped["id"]:

                    if node.node_type == "feat_maker":

                        try:
                            dataset_choice = pipeline_creator.find_input_node(elems).dataset
                        except AttributeError:
                            raise PreventUpdate()

                        # Get the mapping symbols
                        # These are the same now but will be changed later
                        user_columns = list(mapping_store["selected_columns"])
                        user_symbols = list(mapping_store["selected_columns"].values())

                        # left- and right-hand side
                        lhs = ','.join(user_symbols)
                        rhs = ' '.join(user_symbols)

                        # TODO: Make sure that these symbols are defined in the
                        #       correct order and that this order is preserved
                        #       when passed to the func inside the pipeline.
                        #       Line 183 probably fixes this but we need to
                        #       double check.
                        exec_commands = [
                            f"{lhs} = sympy.symbols('{rhs}')",
                            f"f = {user_text}",
                            f"lambdify( ({lhs}), f)",
                        ]

                        func_name = f"{user_id}_feat_{'-'.join(user_columns)}"
                        # Store the func to Redis, and save only the
                        # key. This is due to python functions not
                        # being JSON serializable.
                        r.set(func_name, dill.dumps(exec_commands))

                        # TODO: This needs improvement, e.g. with adding
                        #       variables in the edges and passing data
                        #       through there. The current implementation
                        #       is forced to load the dataset twice.
                        params = {"func_name": func_name,
                                  "cols": user_columns,
                                  "dataset_choice": dataset_choice,
                                  "user_id": user_id}
                        node.options["data"]["func_params"].update(params)

                    else:
                        node.options["data"]["func_params"].update({
                            modify_node_attribute: modify_node_params
                        })

    return G.render_graph()


@app.callback(Output("inspector", "children"),
              [Input("cytoscape-graph", "tapNodeData")],
              [State("user_id", "children"),
               State("cytoscape-graph", "elements")])
def inspect_node(selected, user_id, elems):


    if selected is None or "parent" not in selected:
        # No need to show info for parent nodes as
        # they are there just for show
        raise PreventUpdate()

    # Defaults
    multi = False
    dataset_choice = None

    if len(selected):
        func = node_options[selected["node_type"]]["func"]
        arguments = list(func.modifiable_params.keys())

        # func is a SKLEARN-like class
        if isinstance(func(), pipeline_classes.GenericInput):
            arguments = ["dataset"]

        options = [
            {"label": arg, "value": arg}
            for arg in arguments
        ]

    if isinstance(func(), pipeline_classes.FeatureMaker):
        # 1) Select appropriate elements and make the graph
        # 2) Create pipelines
        # 3) Iterate over them to find the one with FeatureMaker node
        # 4) Iterate over that again to find its input node

        input_node = pipeline_creator.find_input_node(elems)

        try:
            dataset_choice = input_node.dataset
        except AttributeError:
            return [
                html.H4("Something went wrong with the input"),

                # for debugging a global callback
                *create_dropdown("", [], id="modify_option_dropdown",
                                 style={"display": "none"}),

                *debugger_layout,
            ]

        df = get_data(dataset_choice, user_id)

        # Truncate labels so they don't fill the whole dropdown
        options = [{'label': col[:35], 'value': col} for col in df.columns]
        multi = True

    return [
        html.Div([
            *create_dropdown("Options", options,
                             id="modify_option_dropdown",
                             multi=multi),

            html.Div([], id="other_menus"),

            # here only to debug the modify_graph callback
            *debugger_layout,

        ]),
    ]


@app.callback(Output("other_menus", "children"),
              [Input("modify_option_dropdown", "value")],
              [State("cytoscape-graph", "tapNodeData"),
               State("user_id", "children")])
def update_radio_buttons_modify_params(value, selected, user_id):


    if selected is None or value is None:
        return [html.H4("Nothing selected.")]

    if len(selected):
        func = node_options[selected["node_type"]]["func"]

        # func is a sklearn-like class
        if isinstance(func(), pipeline_classes.GenericInput):
            if isinstance(func(), pipeline_classes.TwitterAPI):
                twitter_data = r.keys(f"{user_id}_twitter_data_*")
                choices = [{"label":k.decode(), "value": k.decode()} for k in twitter_data]
            else:
                choices, _ = get_available_choices(r, user_id)

        elif isinstance(func(), pipeline_classes.FeatureMaker):
            return [
                html.Div(id="data_holder"),
                html.Div(id="sympy_output"),
            ]

        else:
            choices = [
                {"label": str(val), "value": val}
                for val in func.modifiable_params[value]
            ]

    return [
        dcc.RadioItems(options=choices, id="modify_node_params",
                      labelStyle={
                          'display': 'inline-block',
                          'margin': '5px'
                      }),
    ]


@app.callback(Output("delete_options", "options"),
              [Input("cytoscape-graph", "elements")],
              [State("user_id", "children")])
def inspect_node(elements, user_id):


    return [{
        "value": elem["data"]["id"],
        "label": elem["data"]["label"]
        } for elem in elements if (elem["data"].get("source") is None) and
                                  ("parent" in elem["data"])]


@app.callback([Output("modal", "is_open"),
               Output("model_specs", "children")],
              [Input("convert", "n_clicks"),
               Input("close", "n_clicks")],
              [State("cytoscape-graph", "elements"),
               State("cytoscape-graph", "stylesheet"),
               State("user_id", "children"),
               State("modal", "is_open")])
def convert_model(n_clicks, close, elements, layout, user_id, is_open):

    if user_id.startswith("python_generated_ssid"):
        # Trim id
        user_id = user_id.split("-")[-1]


    if n_clicks is None:
        return [False, [html.H5("No specs defined yet")]]

    else:
        # Keep elements that are either edges (have a source)
        # or elements that have a parent (nodes, not groups)
        elements = [elem for elem in elements if (("source" in elem["data"]) or
                                                  ("parent" in elem["data"]))]

        pipelines, classifiers = pipeline_creator.create_pipelines(elements,
                                                                   node_options)

        # Save pipelines to Redis (to be used in other modules)
        for pipe, clf in zip(pipelines, classifiers):
            r.set(f"{user_id}_pipeline_{clf}", dill.dumps(pipe))

        # TODO: Make this a modal
        #       https://dash-bootstrap-components.opensource.faculty.ai/l/components/modal
        return [not is_open, [html.P(f"{i+1}) {str(pipeline)}")
                for (i, pipeline) in enumerate(pipelines)]]
