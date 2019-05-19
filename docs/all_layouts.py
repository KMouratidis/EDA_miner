
import dash
import dash_core_components as dcc
import dash_html_components as html

layouts = {}




layouts["../EDA_miner/__init__"] = html.Div([
html.H2("""__init__.py"""), 
html.Br(), html.Div([
	html.H3("""Welcome to EDA Miner!"""),
	html.P(""""""),
	html.H3("""Usage walk-through:"""),
	html.P("""We strive to create a simple and intuitive interface. The app is meant to be run in a central server and accessed via web, but can of course be run locally, too."""),
	html.P(""""""),
	html.P("""Upon visiting the page you will be directed to the "Data View" tab where you upload your own datasets, connect to APIs, or view the data you have uploaded. When viewing your data, each API displays data in different ways, although actually using those data is not yet implemented (May 2019)."""),
	html.P(""""""),
	html.P("""As soon as you have uploaded a dataset, the other two tabs become functional. The first stop would be the "Explore & Visualize" tab. Here you will find options to plot your data; each sub-tab contains a different class of visualizations."""),
	html.Li(""" Exploratory analysis: contains all the 2D graphs, including                             matplotlib-generated pairplots."""),
	html.Li(""" Key performance indicators: currently implements only a baseline graph, but we plan to implement functionality so you can create your own KPIs, and we want to add additional                                   analysis tools."""),
	html.Li(""" 3D graphs: currently only plots 3D scatterplots."""),
	html.Li(""" Network graphs: use Cytoscape.js to create graph/network                       visualizations, allowing various layout choices."""),
	html.Li(""" Text visualizations: currently only allow for creating simple word clouds (from given text), but plans for further integration and more visualizations include                            word vector visualization."""),
	html.Li(""" PDF report: allows you to create reports using the figures you plot in the other tabs (using the "export graph                   config" buttons) and add custom text, headers, titles."""),
	html.P(""""""),
	html.P(""""""),
	html.P("""Finally, in the "Analyze & Predict" tab you are able to use your data to train Machine Learning models. The Model builder can be used to create more advanced pipelines (including defining your own features). The default steps are to first define the model fully (or some features may not work), then go over every node you want to customize and change its node options, and when you're done export the model ("convert to model" button). Finally, head over to the "Pipelines trainer" tab, select and train your model. If you want to run simpler models, there are additional tabs with the most common types of problems."""),
	html.P(""""""),
	html.P(""""""),
	html.H3("""Project structure:"""),
	html.P("""Contributors wanting to familiarize themselves with the project structure can take a look at the contributor guidelines (https://github.com/KMouratidis/EDA_miner_public/wiki/Style-guide-and-contributor-guidelines). You can also go through all the files and read the module docstrings that have rough guidelines about contributions. In the Python     spirit, feel free to completely ignore them."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/styles"] = html.Div([
html.H2("""styles.py"""), 
html.Br(), html.Div([
	html.P("""This module is meant as a collection of styles that cannot be defined in the CSS (e.g. due to JS/Dash libraries' rendered elements not being viewable in inspection, or some overriding)."""),
	html.P(""""""),
	html.H3("""Available styles:"""),
	html.Li(""" cyto_stylesheet: The style used for the Model Builder, and will probably also be used for other cytoscape                        visualizations."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/layouts"] = html.Div([
html.H2("""layouts.py"""), 
html.Br(), html.Div([
	html.P("""Similar to `styles.py`, this module is mean as a collection of layouts to be used across the dash app. A layout is about what components exist in any view (e.g. html elements) whereas a style is about... styling! Styles are implemented as functions to allow use with different parameters."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" default_2d: Layout for most plotly graphs."""),
	html.Li(""" default_3d: Layout for 3D graphs, not implemented."""),
	html.Li(""" default_kpi: Layout for KPI graphs, not implemented."""),
	html.P(""""""),
	html.H3("""Classes:"""),
	html.Li(""" PDF_Layout1: A sample PDF layout, more to be added. Implemented as a class out of convenience, may be changed later.                    Usage: `PDF_Layout1.render(x_axis, y_axis)`."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Feel free to tamper with all of the functions and classes below and/or add your own. Beware that in some cases (e.g. defining a new PDF layout) you might need to make changes in other files,     or at least wait till needed functionality is added."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""default_2d(xvars, yvars):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Default `go.Layout` for 2D graphs."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""xvars: str, title of the x-axis."""),
	html.P("""yvars: str, title of the y-axis."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""A `go.Layout` instance."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""default_3d(xvars, yvars, zvars):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Default `go.Layout` for 3D graphs. Currently same as default_2d."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""xvars: str, title of the x-axis."""),
	html.P("""yvars: str, title of the y-axis."""),
	html.P("""zvars: str, currently not used."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""A `go.Layout` instance."""),
	html.P(""""""),
	html.H3("""Todo:"""),
	html.P("""This needs a better implementation"""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""default_kpi(xvars, yvars):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Default `go.Layout` for KPI graphs. Currently same as default_2d."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""xvars: str, title of the x-axis."""),
	html.P("""yvars: str, title of the y-axis."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""A `go.Layout` instance."""),
	html.P(""""""),
	html.H3("""Todo:"""),
	html.P("""This might need a better implementation"""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""PDF_Layout1:""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""This class is meant to capture all specifications needed to create a report layout. This isn't currently implemented correctly, it merely serves as a placeholder, not a template to be mimicked. The elements present below are being used elsewhere to create     the layout of the the PDF, but those will probably moved here."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/utils"] = html.Div([
html.H2("""utils.py"""), 
html.Br(), html.Div([
	html.P("""This module provides utilities, functions, and other code that is meant to be used across the app. This may undergo changes soon."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" cleanup: Clean up after the Dash app exits."""),
	html.Li(""" create_dropdown: Create a dropdown with a title."""),
	html.Li(""" create_table: Creates a `dash_table.DataTable` given a `pd.DataFrame`."""),
	html.Li(""" encode_image: Read and base64-encode an image for the dash app."""),
	html.Li(""" get_data: Get a `pandas.DataFrame` with the specified data."""),
	html.Li(""" hard_cast_to_float: Convert to float or return 0."""),
	html.Li(""" parse_contents: Decode uploaded files and store them in Redis."""),
	html.Li(""" pretty_print_tweets: Create H5 elements from the user's Twitter                            timeline."""),
	html.Li(""" redis_startup: Connect to a Redis server & handle startup."""),
	html.P(""""""),
	html.H3("""Global variables:"""),
	html.Li(""" r: A Redis connection that is used throughout the app."""),
	html.Li(""" mapping: A dict that maps tags to sklearn models meant for                creating dropdowns and used in `apps.analyze` modules."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""You should probably not write code here, unless you are adding functions aimed at being used by many lower-level modules. Some of the functions here will later be moved to lower-level     modules (e.g. `pretty_print_tweets`)."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""cleanup(redis_conn):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Clean up after the Dash app exits."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""redis_conn: `redis.Redis` object."""),
	html.P(""""""),
	html.H3("""Further details:"""),
	html.P("""Flush every key stored in the Redis database. If there are users that have logged in and uploaded data, store those on disk. Also remove any static files generated         while the server was running."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""create_dropdown(name, options, **kwargs):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Create a dropdown with a title."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""name (str): the title above the dropdown."""),
	html.P("""options (list(dict)): dictionaries should contain keys at least                              the keys (label, value)."""),
	html.P("""**kwargs: keyword-value pairs. Accepts any keyword-arguments                   that can be passed to `dcc.Dropdown`."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: an H5 and the Dropdown."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""create_table(df, table_id="table"):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Creates a `dash_table.DataTable` given a `pandas.DataFrame`."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""df (`pandas.DataFrame`): the data."""),
	html.P("""table_id (str, optional): id of the table element for usage                                   with dash callbacks."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""A `dash_table.DataTable` with pagination."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""encode_image(image_path):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Read and base64-encode an image for the dash app</h2>"""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""image_path (str): absolute path or relative to the                           top-level directory"""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""A str to be used for the src attribute of an img element."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""get_data(api_choice, user_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Get a `pandas.DataFrame` with the specified data."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""api_choice (str): the key used by the Redis server                           to store the data."""),
	html.P("""user_id (str): the user for whom to fetch data."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""hard_cast_to_float(x):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Convert to float or return 0."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""x (anything): will be type-casted or 0'ed."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""float."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""parse_contents(contents, filename, date, user_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Decode uploaded files and store them in Redis."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""contents (str): the content of the file to be decoded."""),
	html.P("""filename (str): name of uploaded file."""),
	html.P("""date (str): (modification?) date of the file."""),
	html.P("""user_id (str): the user for whom to fetch data."""),
	html.P(""""""),
	html.H3("""Further details:"""),
	html.P("""After decoding the uploaded file, handle any remaining operations here. This was stolen from the dash docs. Currently         it only supports csv, xls(x), json, and feather file types."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""pretty_print_tweets(api, n_tweets):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Create H5 elements from the user's Twitter timeline."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""api (`twitter.Api`): a connection to Twitter                              with verified credentials."""),
	html.P("""n_tweets (int): the number of tweets to display."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""redis_startup():""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Connect to a Redis server & handle startup."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""`redis.Redis`: a connection to a Redis server."""),
	html.P(""""""),
	html.H3("""Further details:"""),
	html.P("""Connects to a Redis server on its default port (6379) and         is also responsible for any other startup operations needed."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/reportapp"] = html.Div([
html.Br(), html.H3("""load_stuff(_):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""This module is meant to be used as a secondary server only for printing"""),
	html.P("""PDFs made inside the `PDF_Layout` tab."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" load_stuff: On button click, load the layout exported                   from the main app."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Improvements can definitely be made regarding handling of PDF printing,"""),
	html.P("""with particular need of javascript functionality. Help is most welcome"""),
	html.P("""here, and should be prioritized."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""load_stuff(_):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Load the layout exported from the main app when click."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""_ (int): number of times the button was clicked, not important."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""pdf_layout (obj): loaded from bytes, the dash components                           making up the PDF report."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/app"] = html.Div([
html.H2("""app.py"""), 
html.Br(), html.Div([
	html.P("""The main app is here. It takes the base menus from menus.py and puts them in the app.layout, then defines callbacks and finally has the if-name-main block necessary to run the app."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" high_level_tabs: On high-level tab selection, render                        the appropriate layout."""),
	html.Li(""" update_sidebar_menus: For the second level of tabs, show                             different sidebar menu."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.H3("""You should probably not write code here, unless:"""),
	html.Li(""" working on side-menus,"""),
	html.Li(""" working on login system,"""),
	html.Li(""" adding a new-high-level tab, or other new feature."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""high_level_tabs(tab):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""On high-level tab selection, render the appropriate layout."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""update_sidebar_menus(level2_tabs):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""For the second level of tabs, show different sidebar menu."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/server"] = html.Div([
html.H2("""server.py"""), 
html.Br(), html.Div([
	html.P("""This module is only here because of the Dash app spanning multiple files. General configurations of the underlying app and server go here as well."""),
	html.P(""""""),
	html.H3("""Global Variables:"""),
	html.Li(""" server: The underlying Flask server, probably needed only for               deployment."""),
	html.Li(""" app: The Dash server, imported everywhere that a dash callback            needs to be defined."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""DO NOT MODIFY WITHOUT PERMISSION! These settings should rarely be     tampered with, if at all."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/menus"] = html.Div([
html.H2("""menus.py"""), 
html.Br(), html.Div([
	html.P("""This module will collect all unchanging views and dash components (buttons, sidemenus, etc) so that the code in index.py is cleaner and abstracted."""),
	html.P(""""""),
	html.H3("""Global variables:"""),
	html.Li(""" SideBar: The left sidebar, meant to house the logo, and                a few extra buttons for non-app functionality."""),
	html.Li(""" MainMenu: The high-level tabs, and two placeholders for the                 low-level tabs plus a `dash_table.DataTable`."""),
	html.Li(""" SideBar: The right sidebar, meant to be used for elements that interact with the important parts of dash and providing any interactivity, customization, and                other options."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" serve_layout: The layout of our app. Defined in a function                     so as to generate different `session_id`s."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" button_toggle: On click show/hide the external links."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.H3("""You should probably not write code here, unless you're:"""),
	html.Li(""" adding a new button, external link, or similar to the sidebar,"""),
	html.Li(""" creating a login functionality,"""),
	html.Li(""" adding a new top-level menu tab, or other new feature."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""button_toggle(n_clicks):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""On click show/hide the external links."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""n_clicks: int, number of times the button was clicked."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""A style dict modifying the display CSS attribute."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""serve_layout():""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""The layout of our app needs to be inside a function so that every time some new session starts a new     session_id is generated."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/users_mgt"] = html.Div([
])



layouts["../EDA_miner/config"] = html.Div([
])



layouts["../EDA_miner/apps/__init__"] = html.Div([
html.H2("""__init__.py"""), 
html.Br(), html.Div([
	html.H3("""Developer notes:"""),
	html.P("""Here you will find all of the "apps", each is a high-level tab. The main function of the files defined here is to delegate work to lower-level modules, although the structure might later be changed.     View the respective files for more details notes."""),
	html.P(""""""),
	html.H3("""data_view.py:"""),
	html.P("""Defines the "Data View" tab. Anything that has to to do with     acquiring, editing, and viewing data."""),
	html.P(""""""),
	html.H3("""exploration_view.py:"""),
	html.P("""Defines the "Explore & Visualize" tab. Anything that has to do with     graphs and analysis (e.g. KPIs)."""),
	html.P(""""""),
	html.H3("""analyze_view.py:"""),
	html.P("""Defines the "Analyze & Predict" tab. Anything that has to do with     creating and training Machine Learning models."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/exploration_view"] = html.Div([
html.H2("""exploration_view.py"""), 
html.Br(), html.Div([
	html.P("""This module takes care of the menu and choices provided when the "Explore & Visualize" high-level tab is selected."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" tab_subpages: Given the low-level tab choice, render the                     appropriate view."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""You should probably not write code here, unless you are defining a new level-2 tab. Here you can find all visuals-generating functionality. Implementations go to their own modules down the     package hierarchy, in `apps.exploration`"""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""tab_subpages(tab, user_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Given the low-level tab choice, render the appropriate view."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""tab (str): the low-level tab."""),
	html.P("""user_id (str): the user/session uid."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""A list of HTML-dash components, usually within a div."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/analyze_view"] = html.Div([
html.H2("""analyze_view.py"""), 
html.Br(), html.Div([
	html.P("""This module takes care of the menu and choices provided when the "Analyze & Predict" high-level tab is selected."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" tab_subpages: Given the low-level tab choice, render the                     appropriate view."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""You should probably not write code here, unless you are defining a new level-2 tab. Here you can find functionality to define or train ML / NN models. Implementations go to their own modules     down the package hierarchy, in `apps.analyze`."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""tab_subpages(tab, user_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Given the low-level tab choice, render the appropriate view."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""tab (str): the low-level tab."""),
	html.P("""user_id (str): the user/session uid."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""A list of HTML-dash components, usually within a div."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/data_view"] = html.Div([
html.H2("""data_view.py"""), 
html.Br(), html.Div([
	html.P("""This module takes care of the menu and choices provided when the "Data view" high-level tab is selected."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" tab_subpages: Given the low-level tab choice, render the                     appropriate view."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""You should probably not write code here, unless you are defining a new level-2 tab. Here you can find find functionality to either upload your data, connect to an API, or view/edit already uploaded data. Implementations go to their own modules down the package     hierarchy, in `apps.data`."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""tab_subpages(tab, user_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Given the low-level tab choice, render the appropriate view."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""tab (str): the low-level tab."""),
	html.P("""user_id (str): the user/session uid."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""A list of HTML-dash components, usually within a div."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/analyze/__init__"] = html.Div([
html.H2("""__init__.py"""), 
html.Br(), html.Div([
	html.H3("""Developer notes:"""),
	html.P(""""""),
	html.H3("""Some suggestions on what could be done:"""),
	html.P(""""""),
	html.Li(""" Better reporting on fitting results."""),
	html.Li(""" Download a model."""),
	html.Li(""" Predict a test set."""),
	html.Li(""" Prettier interfaces."""),
	html.Li(""" Implement Econometrics functionality."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/analyze/Classification"] = html.Div([
html.H2("""Classification.py"""), 
html.Br(), html.Div([
	html.P("""This module defines the interface for fitting simple classification models."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" Classification_Options: Generate the layout of the dashboard."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" render_variable_choices_classification: Create a menu of dcc components for the user to choose fitting                                               options."""),
	html.Li(""" fit_classification_model: Fits any pipelines defined."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Feel free to experiment as much as you like here, although you probably     want to write code elsewhere."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""algo_choice_classification, user_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Create a menu of dcc components to select dataset, variables,"""),
	html.P("""and training options."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""dataset_choice (str): Name of dataset."""),
	html.P("""algo_choice_classification (str): The choice of algorithm type."""),
	html.P("""user_id (str): Session/user id."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: Dash elements."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""fit_classification_model(xvars, yvars, algo_choice_classification,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Take user choices and, if all are present, fit the appropriate model."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""xvars (list(str)): predictor variables."""),
	html.P("""yvars (str): target variable."""),
	html.P("""algo_choice_classification (str): The choice of algorithm type."""),
	html.P("""user_id: Session/user id."""),
	html.P("""dataset_choice: Name of dataset."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list, dict: Dash element(s) with the results of model fitting,"""),
	html.P("""and parameters for plotting a graph."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/analyze/Model_Builder"] = html.Div([
html.H2("""Model_Builder.py"""), 
html.Br(), html.Div([
	html.P("""This module will be used to graphically create models. RapidMiner, Weka, Orange, etc, ain't got sh!t on us :)"""),
	html.P(""""""),
	html.P("""You should probably not write code here, UNLESS you know what you're doing."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/analyze/Clustering"] = html.Div([
html.H2("""Clustering.py"""), 
html.Br(), html.Div([
	html.P("""TBW..."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""render_variable_choices_clustering(dataset_choice, algo_choice_clustering,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Create a menu of dcc components to select dataset, variables,"""),
	html.P("""and training options."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""dataset_choice (str): Name of dataset."""),
	html.P("""algo_choice_clustering (str): The choice of algorithm type."""),
	html.P("""user_id (str): Session/user id."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: Dash elements."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""fit_clustering_model(xvars, yvars, n_clusters, algo_choice_clustering,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Take user choices and, if all are present, fit the appropriate model."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""xvars (list(str)): predictor variables."""),
	html.P("""yvars (str): target variable; not needed."""),
	html.P("""algo_choice_clustering (str): The choice of algorithm type."""),
	html.P("""user_id: Session/user id."""),
	html.P("""dataset_choice: Name of dataset."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list, dict: Dash element(s) with the results of model fitting,"""),
	html.P("""and parameters for plotting a graph."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/analyze/Econometrics"] = html.Div([
html.H2("""Econometrics.py"""), 
html.Br(), html.Div([
	html.P("""This module defines the interface for doing econometrics stuff."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" Econometrics_Options: Generate the layout of the dashboard."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" render_variable_choices_econometrics: Create a menu of dcc components for the user to choose fitting                                             options."""),
	html.Li(""" fit_econometrics_model: Fits any models defined."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Not implemented yet. Feel free to experiment as much as you like here.     What do econometricians do other than glorified linear regressions?! :D"""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""render_variable_choices_econometrics(dataset_choice,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Create a menu of dcc components to select dataset, variables,"""),
	html.P("""and training options."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""dataset_choice (str): Name of dataset."""),
	html.P("""algo_choice_econometrics (str): The choice of algorithm type."""),
	html.P("""user_id (str): Session/user id."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: Dash elements."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""fit_econometrics_model(xvars, yvars, algo_choice_econometrics,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Take user choices and, if all are present, fit the appropriate model."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""xvars (list(str)): predictor variables."""),
	html.P("""yvars (str): target variable."""),
	html.P("""algo_choice_econometrics (str): The choice of algorithm type."""),
	html.P("""user_id: Session/user id."""),
	html.P("""dataset_choice: Name of dataset."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: Dash element(s) with the results of model fitting."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/analyze/Pipelines"] = html.Div([
html.H2("""Pipelines.py"""), 
html.Br(), html.Div([
	html.P("""This module defines the interface for fitting (pre)defined pipelines."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" Pipeline_Options: Generate the layout of the dashboard."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" render_variable_choices_pipeline: Create a menu of dcc components for the user to choose fitting                                         options."""),
	html.Li(""" fit_pipeline_model: Fits any pipelines defined."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""You should probably not write code here, UNLESS reworking the interface."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""render_variable_choices_pipeline(algo_choice_pipeline,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Create a menu of dcc components to select pipeline and variables."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""algo_choice_pipeline (str): Choice among (pre)defined pipelines."""),
	html.P("""user_id (str): Session/user id."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: Dash elements."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""fit_pipeline_model(xvars, yvars, fit_model, algo_choice_pipeline, user_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Take user choices and, if all are present, fit the appropriate model."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""xvars (list(str)): predictor variables."""),
	html.P("""yvars (str): target variable."""),
	html.P("""algo_choice_pipeline (str): Choice among (pre)defined pipelines."""),
	html.P("""user_id: Session/user id."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: Dash element(s) with the results of model fitting."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/analyze/Regression"] = html.Div([
html.H2("""Regression.py"""), 
html.Br(), html.Div([
	html.P("""This module defines the interface for fitting simple regression models."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" Regression_Options: Generate the layout of the dashboard."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" render_variable_choices_regression: Create a menu of dcc components for the user to choose fitting                                           options."""),
	html.Li(""" fit_regression_model: Fits any models defined."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Feel free to experiment as much as you like here, although you probably     want to write code elsewhere."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""render_variable_choices_regression(dataset_choice, algo_choice_regression,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Create a menu of dcc components to select dataset, variables,     and training options."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""dataset_choice (str): Name of dataset."""),
	html.P("""algo_choice_regression (str): The choice of algorithm type."""),
	html.P("""user_id (str): Session/user id."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: Dash elements."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""fit_regression_model(xvars, yvars, algo_choice_regression,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Take user choices and, if all are present, fit the appropriate model."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""xvars (list(str)): predictor variables."""),
	html.P("""yvars (str): target variable."""),
	html.P("""algo_choice_regression (str): The choice of algorithm type."""),
	html.P("""user_id: Session/user id."""),
	html.P("""dataset_choice: Name of dataset."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: Dash element(s) with the results of model fitting."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/analyze/models/__init__"] = html.Div([
html.H2("""__init__.py"""), 
html.Br(), html.Div([
	html.H3("""Developer notes:"""),
	html.P(""""""),
	html.P(""""""),
	html.H3("""Some suggestions on what could be done:"""),
	html.Li(""" Improve handling of pipeline traversal and creation."""),
	html.Li(""" Add new classes for the pipelines (inputs, transformers,     data cleaners, models)."""),
	html.Li(""" Improve handling of data / use better data structures."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/analyze/models/utils"] = html.Div([
html.H2("""utils.py"""), 
html.Br(), html.Div([
	html.P("""This module collects utility functions and models."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" baseline: Calculate the baseline for a time series."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Feel free to add or modify stuff here."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""baseline(values, min_max="min", deg=7, ema_window=7, roll_window=7,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P(""""""),
	html.H3("""Args:"""),
	html.H3("""values (iterable(int)):"""),
	html.P("""min_max (str): Whether to calculate an upper or lower baseline."""),
	html.P("""deg (int): The degree of the polynomial fitting."""),
	html.P("""ema_window (int): Window for the exponential moving average."""),
	html.P("""roll_window (int): Window for the simple moving average."""),
	html.P("""max_it (int): Number of iterations for `peakutils.baseline`."""),
	html.P("""tol (float): Least amount of change before termination of fitting                      in `peakutils.baseline`."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""np.array: the baseline."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/analyze/models/graph_structures"] = html.Div([
html.H2("""graph_structures.py"""), 
html.Br(), html.Div([
	html.P("""This module collects function to traverse the ModelBuilder graph."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" create_pipelines: Create pipelines from cytoscape elements and a                         dict that maps a node type to relevant parameters."""),
	html.H3("""- find_pipeline_input:"""),
	html.P(""""""),
	html.H3("""Classes:"""),
	html.Li(""" Node: A class to hold data for the nodes. Validation and advanced             functionality may be added later."""),
	html.P(""""""),
	html.H3("""Global variables:"""),
	html.Li(""" ml_options (list(dict)): The available sklearn-like classes for use                                with the ModelBuilder."""),
	html.Li(""" node_options (dict): Reverse mapping of ml_options."""),
	html.Li(""" orders (dict): The vertical ordering (position) of groups of nodes."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Feel free to add or modify stuff here, but be cautious. You probably need experience with graphs and/or trees and traversal algorithms.     The current implementation (unless I'm mistaken) are Breadth-First."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""Node:""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""A class to hold data for the nodes. Validation and advanced     functionality may be added later."""),
	html.P(""""""),
	html.P("""Create the node either by supplying `options` or `node_type` and     a `note_id`."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""options (dict): A cytoscape element."""),
	html.P("""node_type (str): One of the keys of node_options."""),
	html.P("""node_id (str): Unique node identifier."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""NodeCollection:""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""A collection of nodes with some added functionality for rendering them."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""nodes (list(dict)): A list of Cytoscape elements."""),
	html.P("""graph (`Graph`): The parent instance."""),
	html.P(""""""),
	html.H3("""Attributes:"""),
	html.P("""parent_nodes (list(dict)): Cytoscape elements that function as                                    parent/group nodes."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""add_node(self, node_type):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Add a new node given a node_type. Generate the ID based on         the previous max for ID for the selected node type."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""node_type(str): One of the keys of node_options."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""None"""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""remove_node(self, node_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Remove a node and its edges."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""node_id (str): ID of the node to be removed."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""None"""),
	html.P(""""""),
	html.H3("""Notes on implementation:"""),
	html.P("""Consider whether connecting the nodes that were connected to             the removed node."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""EdgeCollection:""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""A collection of edges with some added functionality for rendering them."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""edges (list(dict)): A list of Cytoscape elements."""),
	html.P("""graph (`Graph`): The parent instance."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""add_edges(self, selected):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Add edges between the selected nodes."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""selected (list(dict)): A list of Cytoscape elements."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""None"""),
	html.P(""""""),
	html.H3("""Notes on implementation:"""),
	html.P("""Currently, edges take their direction according to the order in which the nodes where clicked, not allowing             going back but allowing connections within the same level."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""Graph:""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""A Graph to hold collections of nodes and edges and perform functions     on them."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""elems (list(dict)): A list of Cytoscape elements."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""render_graph(self):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Calculates positions for all nodes in the graph and render it."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list(dict): A list of Cytoscape elements."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""GraphUtils:""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""To be used for default layouts. This definitely needs a better implementation to be able to handle more advanced pipelines, and/or     provide better interface."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""steps (list(tuples): Pipeline steps in the following format:                              (order, node_type, description)."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/analyze/models/pipeline_classes"] = html.Div([
html.H2("""pipeline_classes.py"""), 
html.Br(), html.Div([
	html.P("""This module collects every model class, including input and transformers."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Feel free to tamper with anything or add your own models and classes. Everything should implement an sklearn-like API providing a fit and (more importantly) a transform method. It should also have a `modifiable_params` dictionary with the names of attributes that can be modified and a list of possible values (keep them limited, for now). Input classes should subclass `GenericInput`. If you add new classes     remember to modify `ml_options` in `graph_structures.py`."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""BaseInput(BaseEstimator, TransformerMixin):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""pass"""),
	html.P(""""""),
	html.P(""""""),
	html.H3("""class GenericInput(BaseInput):"""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/analyze/models/pipeline_creator"] = html.Div([
html.H2("""pipeline_creator.py"""), 
html.Br(), html.Div([
	html.P("""This module collects function to traverse the ModelBuilder graph."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" create_pipelines: Create pipelines from cytoscape elements and a                         dict that maps a node type to relevant parameters."""),
	html.Li(""" find_pipeline_input: Given a goal creates a function that searches a pipeline for nodes of that type (or its subclasses). Essentially goes the reverse way                            of `create_pipelines`."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Feel free to add or modify stuff here, but be cautious. You probably need experience with graphs and/or trees and traversal algorithms.     The current implementation (unless I'm mistaken) are Breadth-First."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""create_pipelines(data, node_options):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Create pipelines from cytoscape elements and a dict that maps a node     type to relevant parameters."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""data (list(dict)): Cytoscape elements."""),
	html.P("""node_options (dict): Parameters to be passed at the classes as                              they are instantiated for the pipeline(s)."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list, list: The pipelines and the terminal nodes."""),
	html.P(""""""),
	html.H3("""Notes on implementation:"""),
	html.P("""This uses networkx for easier traversal. Feel free to implement         your own travel if you want to."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""find_pipeline_node(GOAL):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Given a goal creates a function that searches a pipeline for nodes of that type (or its subclasses). Essentially goes the reverse way of     `create_pipelines`."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""GOAL (sklearn-like class): Stopping criteria / node for the recursion."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""The node of type `GOAL`, if found, else `None`."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/data/__init__"] = html.Div([
html.H2("""__init__.py"""), 
html.Br(), html.Div([
	html.H3("""Developer notes:"""),
	html.P(""""""),
	html.H3("""Some suggestions on what could be done:"""),
	html.Li(""" Implementing the editing and filtering of datasets."""),
	html.Li(""" A "download" button for datasets that were modified."""),
	html.Li(""" More API connections."""),
	html.Li(""" Prettier interfaces."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/data/APIs"] = html.Div([
html.H2("""APIs.py"""), 
html.Br(), html.Div([
	html.P("""This module defines the interface for connecting to APIs. It renders the appropriate layout according to the tab chosen."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" api_connect: Render the appropriate view for the chosen API."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""You should probably not write code here, UNLESS you first defined a new connection to an API (also update View module). Remember to include the elements necessary for the app to function correctly (see `debugger_layout`), or feel free to     rework the whole thing if you can."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/data/View"] = html.Div([
html.H2("""View.py"""), 
html.Br(), html.Div([
	html.P("""This module provides views for the data (tables, lists of tweets, etc)."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" get_available_choices: Get datasets available to user."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" display_subdataset_choices: Show/hide input field for Quandl API."""),
	html.Li(""" render_table: Create a display for the chosen dataset."""),
	html.Li(""" display_reddit_posts: For the Reddit API, allow the user to                             specify a subreddit to get data from."""),
	html.P(""""""),
	html.H3("""Note to others:"""),
	html.P("""You should probably not write code here, UNLESS you defined a     new connection to an API, or are doing refactoring."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""get_available_choices(redis_conn, user_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Get datasets available to user."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.H3("""redis_conn (`redis.Redis`):"""),
	html.P("""user_id (str): Session/user id."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""[list(dict), dict]: A list of options to be used for making dropdowns, and a dict of the available                             dataset keys (and their mapped data)."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""display_subdataset_choices(api_choice):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Show/hide input field for Quandl API."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""api_choice (str): Value from the dropdown."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""dict: CSS style."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""render_table(api_choice, user_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Create a display for the chosen dataset."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""api_choice (str): Value from the dropdown."""),
	html.P("""user_id (str): Session/user id."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: A list of dash components."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""display_reddit_posts(n_clicks, subreddit_choice, user_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""For the Reddit API, allow the user to specify a subreddit     to get data from."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""n_clicks (int): Number of times button was clicked."""),
	html.P("""subreddit_choice (str): The name of the subreddit."""),
	html.P("""user_id (str): Session/user id."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: A list of dash components."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/data/Upload"] = html.Div([
html.H2("""Upload.py"""), 
html.Br(), html.Div([
	html.P("""This module provides an interface for uploading and handling of files."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" parse_uploads: Load and store the uploaded data."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""You should probably not write code here, unless you mean to implement new filetype uploads or other types of upload handling,     or other similar functionality."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""parse_uploads(list_of_contents, list_of_names,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Load and store the uploaded data."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""list_of_contents (list(bytes)): The file contents that need to                                         be parsed."""),
	html.P("""list_of_names (list(str)): The original filenames."""),
	html.P("""list_of_dates (list(str)): The modification (?) dates of files."""),
	html.P("""user_id (str): Session/user id."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: A list of dash components."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/data/data_utils/api_connectors"] = html.Div([
html.H2("""api_connectors.py"""), 
html.Br(), html.Div([
	html.P("""This module collects the layouts for connecting to the various APIs."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" twitter_connect: Connect to the Twitter API."""),
	html.Li(""" google_sheets_connect: Connect to the Google Sheets API."""),
	html.Li(""" reddit_connect: Connect to the Reddit API."""),
	html.Li(""" spotify_connect: Connect to the Spotify API."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""You should probably not write code here, unless adding     a new API connection (or improving existing ones)."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""twitter_connect(consumer_key, consumer_secret, access_token_key,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Connect to Twitter API and store the handle in Redis."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""google_sheets_connect(credentials_file, gspread_key):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Connect to Google Sheets and store the data in Redis."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""reddit_connect(client_id, client_secret):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Connect to Reddit and store the handle in Redis."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""spotify_connect(client_id, client_secret):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Connect to Spotify and store the handle in Redis."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/data/data_utils/__init__"] = html.Div([
html.H2("""__init__.py"""), 
html.Br(), html.Div([
	html.H3("""Developer notes:"""),
	html.P(""""""),
	html.P("""The modules here are for implementing utilities needed by higher-level"""),
	html.H3("""modules. Some suggestions on what could be done:"""),
	html.Li(""" Add new API connections (note: you need to implement both"""),
	html.P("""the connector and define a layout/form)."""),
	html.Li(""" Fix the bug that made me pollute the whole file with those"""),
	html.P("""ugly debugger layouts."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/data/data_utils/api_layouts"] = html.Div([
html.H2("""api_layouts.py"""), 
html.Br(), html.Div([
	html.P("""This module collects the layouts for connecting to the various APIs."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" success_message: Notify the user for successful connection."""),
	html.P(""""""),
	html.H3("""Global variables:"""),
	html.Li(""" twitter_layout: 4 input fields and a button."""),
	html.Li(""" gsheets_layout: 2 input fields and a button."""),
	html.Li(""" reddit_layout: 2 input fields and a button."""),
	html.Li(""" quandl_layout: 2 input fields and a button."""),
	html.Li(""" spotify_layout: 2 input fields and a button."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""You should probably not write code here, unless adding     a new API connection."""),
	html.P(""""""),
	html.P("""IMPORTANT: When designing layouts ALWAYS pre-append the input elements with the API name, and ALWAYS name each input id according to the names of the variables of the respective API     connector."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""success_message(api):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Utility to provide feedback on successful connections."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""api (str): Name / key of the API."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: A list of Dash elements."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/exploration/__init__"] = html.Div([
html.H2("""__init__.py"""), 
html.Br(), html.Div([
	html.H3("""Developer notes:"""),
	html.P(""""""),
	html.P("""**Do not add graph functions here.** Some suggestions on what"""),
	html.H3("""could be done here:"""),
	html.Li(""" Prettify layout and user interface."""),
	html.Li(""" Implement the interface to allow the user to create their own KPIs."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/exploration/PDF_report"] = html.Div([
html.H2("""PDF_report.py"""), 
html.Br(), html.Div([
	html.P("""This module is about rendering and potentially printing PDF reports."""),
	html.P(""""""),
	html.H3("""Global Variables:"""),
	html.Li(""" Sidebar: To be used for creating side-menus."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" PDF_report_options: Generate the layout of the PDF generator."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" render_pdf_func: Render the PDF by filling-in the templates                        using the user-provided choices and texts."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""** FEEL FREE TO SUBMIT YOUR OWN MWE DASH APPS (LAYOUT + STYLE). ** Contributions are greatly encouraged here, and this is a great starting point if you are new to dash or this project. What needs to be done is mainly creating PDF templates (see also the example at `layouts.PDF_Layout1`), but main functionality is also lacking. Feel free to add new buttons, input, or other interface-related, element. Also, contributions on a better export/render system are     welcome, although slightly more advanced."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""render_pdf_func(n_clicks, exported_figure1, exported_figure2,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Render the PDF by filling-in the templates using the user-provided     choices and texts."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""n_clicks (int): Number of times render button was clicked."""),
	html.P("""exported_figure1 (dict): a dict containing the figure information                                  from a hidden div."""),
	html.P("""exported_figure2 (dict): Same as above."""),
	html.P("""row1col1_text (str): User text written in one of the `textarea`s                              provided by the template."""),
	html.P("""header_input (str): User text written as the PDF title."""),
	html.P("""row1_header_input: User text written as a title of the first                            section."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""[dict, dict, list, list, list]: Returns the two figures, and three lists containing elements to fill                                         the respective divs."""),
	html.P(""""""),
	html.H3("""Notes on implementation:"""),
	html.P("""This function (including the previous layout) are only defined for 1 report template. Additions to this page will most probably lead to to inserting new elements in the initial layout or changing the whole implementation completely. Feel free to discuss what you         would like to see implemented for you to use, or even your ideas."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""print_pdf(n_clicks1, n_clicks2, pdf_layout):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""function printExternal() {"""),
	html.P("""let printWindow = window.open( "http://127.0.0.1:8051","""),
	html.P("""'Print', 'left=200, top=200, width=950, height=500, toolbar=0, resizable=0');"""),
	html.P("""printWindow.addEventListener('load', function(){"""),
	html.P("""printWindow.print();"""),
	html.P("""printWindow.close();"""),
	html.P("""}, true);"""),
	html.P("""}"""),
	html.P(""""""),
	html.P(""""""),
	html.P("""let printPDF = document.getElementById("print_PDF");"""),
	html.P("""printPDF.onclick = printExternal;"""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/exploration/Networks"] = html.Div([
html.H2("""Networks.py"""), 
html.Br(), html.Div([
	html.P("""This module is about viewing network data."""),
	html.P(""""""),
	html.H3("""Global Variables:"""),
	html.Li(""" Sidebar: To be used for creating side-menus."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" Network_Options: Generate the layout of the dashboard."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" render_variable_choices_network: Create a menu of dcc components for the user to choose plotting                                        options."""),
	html.Li(""" plot_network: Plot the network graph according to user choices."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Contributions are encouraged here, although you should consider starting with another part if you're new to dash or this project. Main functionality is still lacking in this part. You can use this module to add new buttons, input, or other interface-related, element, or maybe a new type of graph (in which case implement it in a new file `graphs.networks.py`). Like with other modules,     working on exporting network graphs is encouraged."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""render_variable_choices_network(dataset_choice, user_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Create a menu of dcc components for the user to choose         plotting options."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""dataset_choice (str): Name of dataset."""),
	html.P("""user_id (str): Session/user id."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list(list(dict)): Key-value pairs to be input as                           `dcc.Dropdown` options."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""plot_network(in_node, out_node, layout_choice, user_id,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Plot the network graph according to user choices."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""in_node (str): Column name containing the values of                       nodes from where links start."""),
	html.P("""out_node (str): Column name for nodes where links end."""),
	html.P("""layout_choice (str): One of the layouts available in                              Cytoscape."""),
	html.P("""user_id (str): Session/user id."""),
	html.P("""dataset_choice_network (str): Name of dataset."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""[list(dict), dict]: A list of elements (dicts for Cytoscape)                             and the layout for the graph."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/exploration/KPIs"] = html.Div([
html.H2("""KPIs.py"""), 
html.Br(), html.Div([
	html.P("""This module is about building and viewing KPIs. The user should be able to view more advanced graphs and also create their own indicators."""),
	html.P(""""""),
	html.H3("""Global Variables:"""),
	html.Li(""" Sidebar: To be used for creating side-menus."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" KPI_Options: Generate the layout of the dashboard."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" render_variable_choices_kpi: Create a menu of dcc components for                                    the user to choose  plotting options."""),
	html.Li(""" plot_graph_kpi: Plot the graph according to user choices."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Contributions are greatly needed and encouraged here. Main functionality is still lacking in this part. You can use this module to add new buttons, input, or other interface-related, element, or maybe a new type of graph (in which case implement it in `graphs.kpis.py`). Working on exporting KPI graphs is     also encouraged."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""render_variable_choices_kpi(dataset_choice, user_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Create a menu of dcc components for the user to choose     plotting options."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""dataset_choice (str): Name of dataset."""),
	html.P("""user_id (str): Session/user id."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list(list(dict)): Key-value pairs to be input as                           `dcc.Dropdown` options."""),
	html.P(""""""),
	html.H3("""Notes on implementation:"""),
	html.P("""Currently only one type of KPI graph is supported, but more should be added later on. Additionally, work should be done         on building custom KPIs and maybe graphs."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""plot_graph_kpi(xvars, yvars, secondary_yvars,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Plot the graph according to user choices."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""xvars (str): `x-axis` of the graph."""),
	html.P("""yvars (str or list(str)): `y-axis`, can be multiple."""),
	html.P("""secondary_yvars: `bar-chart` variable."""),
	html.P("""user_id (str): Session/user id."""),
	html.P("""dataset_choice (str): Name of dataset."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""dict: A dictionary holding a plotly figure including layout."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/exploration/TextVisualizations"] = html.Div([
html.H2("""TextVisualizations.py"""), 
html.Br(), html.Div([
	html.P("""This module is about visualizing text data."""),
	html.P(""""""),
	html.H3("""Global Variables:"""),
	html.Li(""" Sidebar: To be used for creating side-menus."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" TextViz_Options: Generate the layout of the dashboard."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" plot_graph_text: Currently only word cloud visualizations are                        supported, from given text."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Contributions are encouraged here. Main functionality is still lacking in this part. You can use this module to add new buttons, input, or other interface-related, element, or maybe a new type of text visualizations (in which case implement it in a new file `graphs.textviz.py`). Like with other modules, working on exporting network graphs is encouraged. Finally, adding new visualization types is very welcome as well, but avoid loading huge word vectors files     at this stage of development."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""plot_graph_text(n_clicks, text, user_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Currently only word cloud visualizations are supported,"""),
	html.P("""from given text."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""n_clicks (int): Number of button clicks."""),
	html.P("""text (str): User-provided text used to create a word cloud."""),
	html.P("""user_id (str): Session/user id."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""str: the image encoded appropriately to be set as the 'src'              value of the `img` element"""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/exploration/Exploration3D"] = html.Div([
html.H2("""Exploration3D.py"""), 
html.Br(), html.Div([
	html.P("""This module defines the available graphs and creates the interface for the 3D dashboard."""),
	html.P(""""""),
	html.H3("""Global Variables:"""),
	html.Li(""" Sidebar: To be used for creating side-menus."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" Exploration3D_Options: Generate the layout of the dashboard."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" render_variable_choices_3d: Create a menu of dcc components for                                   the user to choose  plotting options."""),
	html.Li(""" plot_graph_3d: Plot the graph according to user choices."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""You should only write code here with caution, although contribution in this part are very encouraged. You can use this module to add new buttons, input, or other interface-related, element, or maybe a new type of graph (in which case implement it in `graphs.graphs3d.py`). Keep in mind that it may be moved later on to lower-level modules. Also, there is a chance that this will be moved entirely into another tab. Finally, exporting 3D graphs is currently not implemented, so     work on that is encouraged as well."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""render_variable_choices_3d(dataset_choice, user_id):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Create a menu of dcc components for the user to choose"""),
	html.P("""plotting options."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""dataset_choice (str): Name of dataset."""),
	html.P("""user_id (str): Session/user id."""),
	html.P(""""""),
	html.H3("""Notes on implementation:"""),
	html.P("""Currently only one type of 3D graph is supported, but more"""),
	html.P("""should be added later on."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""plot_graph_3d(xvars, yvars, zvars, user_id, dataset_choice_3d):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Plot the graph according to user choices."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""xvars (str): `x-axis` of the graph."""),
	html.P("""yvars (str): `y-axis`."""),
	html.P("""zvars (str): `z-axis`."""),
	html.P("""user_id (str): Session/user id."""),
	html.P("""dataset_choice_3d (str): Name of dataset."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""dict: A dictionary holding a plotly figure including layout."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/exploration/Exploration"] = html.Div([
html.H2("""Exploration.py"""), 
html.Br(), html.Div([
	html.P("""This module defines the available graphs and creates the interface for the 2D dashboard."""),
	html.P(""""""),
	html.H3("""Global Variables:"""),
	html.Li(""" Sidebar: To be used for creating side-menus."""),
	html.Li(""" Graphs_Export: Two buttons to export graphs (later used for                      PDF report generation)."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" Exploration_Options: Generate the layout of the dashboard."""),
	html.P(""""""),
	html.H3("""Dash callbacks:"""),
	html.Li(""" render_variable_choices_2d: Create a menu of dcc components for                                   the user to choose  plotting options."""),
	html.Li(""" plot_graph_2d: Plot the graph according to user choices."""),
	html.Li(""" toggle_modal: Notify when a graph is exported."""),
	html.Li(""" export_graph_callback: Export a graph (to a hidden div). One for                              every hidden graph."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""You should only write code here with caution. You can use this module to add new buttons, input, or other interface-related, element, or maybe a new type of graph (in which case implement     it in `graphs.graphs2d.py`)."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""render_variable_choices_2d(dataset_choice, graph_choice_exploration,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Create a menu of dcc components for the user to choose     plotting options."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""dataset_choice (str): Name of dataset."""),
	html.P("""graph_choice_exploration (str): The choice of graph type."""),
	html.P("""user_id (str): Session/user id."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""[list(dict), list(dict), bool]: Key-value pairs to be input as `dcc.Dropdown` options and a boolean to indicate whether                                         the graph needs a y-variable."""),
	html.P(""""""),
	html.H3("""Notes on implementation:"""),
	html.P("""These options should also take into account the datasets."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""plot_graph_2d(xvars, yvars, graph_choice_exploration,""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Plot the graph according to user choices."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""xvars (str): `x-axis` of the graph."""),
	html.P("""yvars (str or list(str)): `y-axis`, can be multiple depending                                   on graph type."""),
	html.P("""graph_choice_exploration (str): The choice of graph type."""),
	html.P("""user_id (str): Session/user id."""),
	html.P("""dataset_choice (str): Name of dataset."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""[dict, bool]: A dictionary holding a plotly figure including layout and a boolean to indicate whether a Y                       variable is needed."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""toggle_modal(close, *args):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Notify when a graph is exported."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""close (int): Number of times the close button was clicked."""),
	html.P("""*args (multiple): Timestamps for export button clicks, whether                           the modal is open, and the figure instance."""),
	html.P(""""""),
	html.H3("""Notes on implementation:"""),
	html.P("""Since the export buttons may increase in number we cannot avoid the *args parameter. Sadly, this *args has to contain other parts         too, since dash `State`s must always be at the end."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""[bool, str or html element]: Whether to open/close the modal                                      and the text (or html) displayed."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""export_graph_callback(n_clicks, figure):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Export a graph (to a hidden div). One for every hidden graph."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""n_clicks (int): Number of clicks for each respective button."""),
	html.P("""figure (dict): The figure parameters to be exported."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""dict: the figure is exported to the hidden div."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/exploration/graphs/__init__"] = html.Div([
html.H2("""__init__.py"""), 
html.Br(), html.Div([
	html.H3("""Developer notes:"""),
	html.P(""""""),
	html.H3("""Some suggestions on what could be done here:"""),
	html.Li(""" Define more PDF report layouts (see also `layouts.py`)."""),
	html.Li(""" Add more graph types in any of the categories (but avoid word       vector visualizations)."""),
	html.Li(""" Add additional functionality in KPIs."""),
	html.Li(""" Improve baseline graph and/or function."""),
	html.Li(""" Improve network visualizations."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/exploration/graphs/kpis"] = html.Div([
html.H2("""kpis.py"""), 
html.Br(), html.Div([
	html.P("""This module collects functions and utilities for KPI visualization but may also be used to add other options and core implementation logic."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" baseline_graph: Creates a baseline graph: a lineplot for the                         timeseries and its baseline, and a barchart."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Feel free to write code here either to improve current or to add new functionality. This part is in need of both customization and     presets."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""baseline_graph(df, xvars, yvars, secondary_yvars):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Creates a baseline graph: a lineplot for the timeseries and     its baseline, and a barchart."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""df (`pd.DataFrame`): The data."""),
	html.P("""xvars (str): Column of `df`; `x-axis`."""),
	html.P("""yvars (str or list(str)): Column(s) of `df`; lineplot(s)."""),
	html.P("""secondary_yvars (str):  Column of `df`; bar-chart."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: Plotly traces."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/exploration/graphs/graphs3d"] = html.Div([
html.H2("""graphs3d.py"""), 
html.Br(), html.Div([
	html.P("""This module collects functions and utilities for 3D visualization."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" scatterplot3d: Create a 3D scatterplot."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Feel free to write code here either to improve current or to add     new functionality. What is particularly needed is new graph types."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""scatterplot3d(x, y, z, **kwargs):""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Create a 3D scatterplot."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""x  (iterable): `x-axis` data."""),
	html.P("""y  (iterable): `y-axis` data."""),
	html.P("""z  (iterable): `z-axis` data."""),
	html.P("""**kwargs: Anything accepted by `plotly.graph_objs.Scatter3d`."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""list: Plotly traces."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/exploration/graphs/graphs2d"] = html.Div([
html.H2("""graphs2d.py"""), 
html.Br(), html.Div([
	html.P("""This module contains the implementations of graphing functions. I skipped adding docstrings for every function since most of them are one-liners anyway and should be pretty obvious."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" scatterplot: Create a 2D scatterplot."""),
	html.Li(""" line_chart: Create a lineplot."""),
	html.Li(""" histogram: Create a histogram."""),
	html.Li(""" heatmap: Create a heatmap of column correlations."""),
	html.Li(""" bubble_chart: Create a bubble chart."""),
	html.Li(""" filledarea: Create a lineplot with filled areas."""),
	html.Li(""" errorbar: Create a lineplot with error bars (currently fixed)."""),
	html.Li(""" density2d: Create a heatmap."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Feel free to write code here either to improve current or to add new functionality. Also feel free to add or tamper with styles     and/or helper functions."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])



layouts["../EDA_miner/apps/exploration/graphs/textviz"] = html.Div([
html.H2("""textviz.py"""), 
html.Br(), html.Div([
	html.P("""This module collects functions and utilities for text visualizations."""),
	html.P(""""""),
	html.H3("""Functions:"""),
	html.Li(""" create_wordcloud: Generate a wordcloud and save it to a file."""),
	html.P(""""""),
	html.H3("""Notes to others:"""),
	html.P("""Feel free to write code here either to improve current or to add new functionality. Avoid word vectors visualizations at this stage     of development as it will simply increase (re)load times for the app."""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

html.Br(), html.H3("""create_wordcloud(text, user_id, *, background_color="white",""", style={"backgroundColor": "#AAA", "display": "inline"}), 
html.Div([
	html.P("""Generate a wordcloud and save it to a file."""),
	html.P(""""""),
	html.H3("""Args:"""),
	html.P("""text (str): Raw text for the word cloud."""),
	html.P("""user_id (str): Session/user id. Needed to save the image."""),
	html.P("""background_color (str):  Color as accepted by wordcloud / matplotlib."""),
	html.P("""additional_stopwords (list(str)): Stopwords to remove along                                           with the predefined ones."""),
	html.P("""max_words (int): Max number of words to include in the wordcloud."""),
	html.P("""save (bool): Whether to save the figure. Currently unimportant."""),
	html.P("""ret (bool): Whether to return a value. Currently unimportant."""),
	html.P("""**kwargs: Anything that `wordcloud.WordCloud` accepts."""),
	html.P(""""""),
	html.H3("""Returns:"""),
	html.P("""None"""),
], style={"marginLeft": "20px", "backgroundColor": "#CCE"}),

])
