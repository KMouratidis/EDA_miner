import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import visdcc

# This is created above
from .doc_maker import documented_funcs_classes, total_funcs_classes
from .all_layouts import layouts
from utils import interactive_menu

import os
import re


app = dash.Dash(__name__, requests_pathname_prefix="/docs/",
                assets_external_path="http://127.0.0.1:8000/static/",)

# Any other configurations for the Dash/Flask server go here
app.config['suppress_callback_exceptions'] = True

# Create the layout for docs
layout = []
for folder, folders, files in os.walk("../EDA_miner/"):

    if not folder.endswith("/"):
        folder = folder + "/"

    # folder is not ../EDA_miner/ but starts with it
    # use this for the name of elements, not the href
    short_folder = folder
    if len(folder) > 14:
        short_folder = folder[13:]
    else:
        short_folder = folder[3:]

    children = [
        file for file in files if file.endswith(".py") and (
            not any(x in file for x in ["reportapp", "printable_layout",
                                        "users.db", "coverage", "cache",
                                        "base_dash.py", "temp_",])
    )]

    if not len(children) or ("dash_rnd" in folder):
        continue

    html_acceptable_folder = folder.replace("..", "-").replace("/", "-")

    layout.append(
        html.Div([
            html.Button(short_folder, id="collapse-button-"+html_acceptable_folder,
                        className="folderMenu", n_clicks=0),
            dbc.Collapse(
                dbc.Card([html.Div(
                    dcc.Link(link if not link.startswith("__init__") else short_folder[:-1],
                             href="/docs/" + short_folder + link,
                             style={"textDecoration": "none"}))
                          for link in children]),
                id="collapse_" + html_acceptable_folder,
                className="collapsibleMenu"
            ),
        ])

    )

    # Create 1 callback for each package
    @app.callback(
        Output("collapse_" + html_acceptable_folder, "is_open"),
        [Input("collapse-button-" + html_acceptable_folder, "n_clicks")],
        [State("collapse_" + html_acceptable_folder, "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n % 2 == 1:
            return True
        else:
            return False


app.layout = html.Div([

    *interactive_menu(output_elem_id="sidenav2_contents"),

    visdcc.Run_js(id='open_sidebar2', run="""openNav2()"""),

    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    # content will be rendered in this element
    html.Div(id='page-content',
             style={"display": "inline-block", "width": "75%"})
])


@app.callback(Output("sidenav2_contents", "children"),
              [Input('url', 'value')])
def render_sidemenu(url):
    """
    Render the menu in the side-navbar.

    Args:
        url (str): The url on the Location element.

    Returns:
        A Dash element or list of elements.
    """

    return html.Div(layout, id="nagivation",
                    style={"display": "inline-block",
                           "width": "15%",
                           "marginTop": "35px",
                           "verticalAlign": "top"}),


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    try:
        if "EDA_miner/" in pathname:
            layout = layouts.get("/home/kmourat/GitHub/EDA_miner/" + pathname[6:-3],
                                 "No docstrings written here. Bummer...")

        else:
            layout = layouts.get("/home/kmourat/GitHub/EDA_miner/EDA_miner/"+pathname[6:-3], "BOOM")

        if len(layout):
            return layout
        else:
            return html.H4(f"File {pathname[6:-3]} doesn't have any docs")

    except (KeyError, TypeError):
        return html.Div(str(layouts.keys()))


parent_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
with open(parent_dir + "/project_info.txt", "r") as f:
    rd = f.read()

with open(parent_dir + "/project_info.txt", "w") as f:
    f.write(re.sub("numeric: doc-coverage: \d+%", f"numeric: "
        f"doc-coverage: {str(int((documented_funcs_classes/total_funcs_classes)*100))}%", rd))


server = app.server
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8084)
