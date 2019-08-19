"""
This module will be used to graphically create models. \
RapidMiner, Weka, Orange, etc, ain't got sh!t on us :)

You should probably not write code here, UNLESS you know \
what you're doing.

Dash callbacks:
    - update_radio_buttons_modify_params: List the available options for \
                                          the selected node and parameter.
    - modify_graph: Handle everything about the model builder.
    - render_deletion_menu: Update the dropdown that lists the nodes \
                            available for deletion.
    - add_node_menu_toggle: Show/hide the menu for adding new nodes.

"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from inspect import getfullargspec

from .server import app, redis_conn
from utils import get_dataset_options
from .styles import cyto_stylesheet
from .models.graph_structures import Graph
from .models.graph_structures import node_options, ml_options
from .models.graph_structures import prebuilt_graphs
from .models import pipeline_creator

import dill
from flask_login import current_user


SideBar_modelBuilder = []

add_node_options = [
    {"label": model['label'], "value": model['node_type']}
    for model in ml_options
]

actions = ["add", "remove", "update", "prebuilt", "connect"]


def Model_Builder_Layout():

    # When the user first visits the tab, create a default pipeline.
    user_id = current_user.username
    initial_graph = Graph(prebuilt="default")
    redis_conn.set(f"{user_id}_graph_current", dill.dumps(initial_graph))
    removal_options = initial_graph.available_nodes_for_removal()

    return html.Div([
        html.Div([

            # The left side with the options
            html.Div(id="model_choices", children=[

                # Add a node
                html.Div([
                    # We need a button because the user might want to
                    # add multiple nodes of the same type, and it also
                    # makes sense for most cases, I guess
                    dcc.Dropdown(options=add_node_options, multi=False,
                                 id="add_new_node_type"),
                    html.Button("Add a node", id="add_nodes"),

                ], className="parameterMenu"),

                # Remove node
                html.Div([
                    # We need to update the delete options when nodes
                    # are added or deleted, and since it cannot be both
                    # Input and Output we need the button as an middle step
                    dcc.Dropdown(multi=False, id="remove_old_node",
                                 options=removal_options),
                    html.Button("Remove node", id="remove_nodes"),

                ], className="parameterMenu"),

                # Update a node / modify params
                html.Div([
                    # Divs that will contain the dropdown & radio buttons
                    # for the user choices of parameters. Update is kinda
                    # special because you need to tap a node and get input
                    # from Cytoscape.
                    html.Div(id="parameters_dropdown"),
                    html.Div(id="parameter_values_div"),

                    html.Button("Update node parameters", id="update_nodes"),

                ], className="parameterMenu"),

                # Choose prebuilt graph
                html.Div([
                    dcc.Dropdown(multi=False, id="prebuilt_model_choice",
                                 options=[
                                     {"value": k, "label": k}
                                     for (k, v) in prebuilt_graphs.items()
                                 ]),
                    html.Button("Load prebuilt graph", id="prebuilt_nodes"),

                ], className="parameterMenu"),

                # Connect selected nodes
                html.Div([
                    html.Button("Connect selected nodes", id="connect_nodes"),
                ], className="parameterMenu"),

                html.Div([
                    dcc.Input(id="graph_name", placeholder="Graph name..."),
                    html.Button("Save graph and export pipelines",
                                id="save_graph"),
                ], className="parameterMenu"),

            ], className="col-sm-2"),

            # The network graph
            html.Div([
                cyto.Cytoscape(
                    id='cytoscape-graph',
                    layout={'name': "preset"},
                    style={"height": "600px"},
                    elements=initial_graph.render(),
                    stylesheet=cyto_stylesheet,
                )
            ], className="col-sm-10"),

        ], className="row"),

        # A hidden div to get the outputs of all the graph operations.
        # Mainly used as a convenience for separating callbacks.
        html.Div([

            # Divs for the callbacks to work.
            # These might be removed later on if we decide to use
            # modals as the outputs of callbacks instead of divs.
            *[html.Div(id=f"{action}_div")
              for action in actions],

            # Likewise, but for modals
            *[dbc.Modal([
                dbc.ModalHeader("Graph successfully updated."),
                dbc.ModalBody(id=f"{action}_modal_new_values")
            ], id=f"{action}_modal", is_open=False)
                for action in actions+["graph"]],

            # And another for exporting graphs
            html.Div(id="graph_div"),

        ], id="hidden_div", style={"display": "none"}),
    ])


# Get the signatures from the generic Graph class
for action, func in zip(actions, [Graph.add, Graph.remove, Graph.update,
                                  Graph.prebuilt, Graph.connect]):

    extra_state = []
    if action == "update":
        extra_state.append(State("cytoscape-graph", "tapNodeData"))
    elif action == "connect":
        extra_state.append(State("cytoscape-graph", "selectedNodeData"))

    # The `callback` parameter is necessary because otherwise `action`
    # would evaluate to "connect" (the "current" value of `action` in
    # the global scope). Passing it as a kwarg is one way of handling it.
    @app.callback([Output(f"{action}_div", "children"),
                   Output(f"{action}_modal", "is_open"),
                   Output(f"{action}_modal_new_values", "children")],
                  [Input(f"{action}_nodes", "n_clicks")],
                  [State(f"{action}_{param}", "value")
                   for param in getfullargspec(func).args[1:]]+extra_state)
    def update_nodes(n_clicks, *values, callback=action):

        if all(x is None for x in values):
            raise PreventUpdate()

        user_id = current_user.username

        # Get or create the current model
        curr_model = dill.loads(redis_conn.get(f"{user_id}_graph_current"))

        # Update it
        curr_model.dispatch(callback, *values)

        # Save the modified model
        redis_conn.set(f"{user_id}_graph_current", dill.dumps(curr_model))

        # Dummy return. The explicit string conversion is needed because
        # the various values are not of the same type.
        return n_clicks, True, html.P(f"{callback.capitalize()} --> "
                                      f"{', '.join(str(x) for x in values)}")


# We get the divs as input just we need to trigger an update via
# callback. The graph is actually rendered in python and after
# each independent action. Also, the remove nodes dropdown is a
# special case. Since we can only remove nodes that exist in the
# graph, it needs to be updated as soon as the graph is update.
@app.callback([Output("cytoscape-graph", "elements"),
               Output("remove_old_node", "options")],
              [Input(f"{action}_div", "children")
               for action in actions])
def update_nodes(*n_clicks):
    if all(x is None for x in n_clicks):
        raise PreventUpdate()

    user_id = current_user.username

    # Get the current model
    curr_model = dill.loads(redis_conn.get(f"{user_id}_graph_current"))

    # Get the current nodes as options for the remove_node_dropdown
    removal_options = curr_model.available_nodes_for_removal()

    return curr_model.render(), removal_options


# Show the available parameter options for the selected node type / model
@app.callback(Output("parameters_dropdown", "children"),
              [Input("cytoscape-graph", "tapNodeData")])
def show_configurable_parameters(tap_node):

    # Default value
    options = [{"label": "No options available", "value": "none"}]
    if tap_node is not None:
        # e.g. lin_reg003 -> lin_reg
        model_type = tap_node["id"][:-4]

        model_class = node_options[model_type]["model_class"]
        parameters = list(model_class.modifiable_params.keys())

        # If the new options are empty, keep the old ones
        options = [{"label": arg, "value": arg}
                   for arg in parameters] or options

    return dcc.Dropdown(multi=False, id="update_parameters", clearable=False,
                        options=options, value=options[0]["value"]),


# According to the choice of parameter, render the choices for its values
@app.callback(Output("parameter_values_div", "children"),
              [Input("update_parameters", "value")],
              [State("cytoscape-graph", "tapNodeData")])
def show_parameter_values(parameter, tap_node):

    try:
        model_type = tap_node["id"][:-4]
        model_class = node_options[model_type]["model_class"]

        if model_type == "input_file":
            options = get_dataset_options(redis_conn)

        else:
            options = [{"label": str(val), "value": val}
                       for val in model_class.modifiable_params[parameter]]

        default_value = options[0]["value"]

        return dcc.RadioItems(value=default_value, options=options,
                              id="update_parameter_values",
                              labelStyle={'display': 'inline-block',
                                          'margin': '5px'})

    except (KeyError, TypeError):
        # KeyError: This happens when the tapped node changes. And/or we get
        #           no modifiable parameters for the tapped node's model_class.
        # TypeError: This happens when no node is tapped.
        return []


@app.callback([Output("graph_div", "children"),
               Output("graph_modal", "is_open"),
               Output("graph_modal_new_values", "children")],
              [Input("save_graph", "n_clicks")],
              [State("graph_name", "value")])
def export_graph_pipelines(n_clicks, value):

    user_id = current_user.username

    # Get current model
    curr_model = dill.loads(redis_conn.get(f"{user_id}_graph_current"))
    # Create pipelines (one for each output node)
    pipelines, terminal_nodes = pipeline_creator.create_pipelines(curr_model.graph)

    # Save pipelines
    for pipeline, terminal_node in zip(pipelines, terminal_nodes):
        redis_conn.set(f"{user_id}_pipeline_{value}_{terminal_node}",
                       dill.dumps(pipeline))

    # Save graph
    redis_conn.set(f"{user_id}_graph_{value}", dill.dumps(curr_model))

    return n_clicks, True, [
        html.P(f"{i+1}) Exported pipelines: {pipeline}")
        for i, pipeline in enumerate(pipelines)
    ]
