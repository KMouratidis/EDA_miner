## First create the docs

import os
import re


text = []

handler = text.append

handler("""
import dash
import dash_core_components as dcc
import dash_html_components as html

layouts = {}

""")
    
    
total_funcs_classes = 0
documented_funcs_classes = 0

for folder, folders, files in os.walk("../EDA_miner/"):
    for file in files:

        if not file.endswith(".py"):
            continue
        
        if not folder.endswith("/"):
            folder = folder + "/"
            
        with open(folder + file) as f:
            rd = f.readlines()


        doc = False
        add_to_next = False
        prev_line = ""

        handler(f"""

layouts["{folder}{file[:-3]}"] = html.Div([""")


        for i, line in enumerate(rd):
            # If func/class and not private
            if ("def " in line or "class " in line) and not (line.strip().startswith("def _") or line.strip().startswith("class _") or line.strip().startswith("#")) and not doc:
                total_funcs_classes += 1; print("LINE: ", line)

            if '"""' in line:
                doc = not doc

                if i >= 1 and doc:
                    # function name
                    
                    correct_line = i - 1
                    if "def " not in rd[correct_line] and "class " not in rd[correct_line]:
                        while not ("def " in rd[correct_line] or "class " in rd[correct_line]):
                            correct_line -= 1
                    documented_funcs_classes += 1 ; print("DOCUMENTED: ",line)
                                                    
                    if correct_line < i - 1:
                        line = " ".join(rd[j].strip() for j in range(correct_line, i))
                        
                        
                    handler(f'html.Br(), html.H3("""{rd[correct_line].replace("class ", "").replace("def ", "").strip()}""", style={{"backgroundColor": "#AAA", "display": "inline"}}), ')
                    handler("html.Div([")

                        
                    continue
                elif i >= 1 and not doc:
        #             handler(line)
                    handler("""], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),\n""")
                    pass

                    continue

                elif i == 0 and doc:
                    handler(f'html.H2("""{file}"""), ')
                    handler("html.Br(), html.Div([")


            elif doc:
                
                if not len(line):
                    continue


                if line.strip().endswith("\\"):
                    add_to_next = True
                    prev_line = prev_line + line.strip()[:-1]
                    continue

                elif add_to_next:
                    line = prev_line + line


                if line.strip().endswith(":") or line.strip().endswith("!"):
                    line = f'html.H3("""{line.strip()}"""), '

                elif line.strip().startswith("-"):
                    line = f'html.Li("""{line.strip()[1:]}"""), '

                elif not line.strip().startswith("<"):
                    line = f'html.P("""{line.strip()}"""), '


                handler("\t"+line.strip())

                if not line.strip().endswith("\\"):
                    prev_line = ""
                    add_to_next = False

        handler("])\n")


with open("all_layouts.py", "w") as f:
    f.write("\n".join(text))


## Load the docs and run the server

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# This is created above
from all_layouts import layouts


external_stylesheets = ["https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
                        'https://codepen.io/chriddyp/pen/bWLwgP.css',]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Any other configurations for the Dash/Flask server go here
app.config['suppress_callback_exceptions'] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# This is what the rendered html will look like
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>

        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        
        {%metas%}
        <title>EDA Miner</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div class="app0">{%app_entry%}</div>

        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


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

    children = [file for file in files if file.endswith(".py")]

    if not len(children):
        continue

    layout.append(
        html.Div([
            dbc.Button(short_folder, id="collapse-button-"+folder.replace("..", "-").replace("/", "-"),
                       style={"width": "90%"}),
            dbc.Collapse(
                dbc.Card([html.Div(
                    dcc.Link(link, href="/" + folder + link if folder.endswith("/")
                    else folder + "/" + link,
                             style={"textDecoration": "none"}))
                          for link in children]),
                id="collapse_" + folder.replace("/", "-").replace("..", "-"),
                style={"width": "90%"}
            ),
        ])

    )

    # Create 1 callback for each package
    @app.callback(
        Output("collapse_"+folder.replace("..", "-").replace("/", "-"), "is_open"),
        [Input("collapse-button-"+folder.replace("..", "-").replace("/", "-"), "n_clicks")],
        [State("collapse_"+folder.replace("..", "-").replace("/", "-"), "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open


app.layout = html.Div([

    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    html.Div(layout, id="nagivation",
             style={"display": "inline-block",
                    "width": "15%",
                    "verticalAlign": "top"}),


    # content will be rendered in this element
    html.Div(id='page-content',
             style={"display": "inline-block", "width": "75%"})
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    try:
        return layouts.get(".."+pathname[:-3])
    except (KeyError, TypeError):
        return html.Div(str(layouts.keys()))


with open("../project_info.txt", "r") as f:
    rd = f.read()

with open("../project_info.txt", "w") as f:
    f.write(re.sub("numeric: doc-coverage: \d+%", f"numeric: doc-coverage: {str(int(documented_funcs_classes/total_funcs_classes*100))}%", rd))


server = app.server
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8084)
