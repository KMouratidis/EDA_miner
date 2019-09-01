
# THIS IS AN AUTO-GENERATED FILE. IT IS NEITHER MEANT TO BE READ NOR
# TO BE WRITTEN / MODIFIED. REFER TO `doc_maker.py` FOR SPECIFICS.

import dash
import dash_core_components as dcc
import dash_html_components as html

layouts = {}




layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/initialize_project"] = html.Div([
html.H2("""initialize_project.py""", className="filename"), 
html.Div([
    html.P("""A dummy script to generate the database, a dummy user, and do any otherinitialization action needed to fire up the project """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/presentation_server"] = html.Div([
html.H2("""presentation_server.py""", className="filename"), 
html.Div([
    html.P("""Dummy script, supposed to run the standalone presentation app """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/models"] = html.Div([
html.H2("""models.py""", className="filename"), 
html.Div([
    html.P("""This module collects / defines the various models. It also initializes thelogin manager since if we were to put it into app_extensions it would causecircular dependencies (or we would have to take our User model code there) """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""User(db.Model, UserMixin): """, className="docstring-contents"), 
html.Div([
    html.P("""ORM class for the user """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""load_user(user_id): """, className="docstring-contents"), 
html.Div([
    html.P("""Callback to reload the user object (from the docs """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""unauthorized(): """, className="docstring-contents"), 
html.Div([
    html.P("""The user tries to access a view they are not authorized for. NUKE EM! """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""html or dash elements, essentially a 40 """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/exceptions"] = html.Div([
html.H2("""exceptions.py""", className="filename"), 
html.Div([
    html.P("""This module contains custom exceptions, simply to help with debugging andlogging. This is still experimental """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""UnexpectedResponse(Exception): """, className="docstring-contents"), 
html.Div([
    html.P("""Created primarily to inform about failed requests to (REST) APIs """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/model_server"] = html.Div([
html.H2("""model_server.py""", className="filename"), 
html.Div([
    html.P("""Dummy script, supposed to run the standalone modeling app """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/viz_server"] = html.Div([
html.H2("""viz_server.py""", className="filename"), 
html.Div([
    html.P("""Dummy script, supposed to run the standalone visualization app """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/env"] = html.Div([
], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/users_mgt"] = html.Div([
html.H2("""users_mgt.py""", className="filename"), 
html.Div([
    html.P("""This module is responsible for defining actions/helpers for user management """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""add_user(username, password, email): """, className="docstring-contents"), 
html.Div([
    html.P("""Create new user in the database """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""username (str): User name. Case-sensitive & unique """, className="funcParam"),
    html.P("""password (str): User password. Ensure strength during registration """, className="funcParam"),
    html.P("""email (str): A validated email address """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""Non """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""del_user(username): """, className="docstring-contents"), 
html.Div([
    html.P("""Delete a user from the database """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""username (str): User name. Does not handle logic """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""Non """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""show_users(): """, className="docstring-contents"), 
html.Div([
    html.P("""Prints the list of available users """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""Non """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""update_password(user_id, password): """, className="docstring-contents"), 
html.Div([
    html.P("""Update the password for the specified user """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""user_id (int): The user id, as in the database """, className="funcParam"),
    html.P("""password (str): The HASHED password """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""Non """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/docs_server"] = html.Div([
html.H2("""docs_server.py""", className="filename"), 
html.Div([
    html.P("""Dummy script, supposed to run the standalone docs app """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/tasks_server"] = html.Div([
], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/env_template"] = html.Div([
], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/app_extensions"] = html.Div([
html.H2("""app_extensions.py""", className="filename"), 
html.Div([
    html.P("""Use this module to collect all the extensions used. These can be defined inother modules, but do import them here and then from here to `wsgi.py` """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/utils"] = html.Div([
html.H2("""utils.py""", className="filename"), 
html.Div([
    html.P("""This module provides utilities, functions, and other code that ismeant to be used across the app. This may undergo changes soon """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""cleanup: Clean up after the Dash app exits. """, className="funcParam"),
    html.P("""create_dropdown: Create a dropdown with a title. """, className="funcParam"),
    html.P("""create_table: Creates a `dash_table.DataTable` given a `pd.DataFrame`. """, className="funcParam"),
    html.P("""create_trace_dropdown: Create a menu item for traces. """, className="funcParam"),
    html.P("""- convert_schema_to_frictionless: Convert the schema from our internal                                      format to the frictionless-data format """, className="funcParam"),
    html.P("""- get_dataset_options: Get datasets available to user as options for                           `dcc.Dropdown` """, className="funcParam"),
    html.P("""get_data_schema: Get a dict with the specified dataset's schema. """, className="funcParam"),
    html.P("""hard_cast_to_float: Convert to float or return 0. """, className="funcParam"),
    html.P("""- interactive_menu: Create the necessary elements for the sidemenus                        to become interactive """, className="funcParam"),
    html.P("""save_schema: Save the schema including a preview for the data. """, className="funcParam"),
    html.P("""parse_contents: Decode uploaded files and store them in Redis. """, className="funcParam"),
    html.P("""redis_startup: Connect to a Redis server & handle startup. """, className="funcParam"),
    html.P("""Global variables: """, className="section"),
    html.P("""redis_conn: A Redis connection that is used throughout the app. """, className="funcParam"),
    html.P("""- mapping: A dict that maps tags to sklearn models meant for               creating dropdowns and used in `apps.analyze` modules """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""You should probably not write code here, unless you are addingfunctions aimed at being used by many lower-level modules.Some of the functions here will later be moved to lower-level    modules (e.g. `pretty_print_tweets`) """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""cleanup(redis_conn): """, className="docstring-contents"), 
html.Div([
    html.P("""Clean up after the Dash app exits """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""redis_conn: `redis.Redis` object """, className="funcParam"),
    html.P("""Further details: """, className="section"),
    html.P("""Flush every key stored in the Redis database. If thereare users that have logged in and uploaded data, store        those on disk """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""create_dropdown(name, options, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a dropdown with a title """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""name (str): the title above the dropdown """, className="funcParam"),
    html.P("""options (list(dict)): dictionaries should contain keys at least                             the keys (label, value) """, className="funcParam"),
    html.P("""**kwargs: keyword-value pairs. Accepts any keyword-arguments                  that can be passed to `dcc.Dropdown` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list: an H5 and the Dropdown """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""create_trace_dropdown(name, options, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a menu item for traces. Same as above, but different style """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""name (str): the title above the dropdown """, className="funcParam"),
    html.P("""options (list(dict)): dictionaries should contain keys at least                             the keys (label, value) """, className="funcParam"),
    html.P("""**kwargs: keyword-value pairs. Accepts any keyword-arguments                  that can be passed to `dcc.Dropdown` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list: an H5 and the Dropdown """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""create_table(df, table_id="table", columns=None): """, className="docstring-contents"), 
html.Div([
    html.P("""Creates a `dash_table.DataTable` given a `pandas.DataFrame` """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""df (`pandas.DataFrame`): the data """, className="funcParam"),
    html.P("""table_id (str, optional): id of the table element for usage                                  with dash callbacks """, className="funcParam"),
    html.P("""columns (list(dict)): the column data passed to the data table """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A `dash_table.DataTable` with pagination """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""convert_schema_to_frictionless(schema): """, className="docstring-contents"), 
html.Div([
    html.P("""Convert the schema from our internal format to the frictionless-data    format. See: https://frictionlessdata.io/specs/table-schema """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""get_dataset_options(redis_conn): """, className="docstring-contents"), 
html.Div([
    html.P("""Get datasets available to user as options for `dcc.Dropdown` """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""redis_conn (`redis.Redis`): Connection to a Redis database """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list(dict): A list of options to be used for making                    dropdowns for variables """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""get_data_schema(dataset_key, redis_conn): """, className="docstring-contents"), 
html.Div([
    html.P("""Get a dict with the specified dataset's schema. The schema containsthree keys: types (int, float, ...), subtypes (binary, email, ...),    and head (5 rows from the `pd.DataFrame` sample) """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""dataset_key (str): the key used by the Redis server                           to store the data """, className="funcParam"),
    html.P("""redis_conn (`redis.Redis`): Connection to a Redis database """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""dict: The dataset schem """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""get_variable_options(dataset_key, redis_conn): """, className="docstring-contents"), 
html.Div([
    html.P("""Get available variables / columns as options for `dcc.Dropdown` """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""dataset_key (str): the key used by the Redis server                           to store the data """, className="funcParam"),
    html.P("""redis_conn (`redis.Redis`): Connection to a Redis database """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list(dict): A list of options to be used for making                    dropdowns for variables """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""hard_cast_to_float(x): """, className="docstring-contents"), 
html.Div([
    html.P("""Convert to float or return 0 """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""x (anything): will be type-casted or 0'ed """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""float """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""interactive_menu(output_elem_id): """, className="docstring-contents"), 
html.Div([
    html.P("""Create the necessary elements for the sidemenus to become interactive """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""output_elem_id (str): The id for the div with the contents                          of the sidemenu """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list: Dash elements, the sidebar, its buttons, and the              JS script to be run """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""interactive_menu(output_elem_id): """, className="docstring-contents"), 
html.Div([
    html.P("""// show the button for opening the submen """, className="funcParam"),
    html.P("""var elem = document.getElementById("open_menu2") """, className="funcParam"),
    html.P("""elem.style.display = "inline-block" """, className="funcParam"),
    html.P("""// and bind the appropriate function to i """, className="funcParam"),
    html.P("""elem.onclick = function(){openNav2()} """, className="funcParam"),
    html.P("""// do the same for the close butto """, className="funcParam"),
    html.P("""var elem2 = document.getElementById("closebtn2") """, className="funcParam"),
    html.P("""elem2.onclick = function(){closeNav2()} """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""save_schema(key, types, subtypes, head, redis_conn, user_id, """, className="docstring-contents"), 
html.Div([
    html.P("""Save the schema including a preview for the data """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""key (str): The Redis key where to save the data """, className="funcParam"),
    html.P("""types (dict): Mapping of columns to data types """, className="funcParam"),
    html.P("""subtypes (dict): Mapping of columns to secondary data types """, className="funcParam"),
    html.P("""head (`pd.DataFrame`): The first 5 rows of the data """, className="funcParam"),
    html.P("""redis_conn (`redis.Redis`): The connection to the desired database """, className="funcParam"),
    html.P("""user_id (str): The user for whom to fetch data """, className="funcParam"),
    html.P("""schema_status (str): Whether the schema was inferred or ifthe user explicitly changed it. Can be                             "ground_truth" or "inferred" """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""bool: Whether Redis successfully stored the key """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""parse_contents(contents, filename, date, user_id, redis_conn): """, className="docstring-contents"), 
html.Div([
    html.P("""Decode uploaded files and store them in Redis """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""contents (str): The content of the file to be decoded """, className="funcParam"),
    html.P("""filename (str): Name of uploaded file """, className="funcParam"),
    html.P("""date (str): (modification?) date of the file """, className="funcParam"),
    html.P("""user_id (str): The user for whom to fetch data """, className="funcParam"),
    html.P("""redis_conn (`redis.Redis`): The connection to the desired database """, className="funcParam"),
    html.P("""Further details: """, className="section"),
    html.P("""After decoding the uploaded file, handle any remainingoperations here. This was stolen from the dash docs. Currently        it only supports csv, xls(x), json, and feather file types """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""redis_startup(): """, className="docstring-contents"), 
html.Div([
    html.P("""Connect to a Redis server & handle startup """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`redis.Redis`: a connection to a Redis server """, className="funcParam"),
    html.P("""Further details: """, className="section"),
    html.P("""Connects to a Redis server on its default port (6379) and isalso responsible for any other startup operations needed such        as reading the data from the previous use """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/forms"] = html.Div([
html.H2("""forms.py""", className="filename"), 
html.Div([
    html.P("""This module collects the forms of the site that need at least some degreeof serious implementation (e.g. for security concerns), like the logins.Even if you can, don't try to create forms for Dash forms; unless you arealso willing to teach us : """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""LoginForm(FlaskForm): """, className="docstring-contents"), 
html.Div([
    html.P("""Login form for the main flask app """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""RegisterForm(FlaskForm): """, className="docstring-contents"), 
html.Div([
    html.P("""Register form for the main flask app. Currently not used. May only be    used for creating an admin panel """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""ResetPassword(FlaskForm): """, className="docstring-contents"), 
html.Div([
    html.P("""Reset password after receiving a randomized URL """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""ChangePassword(ResetPassword): """, className="docstring-contents"), 
html.Div([
    html.P("""Change password form for the main flask app """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""ForgotPassword(FlaskForm): """, className="docstring-contents"), 
html.Div([
    html.P("""Request the reset of password form for the main flask app """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/layouts"] = html.Div([
html.H2("""layouts.py""", className="filename"), 
html.Div([
    html.P("""Similar to `styles.py`, this module is mean as a collection of layoutsto be used across the dash app. A layout is about what components existin any view (e.g. html elements) whereas a style is about... styling!Styles are implemented as functions to allow use with different parameters """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""default_2d: Layout for most plotly graphs. """, className="funcParam"),
    html.P("""default_3d: Layout for 3D graphs, not implemented. """, className="funcParam"),
    html.P("""default_kpi: Layout for KPI graphs, not implemented. """, className="funcParam"),
    html.P("""Classes: """, className="section"),
    html.P("""- PDF_Layout1: A sample PDF layout, more to be added. Implementedas a class out of convenience, may be changed later.                   Usage: `PDF_Layout1.render(x_axis, y_axis)` """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""Feel free to tamper with all of the functions and classes belowand/or add your own. Beware that in some cases (e.g. defining anew PDF layout) you might need to make changes in other files,    or at least wait till needed functionality is added """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""default_2d(xvars, yvars): """, className="docstring-contents"), 
html.Div([
    html.P("""Default `go.Layout` for 2D graphs """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""xvars: str, title of the x-axis """, className="funcParam"),
    html.P("""yvars: str, title of the y-axis """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A `go.Layout` instance """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""default_3d(xvars, yvars, zvars): """, className="docstring-contents"), 
html.Div([
    html.P("""Default `go.Layout` for 3D graphs. Currently same as default_2d """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""xvars: str, title of the x-axis """, className="funcParam"),
    html.P("""yvars: str, title of the y-axis """, className="funcParam"),
    html.P("""zvars: str, currently not used """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A `go.Layout` instance """, className="funcParam"),
    html.P("""Todo: """, className="section"),
    html.P("""This needs a better implementatio """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/__init__"] = html.Div([
html.H2("""EDA_miner""", className="filename"), 
html.Div([
    html.P("""Welcome to EDA Miner """, className="funcParam"),
    html.P("""Usage walk-through: """, className="section"),
    html.P("""We strive to create a simple and intuitive interface. The app is meant tobe run in a central server and accessed via web, but can of course be runlocally, too """, className="funcParam"),
    html.P("""Upon visiting the page you will be directed to the homepage. You can log-into access the various apps available to you, such as apps for data handling,where you upload your own datasets, connect to APIs, view the data you have,or update the inferred data schema, When viewing your data, each API displaysdata in different ways, although actually using those data is not yetimplemented (May 2019) """, className="funcParam"),
    html.P("""As soon as you have uploaded a dataset (or you want to work on example data),a good second stop would be the "Visualization" app. Here you will findoptions to plot your data; each sub-tab contains a different class ofvisualizations """, className="funcParam"),
    html.P("""- Exploratory analysis: contains all the 2D graphs, including                            matplotlib-generated pairplots """, className="funcParam"),
    html.P("""- Key performance indicators: currently implements only a baselinegraph, but we plan to implementfunctionality so you can create yourown KPIs, and we want to add additional                                  analysis tools """, className="funcParam"),
    html.P("""3D graphs: currently only plots 3D scatterplots. """, className="funcParam"),
    html.P("""- Network graphs: use Cytoscape.js to create graph/network                      visualizations, allowing various layout choices """, className="funcParam"),
    html.P("""- Text visualizations: currently only allow for creating simple wordclouds (from given text), but plans for furtherintegration and more visualizations include                           word vector visualization """, className="funcParam"),
    html.P("""- PDF report: allows you to create reports using the figures youplot in the other tabs (using the "export graph                  config" buttons) and add custom text, headers, titles """, className="funcParam"),
    html.P("""The third main app is the "Modeling" app, where you are able to use yourdata to train Machine Learning models. The Model builder can beused to create more advanced pipelines (including defining your ownfeatures). The default steps are to first define the model fully(or some features may not work), then go over every node you want tocustomize and change its node options, and when you're done export themodel ("convert to model" button). Finally, head over to the "Pipelinestrainer" tab, select and train your model. If you want to run simplermodels, the "Single Model" tab has you covered with the most common typesof machine learning problems """, className="funcParam"),
    html.P("""Project structure: """, className="section"),
    html.P("""Contributors wanting to familiarize themselves with the projectstructure can take a look at the contributor guidelines(https://github.com/KMouratidis/EDA_miner_public/blob/master/CONTRIBUTING.md).You can also go through all the files and read the module docstringsthat have rough guidelines about contributions. In the Python    spirit, feel free to completely ignore them """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/wsgi"] = html.Div([
html.H2("""wsgi.py""", className="filename"), 
html.Div([
    html.P("""This is the main application from which to run EDA Miner. Use a commandlike `gunicorn wsgi:application`. It is also here where you can add new apps """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""* To add a new app follow the instructions below (steps 0 - 4). If theapp doesn't need login then skip steps 2.1 - 2.3. Also skip the 0th step    if it is not a Dash app """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/data_server"] = html.Div([
html.H2("""data_server.py""", className="filename"), 
html.Div([
    html.P("""Dummy script, supposed to run the standalone data app """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/google_analytics/app"] = html.Div([
html.H2("""app.py""", className="filename"), 
html.Div([
    html.P("""TBW.. """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""ganalytics_connect(client_email, private_key): """, className="docstring-contents"), 
html.Div([
    html.P("""Connect to a Google Analytics account. Doesn't seem to be    memoizable. Google throws `googleapiclient.errors.HttpError: 401` """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/presentation/app"] = html.Div([
], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/presentation/__init__"] = html.Div([
], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/dash_rnd/_imports_"] = html.Div([
], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/dash_rnd/ResizeDraggable"] = html.Div([
html.Br(), html.H3("""ResizeDraggable(Component): """, className="docstring-contents"), 
html.Div([
    html.P("""ExampleComponent is an example component """, className="funcParam"),
    html.P("""It takes a property, `label`, an """, className="funcParam"),
    html.P("""displays it """, className="funcParam"),
    html.P("""It renders an input with the property `value """, className="funcParam"),
    html.P("""which is editable by the user """, className="funcParam"),
    html.P("""Keyword arguments: """, className="section"),
    html.P("""children (dash component; optional) """, className="funcParam"),
    html.P("""id (string; optional): The ID used to identify this component in Dash callbacks """, className="funcParam"),
    html.P("""label (string; required): A label that will be printed when this component is rendered. """, className="funcParam"),
    html.P("""value (string; optional): The value displayed in the input """, className="funcParam"),
    html.P("""minWidth (number; optional) """, className="funcParam"),
    html.P("""minHeight (number; optional) """, className="funcParam"),
    html.P("""x (number; optional) """, className="funcParam"),
    html.P("""y (number; optional) """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/dash_rnd/__init__"] = html.Div([
], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/tasks/server"] = html.Div([
], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/tasks/app"] = html.Div([
html.Br(), html.H3("""parse_uploads(content, name, date): """, className="docstring-contents"), 
html.Div([
    html.P("""Load and store the uploaded data """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""list_of_contents (list(bytes)): The file contents that need to                                        be parsed """, className="funcParam"),
    html.P("""list_of_names (list(str)): The original filenames """, className="funcParam"),
    html.P("""list_of_dates (list(str)): The modification (?) dates of files """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list: A list of dash components """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/tasks/__init__"] = html.Div([
], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/data/view"] = html.Div([
html.H2("""view.py""", className="filename"), 
html.Div([
    html.P("""This module provides views for the data (tables, lists of tweets, etc) """, className="funcParam"),
    html.P("""Global Variables: """, className="section"),
    html.P("""View_Options: Generate the layout for inspecting available datasets. """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""get_available_choices: Get datasets available to user. """, className="funcParam"),
    html.P("""Dash callbacks: """, className="section"),
    html.P("""display_subdataset_choices: Show/hide input field for Quandl API. """, className="funcParam"),
    html.P("""render_table: Create a display for the chosen dataset. """, className="funcParam"),
    html.P("""- display_reddit_posts: For the Reddit API, allow the user to                            specify a subreddit to get data from """, className="funcParam"),
    html.P("""Note to others: """, className="section"),
    html.P("""You should probably not write code here, UNLESS you defined a    new connection to an API, or are doing refactoring """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""View_Options(): """, className="docstring-contents"), 
html.Div([
    html.P("""Generate the layout for inspecting available datasets """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""render_table(dataset_key): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a display for the chosen dataset """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""dataset_key (str): Value from the dropdown. It is the Redis                           key for the dataset """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list: A list of dash components """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/data/server"] = html.Div([
html.H2("""server.py""", className="filename"), 
html.Div([
    html.P("""This module is only here because of the Dash app spanning multiple files.General configurations of the underlying app and server go here as well """, className="funcParam"),
    html.P("""Global Variables: """, className="section"),
    html.P("""- app: The Dash server, imported everywhere that a dash callback           needs to be defined """, className="funcParam"),
    html.P("""r: The connection to Redis. """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/data/upload"] = html.Div([
html.H2("""upload.py""", className="filename"), 
html.Div([
    html.P("""This module provides an interface for uploading and handling of files """, className="funcParam"),
    html.P("""Global Variables: """, className="section"),
    html.P("""Upload_Options: Generate the layout for uploading datasets. """, className="funcParam"),
    html.P("""Dash callbacks: """, className="section"),
    html.P("""parse_uploads: Load and store the uploaded data. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""You should probably not write code here, unless you mean toimplement new filetype uploads or other types of upload handling,    or other similar functionality """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""parse_uploads(list_of_contents, list_of_names, """, className="docstring-contents"), 
html.Div([
    html.P("""Load and store the uploaded data """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""list_of_contents (list(bytes)): The file contents that need to                                        be parsed """, className="funcParam"),
    html.P("""list_of_names (list(str)): The original filenames """, className="funcParam"),
    html.P("""list_of_dates (list(str)): The modification (?) dates of files """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list: A list of dash components """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/data/app"] = html.Div([
html.Br(), html.H3("""tab_subpages(tab): """, className="docstring-contents"), 
html.Div([
    html.P("""Given the low-level tab choice, render the appropriate view and    side-navbar """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""tab (str): The tab the user is currently on """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A list of lists of HTML-dash components, usually within a div """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/data/apis"] = html.Div([
html.H2("""apis.py""", className="filename"), 
html.Div([
    html.P("""This module defines the interface for connecting to APIs.It renders the appropriate layout according to the tab chosen """, className="funcParam"),
    html.P("""Global Variables: """, className="section"),
    html.P("""- API_Options: Generate the layout for connecting to APIs.This is automatically generated for the APIs                   defined in `api_connectors.connectors_mapping` """, className="funcParam"),
    html.P("""Dash callbacks: """, className="section"),
    html.P("""render_api_login_form: Render the appropriate login form. """, className="funcParam"),
    html.P("""- parse_credentials (multiple): Create callbacks for every APIlogin form, based on their                                    connectors' function arguments """, className="funcParam"),
    html.P("""- get_data_from_api (multiple): Create callbacks for every API                                    fetch_data function """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""You probably do not want to write ANY code here. If you want todefine a new API connection do it in `api_layouts` conforming tothe abstract base class interface and it will be automatically    added here """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""render_api_login_form(api_choice): """, className="docstring-contents"), 
html.Div([
    html.P("""Render the appropriate login form. It takes the choice of API andsearches the mappings for the layout. A different layout is returned    accoring to login status """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""api_choice (str): One of the supported APIs """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""parse_credentials(n_clicks, api_choice, *func_params): """, className="docstring-contents"), 
html.Div([
    html.P("""Create callbacks for every API login form, based on theirconnectors' function arguments. This reads the various connectfunctions and gets their arguments. **Note that the first argument        is `self` so we need the rest of the arguments """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""n_clicks (int): Number of button clicks """, className="funcParam"),
    html.P("""api_choice (str): One of the supported APIs """, className="funcParam"),
    html.P("""*func_params (list): Depending on the selected api and itsconnector function, the list of arguments                                 it needs to receive, in order """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""get_data_from_api(n_clicks, api_choice, *func_params): """, className="docstring-contents"), 
html.Div([
    html.P("""Create callbacks for every API success form, based on theirconnectors' function arguments. This reads the various fetch_datafunctions and gets their arguments. **Note that the first argument        is `self` so we need the rest of the arguments """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""n_clicks (int): Number of button clicks """, className="funcParam"),
    html.P("""api_choice (str): One of the supported APIs """, className="funcParam"),
    html.P("""*func_params (list): Depending on the selected api and itsfetch_data function, the list of                                 arguments it needs to receive, in order """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/data/__init__"] = html.Div([
html.H2("""data""", className="filename"), 
html.Div([
    html.P("""Developer notes: """, className="section"),
    html.P("""Some suggestions on what could be done: """, className="section"),
    html.P("""Implementing the editing and filtering of datasets. """, className="funcParam"),
    html.P("""A "download" button for datasets that were modified. """, className="funcParam"),
    html.P("""More API connections. """, className="funcParam"),
    html.P("""Prettier interfaces. """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/data/schemata"] = html.Div([
html.Br(), html.H3("""Schema_Options(): """, className="docstring-contents"), 
html.Div([
    html.P("""Generate the layout of the dashboard """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A list of Dash elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""schema_table(df, types, subtypes): """, className="docstring-contents"), 
html.Div([
    html.P("""Helper to create the table. Dash's DataTable doesn't allow fordropdowns to only some rows so we create our own where the firstrow is the head, the second rows are like head but have dropdowns    for picking type """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""df (`pd.DataFrame`): The dataset """, className="funcParam"),
    html.P("""types (dict): The types from the data schema """, className="funcParam"),
    html.P("""subtypes (dict): The subtypes from the data schema """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element containing the table """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""show_schema(dataset_choice): """, className="docstring-contents"), 
html.Div([
    html.P("""Show the schema for the dataset and allow the user to modify it """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""dataset_choice (str): Name of dataset """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list: A list of dash components. The custom table """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""update_schema(n_clicks, table_colnames, row_types, row_subtypes, """, className="docstring-contents"), 
html.Div([
    html.P("""Update the dataset schema. This function takes the html elementsfrom the table head (containing column names) and its first tworows (containing dropdowns with the data types/subtypes), parses    them and stores them in redis """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""n_clicks (int): Number of button clicks """, className="funcParam"),
    html.P("""table_colnames (dict): The head (`html.Thead`) of the table,                               as a Dash dict """, className="funcParam"),
    html.P("""row_types (dict): The first table row (`html.Tr`) containing                          the Dash dropdown dict with the data types """, className="funcParam"),
    html.P("""row_subtypes (dict): The first table row (`html.Tr`) containing                             the Dash dropdown dict with the data subtypes """, className="funcParam"),
    html.P("""dataset_choice (str): Name of dataset """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list(str, bool): A message and a boolean for a browser alert """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/data/data_utils/api_layouts"] = html.Div([
html.H2("""api_layouts.py""", className="filename"), 
html.Div([
    html.P("""This module collects the layouts for connecting to the various APIs """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""success_message: Notify the user for successful connection. """, className="funcParam"),
    html.P("""Global variables: """, className="section"),
    html.P("""twitter_layout: 4 input fields and a button. """, className="funcParam"),
    html.P("""gsheets_layout: 2 input fields and a button. """, className="funcParam"),
    html.P("""reddit_layout: 2 input fields and a button. """, className="funcParam"),
    html.P("""quandl_layout: 2 input fields and a button. """, className="funcParam"),
    html.P("""spotify_layout: 2 input fields and a button. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""You should probably not write code here, unless adding    a new API connection """, className="funcParam"),
    html.P("""IMPORTANT: When designing layouts ALWAYS pre-append the inputelements with the API name, and ALWAYS name each input idaccording to the names of the variables of the respective API    connector """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""success_message(api): """, className="docstring-contents"), 
html.Div([
    html.P("""Utility to provide feedback on successful connections """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""api (str): Name / key of the API """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list: A list of Dash elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""save_data_and_schema(self, df, key, take_sample=True, ex=None): """, className="docstring-contents"), 
html.Div([
    html.P("""Helper to infer schema and save the it along with the data """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""df (`pd.DataFrame`): The data to save """, className="funcParam"),
    html.P("""key (str): The name of the dataset (subreddit, twitter account                       quandl tag, etc) """, className="funcParam"),
    html.P("""take_sample (bool): Whether to sample the data or not """, className="funcParam"),
    html.P("""ex (int): In how many seconds to expire the data (given to Redis) """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""Non """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""connect(self, *args, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Connect, save the API object, and change state """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""fetch_data(self, *args, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Get data and return a previe """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""login_layout(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a Dash layout for accepting credentials for login """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""success_layout(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a Dash layout after a successful login, and a menu        to fetch data """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""pretty_print(df): """, className="docstring-contents"), 
html.Div([
    html.P("""Display the sample in a appealing manner, given a DataFrame.This is only displayed prettily here, the `view` module only        shows tables """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""connect(self, consumer_key, consumer_secret, access_token_key, """, className="docstring-contents"), 
html.Div([
    html.P("""Connect to Twitter API """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""fetch_data(self, acc_name): """, className="docstring-contents"), 
html.Div([
    html.P("""Get tweets by the specified user """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""acc_name (str): The account name / handle from Twitter """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`pd.DataFrame`: A sample of the fetched data """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""login_layout(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a Dash layout for accepting credentials for login """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""success_layout(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a Dash layout after a successful login, and a menu        to fetch data """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""pretty_print(df): """, className="docstring-contents"), 
html.Div([
    html.P("""Display the sample in a appealing manner, given a DataFrame.This is only displayed prettily here, the `view` module only        shows tables """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""connect(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Connect to Google Sheets API """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""fetch_data(self, gspread_key): """, className="docstring-contents"), 
html.Div([
    html.P("""Connect to a certain spreadsheet, and get all its sheets usingit's key e.g. full address:https://docs.google.com/spreadsheets/d/1802UymlFPQE2uvk_T8XI3kX1kWniYOngS6sQSnXoe2U/        You might need to change file permissions """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""gspread_key (str): The ID of the spreadhseet to fetch """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`pd.DataFrame`: A sample of the fetched data """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""login_layout(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a Dash layout for accepting credentials for login """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""success_layout(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a Dash layout after a successful login, and a menu        to fetch data """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""pretty_print(df): """, className="docstring-contents"), 
html.Div([
    html.P("""Display the sample in a appealing manner, given a DataFrame.This is only displayed prettily here, the `view` module only        shows tables """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""connect(self, client_id, client_secret): """, className="docstring-contents"), 
html.Div([
    html.P("""Connect to Reddit API """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""fetch_data(self, subreddit_choice, limit): """, className="docstring-contents"), 
html.Div([
    html.P("""Fetch the `limit` latest posts from the specified subreddit """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""subreddit_choice (str): The name of the subreddit to fetch """, className="funcParam"),
    html.P("""limit (int): How many topics to fetch """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`pd.DataFrame`: A sample of the fetched data """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""login_layout(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a Dash layout for accepting credentials for login """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""success_layout(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a Dash layout after a successful login, and a menu        to fetch data """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""pretty_print(df): """, className="docstring-contents"), 
html.Div([
    html.P("""Display the sample in a appealing manner, given a DataFrame.This is only displayed prettily here, the `view` module only        shows tables """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""connect(self, client_email, private_key): """, className="docstring-contents"), 
html.Div([
    html.P("""Connect to a Google Analytics account """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""fetch_data(self, metrics): """, className="docstring-contents"), 
html.Div([
    html.P("""Fetch Google Analytics (realtime) data for the selected metrics """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""metrics (list(str)): The metrics to fetch, e.g.: pageviews """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`pd.DataFrame`: A sample of the fetched data """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""login_layout(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a Dash layout for accepting credentials for login """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""success_layout(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a Dash layout after a successful login, and a menu        to fetch data """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""pretty_print(df): """, className="docstring-contents"), 
html.Div([
    html.P("""Display the sample in a appealing manner, given a DataFrame.This is only displayed prettily here, the `view` module only        shows tables """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""connect(self, client_id, client_secret): """, className="docstring-contents"), 
html.Div([
    html.P("""Connect to Spotify API """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""fetch_data(self, category="toplists"): """, className="docstring-contents"), 
html.Div([
    html.P("""Fetch information about Spotify playlists in a given category """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""category (str): The category in Spotify for playlists, e.g.:                            "toplists" """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`pd.DataFrame`: A sample of the fetched data """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""login_layout(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a Dash layout for accepting credentials for login """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""success_layout(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a Dash layout after a successful login, and a menu        to fetch data """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""pretty_print(df): """, className="docstring-contents"), 
html.Div([
    html.P("""Display the sample in a appealing manner, given a DataFrame.This is only displayed prettily here, the `view` module only        shows tables """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""connect(self, api_key): """, className="docstring-contents"), 
html.Div([
    html.P("""Connect to Quandl API """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""fetch_data(self, dataset_tag): """, className="docstring-contents"), 
html.Div([
    html.P("""Fetch a dataset from Quandl """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""dataset_tag (str): The dataset tag in Quandl, e.g. "NSE/OIL" """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`pd.DataFrame`: A sample of the fetched data """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""login_layout(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a Dash layout for accepting credentials for login """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""success_layout(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a Dash layout after a successful login, and a menu        to fetch data """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""pretty_print(df): """, className="docstring-contents"), 
html.Div([
    html.P("""Display the sample in a appealing manner, given a DataFrame.This is only displayed prettily here, the `view` module only        shows tables """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/data/data_utils/schema_heuristics"] = html.Div([
html.Br(), html.H3("""can_into_date(col): """, className="docstring-contents"), 
html.Div([
    html.P("""# Can handle with various separators# e.g.: "-" or "/" or " "    # (time MUST be separated with ":" """, className="funcParam"),
    html.P("""YYY """, className="funcParam"),
    html.P("""YYYY-M """, className="funcParam"),
    html.P("""MM-YYY """, className="funcParam"),
    html.P("""YYYY-MM-D """, className="funcParam"),
    html.P("""MM-DD-YYY """, className="funcParam"),
    html.P("""DD-MM-YYY """, className="funcParam"),
    html.P("""DD-MM-YYYY-HRS:MI """, className="funcParam"),
    html.P("""June 199 """, className="funcParam"),
    html.P("""03 June 199 """, className="funcParam"),
    html.P("""03 Jun 199 """, className="funcParam"),
    html.P("""03 June 1995 15:3 """, className="funcParam"),
    html.P("""15:32 16 Jun 201 """, className="funcParam"),
    html.P("""15:32 16th Jun 201 """, className="funcParam"),
    html.P("""15:32 Jun 16th 201 """, className="funcParam"),
    html.P("""# Partially handle """, className="funcParam"),
    html.P("""15:32  # assumed: Toda """, className="funcParam"),
    html.P("""# Cannot handl """, className="funcParam"),
    html.P("""YYYY-DD-M """, className="funcParam"),
    html.P("""# Incorrectly handle """, className="funcParam"),
    html.P("""in """, className="funcParam"),
    html.P("""floa """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""can_into_categorical(col, threshold=None): """, className="docstring-contents"), 
html.Div([
    html.P("""Convert to categorical IF the unique values are smaller than    some threshold """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""can_into_int(col): """, className="docstring-contents"), 
html.Div([
    html.P("""Attempt to convert to int """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""column_name_match(col_name, list_of_words, match_threshold=55): """, className="docstring-contents"), 
html.Div([
    html.P("""Helper for matching column names to a list of words """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""infer_types(df, is_sample=False): """, className="docstring-contents"), 
html.Div([
    html.P("""Guess data types """, className="funcParam"),
    html.P("""float > int > datetime > categorical > strin """, className="funcParam"),
    html.P("""1. "Unsafe" assumption. Try to infer datatypes by using directly       "tests" / "transformations" """, className="funcParam"),
    html.P("""2. "Lenient" assumption. Pass once over column headers and try toguess the column. Apply the "test" / "transformation" to see if       it works. Overwrite if necessary """, className="funcParam"),
    html.P("""3. Try to guess subtypes """, className="funcParam"),
    html.P("""4. Anything the user explicitly corrects """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""df (`pd.DataFrame`): Dataframe on which to run data type inference """, className="funcParam"),
    html.P("""is_sample (`bool`): If True then df will be treated as being a sample """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list(dict): Types and subtypes. Each dictionary has the column                    names as keys and the types as values """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/data/data_utils/__init__"] = html.Div([
html.H2("""data_utils""", className="filename"), 
html.Div([
    html.P("""Developer notes: """, className="section"),
    html.P("""The modules here are for implementing utilities needed by higher-leve """, className="funcParam"),
    html.P("""modules. Some suggestions on what could be done: """, className="section"),
    html.P("""Add new API connections (note: you need to implement both """, className="funcParam"),
    html.P("""the connector and define a layout/form) """, className="funcParam"),
    html.P("""Fix the bug that made me pollute the whole file with those """, className="funcParam"),
    html.P("""ugly debugger layouts """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/data/data_utils/api_connectors"] = html.Div([
html.H2("""api_connectors.py""", className="filename"), 
html.Div([
    html.P("""This module collects the layouts for connecting to the various APIs """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""twitter_connect: Connect to the Twitter API. """, className="funcParam"),
    html.P("""google_sheets_connect: Connect to the Google Sheets API. """, className="funcParam"),
    html.P("""reddit_connect: Connect to the Reddit API. """, className="funcParam"),
    html.P("""spotify_connect: Connect to the Spotify API. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""You should probably not write code here, unless adding    a new API connection (or improving existing ones) """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""api_connect(api_choice, *args, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Connect to the selected API. A function that serves as the frontend to all others, abstracting them away. ALso stores the API    handle in Redis for later usage """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""api_choice (str): A key in `connectors_mapping` """, className="funcParam"),
    html.P("""*args: Arguments to be passed to the appropriate API connector """, className="funcParam"),
    html.P("""**kwargs: Keyword arguments to be passed to the appropriate                  API connector """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""bool: Whether everything succeeded or not (an exception was raised) """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/data/data_utils/ganalytics_metrics"] = html.Div([
], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/visualization/server"] = html.Div([
html.H2("""server.py""", className="filename"), 
html.Div([
    html.P("""This module is only here because of the Dash app spanning multiple files.General configurations of the underlying app and server go here as well """, className="funcParam"),
    html.P("""Global Variables: """, className="section"),
    html.P("""- app: The Dash server, imported everywhere that a dash callback           needs to be defined """, className="funcParam"),
    html.P("""redis_conn: The connection to Redis. """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/visualization/kpis"] = html.Div([
html.H2("""kpis.py""", className="filename"), 
html.Div([
    html.P("""This module is about building and viewing KPIs. The user should beable to view more advanced graphs and also create their own indicators """, className="funcParam"),
    html.P("""Global Variables: """, className="section"),
    html.P("""Sidebar: To be used for creating side-menus. """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""KPI_Options: Generate the layout of the dashboard. """, className="funcParam"),
    html.P("""Dash callbacks: """, className="section"),
    html.P("""- render_variable_choices_kpi: Create a menu of dcc components for                                   the user to choose  plotting options """, className="funcParam"),
    html.P("""plot_graph_kpi: Plot the graph according to user choices. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""Contributions are greatly needed and encouraged here. Mainfunctionality is still lacking in this part. You can use thismodule to add new buttons, input, or other interface-related,element, or maybe a new type of graph (in which case implementit in `graphs.kpis.py`). Working on exporting KPI graphs is    also encouraged """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""KPI_Options(options): """, className="docstring-contents"), 
html.Div([
    html.P("""Generate the layout of the dashboard """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""options (list(dict)): Available datasets as options for `dcc.Dropdown` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""render_variable_choices_kpi(dataset_choice): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a menu of dcc components for the user to choose    plotting options """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""dataset_choice (str): Name of the dataset """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list(list(dict)): Key-value pairs to be input as                          `dcc.Dropdown` options """, className="funcParam"),
    html.P("""Notes on implementation: """, className="section"),
    html.P("""Currently only one type of KPI graph is supported, but moreshould be added later on. Additionally, work should be done        on building custom KPIs and maybe graphs """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""plot_graph_kpi(xvars, yvars, secondary_yvars, dataset_choice): """, className="docstring-contents"), 
html.Div([
    html.P("""Plot the graph according to user choices """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""xvars (str): `x-axis` of the graph """, className="funcParam"),
    html.P("""yvars (str or list(str)): `y-axis`, can be multiple """, className="funcParam"),
    html.P("""secondary_yvars: `bar-chart` variable """, className="funcParam"),
    html.P("""dataset_choice (str): Name of dataset """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""dict: A dictionary holding a plotly figure including layout """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/visualization/app"] = html.Div([
html.H2("""app.py""", className="filename"), 
html.Div([
    html.P("""This module takes care of the menu and choices provided when the"Explore & Visualize" high-level tab is selected """, className="funcParam"),
    html.P("""Dash callbacks: """, className="section"),
    html.P("""- tab_subpages: Given the low-level tab choice, render the                    appropriate view """, className="funcParam"),
    html.P("""render_sidemenu: Render the menu in the side-navbar. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""You should probably not write code here, unless you are defininga new level-2 tab. Here you can find all visuals-generatingfunctionality. Implementations go to their own modules down the    package hierarchy, in `apps.exploration """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""tab_subpages(tab): """, className="docstring-contents"), 
html.Div([
    html.P("""Given the low-level tab choice, render the appropriate view """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""tab (str): The tab the user is currently on """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A list of lists of HTML-dash components, usually within a div """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/visualization/dashboard_maker"] = html.Div([
html.H2("""dashboard_maker.py""", className="filename"), 
html.Div([
    html.P("""This module *will* contain the DashboardMaker, a tool that helps you makeyour own dashboards, or at least get graphs and text in, move them aroundand resize them """, className="funcParam"),
    html.P("""Global Variables: """, className="section"),
    html.P("""Dashboard_Options: Generate the layout of the dashboard. """, className="funcParam"),
    html.P("""Dash callbacks: """, className="section"),
    html.P("""display_output: Currently dummy function to create the dashboard. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""Feel free to work both here and in the `dash_rnd`, we really need it """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""display_output(n_clicks, children): """, className="docstring-contents"), 
html.Div([
    html.P("""Currently dummy function to create the dashboard """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""n_clicks (int): Number of button clicks """, className="funcParam"),
    html.P("""children (list): Current items on the dashboard """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/visualization/__init__"] = html.Div([
html.H2("""visualization""", className="filename"), 
html.Div([
    html.P("""Developer notes: """, className="section"),
    html.P("""Some suggestions on what could be done here: """, className="section"),
    html.P("""Prettify layout and user interface. """, className="funcParam"),
    html.P("""Implement the interface to allow the user to create their own KPIs. """, className="funcParam"),
    html.P("""Work on the DashboardMaker (i.e. dash_rnd) or 3D graphs. """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/visualization/chart_maker"] = html.Div([
html.H2("""chart_maker.py""", className="filename"), 
html.Div([
    html.P("""This module defines the available graphs and creates the interfacefor the 2D dashboard """, className="funcParam"),
    html.P("""Global Variables: """, className="section"),
    html.P("""Sidebar: To be used for creating side-menus. """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""Exploration_Options: Generate the layout of the dashboard. """, className="funcParam"),
    html.P("""make_trace: Create a plotly trace (plot element). """, className="funcParam"),
    html.P("""make_trace_menu: Helper function to create modals and trace menus. """, className="funcParam"),
    html.P("""Dash callbacks: """, className="section"),
    html.P("""plot: Plot the graph according to user choices. """, className="funcParam"),
    html.P("""- render_variable_choices: Update menu of dcc components for the user                               to choose plotting options """, className="funcParam"),
    html.P("""toggle_modal: Open/close the modal for choosing a graph type, per trace. """, className="funcParam"),
    html.P("""- update_graph_choice: Update the value (plot choice) of the respective                           button and its label """, className="funcParam"),
    html.P("""dummy_add_trace: Show ("add") or hide ("remove") traces windows. """, className="funcParam"),
    html.P("""toggle_modal: Notify when a graph is exported. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""You should only write code here with caution. You can use thismodule to add new buttons, input, or other interface-related,element, or maybe a new type of graph (in which case implement    it in `graphs.graphs2d.py`) """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""make_trace_menu(n): """, className="docstring-contents"), 
html.Div([
    html.P("""Helper function to create modals and trace menus """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""n (int): The number/id of trace menu """, className="funcParam"),
    html.P("""Notes: """, className="section"),
    html.P("""Each trace needs a modal with buttons, a menu for choices,        and a callback to update the graph (probably with a "plot" button) """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""Exploration_Options(options): """, className="docstring-contents"), 
html.Div([
    html.P("""Generate the layout of the dashboard """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""options (list(dict)): Available datasets as options for `dcc.Dropdown` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""toggle_modal(n1, n2, *rest): """, className="docstring-contents"), 
html.Div([
    html.P("""Open/close the modal for choosing a graph type, per trace """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""n1 (int): Number of button clicks, graph selection button """, className="funcParam"),
    html.P("""n2 (int): Number of button clicks, close menu button """, className="funcParam"),
    html.P("""*rest (list(int)): Number of button clicks, for all graph types                               for all traces """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""bool: Whether to open or close the modal """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""update_graph_choice(*inputs): """, className="docstring-contents"), 
html.Div([
    html.P("""Update the value (plot choice) of the respective button and its label """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""*inputs: The different plots (icons) for all shown/hidden traces                     for every graph type (total: max_traces * graph_types) """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list(str): The label and value of the various buttons, per                       trace menu """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""render_variable_choices(dataset_choice): """, className="docstring-contents"), 
html.Div([
    html.P("""Update menu of dcc components for the user to choose plotting options """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""dataset_choice (str): Name of the dataset """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list(list(dict)): Variable options passed to `dcc.Dropdown` """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""dummy_add_trace(add_trace, remove_trace, n_children): """, className="docstring-contents"), 
html.Div([
    html.P("""Show ("add") or hide ("remove") traces windows """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""add_trace (int): Number of button clicks """, className="funcParam"),
    html.P("""remove_trace (int): Number of button clicks """, className="funcParam"),
    html.P("""n_children (int): Number of traces currently showing """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list(dict): The styles (i.e. shown/hidden) of the trace menus """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""plot(*params): """, className="docstring-contents"), 
html.Div([
    html.P("""Plot the graph according to user choices """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""*params (list): Number of traces, the choices of graph types, thechoices of x variables, the choices of y variables,                        and the dataset choice """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""dict: The figure to be plotted """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""make_trace(graph_choice, xvar, yvar, zvar=None, df=None): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a plotly trace (plot element) """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""graph_choice (str): The type of graph to create """, className="funcParam"),
    html.P("""xvar (str): `x-axis` of the graph """, className="funcParam"),
    html.P("""yvar (str): `y-axis` """, className="funcParam"),
    html.P("""zvar (str): `z-axis`, if applicable """, className="funcParam"),
    html.P("""df (`pd.DataFrame`): The data to plot """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list(`plotly.go.*`): Plotly traces """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/visualization/text_viz"] = html.Div([
html.H2("""text_viz.py""", className="filename"), 
html.Div([
    html.P("""This module is about visualizing text data """, className="funcParam"),
    html.P("""Global Variables: """, className="section"),
    html.P("""Sidebar: To be used for creating side-menus. """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""TextViz_Options: Generate the layout of the dashboard. """, className="funcParam"),
    html.P("""Dash callbacks: """, className="section"),
    html.P("""- plot_graph_text: Currently only word cloud visualizations are                       supported, from given text """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""Contributions are encouraged here. Main functionality is stilllacking in this part. You can use this module to add new buttons,input, or other interface-related, element, or maybe a new typeof text visualizations (in which case implement it in a new file`graphs.textviz.py`). Like with other modules, working on exportingnetwork graphs is encouraged. Finally, adding new visualization typesis very welcome as well, but avoid loading huge word vectors files    at this stage of development """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""TextViz_Options(): """, className="docstring-contents"), 
html.Div([
    html.P("""Generate the layout of the dashboard """, className="funcParam"),
    html.P("""Optional Args: """, className="section"),
    html.P("""options (list(dict)): Not relevant; here only for API compatibility """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""plot_graph_text(n_clicks, text): """, className="docstring-contents"), 
html.Div([
    html.P("""Currently only word cloud visualizations are supported """, className="funcParam"),
    html.P("""from given text """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""n_clicks (int): Number of button clicks """, className="funcParam"),
    html.P("""text (str): User-provided text used to create a word cloud """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""str: the image encoded appropriately to be set as the 'src'             value of the `img` elemen """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/visualization/networks"] = html.Div([
html.H2("""networks.py""", className="filename"), 
html.Div([
    html.P("""This module is about viewing network data """, className="funcParam"),
    html.P("""Global Variables: """, className="section"),
    html.P("""Sidebar: To be used for creating side-menus. """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""Network_Options: Generate the layout of the dashboard. """, className="funcParam"),
    html.P("""Dash callbacks: """, className="section"),
    html.P("""- render_variable_choices_network: Create a menu of dcc componentsfor the user to choose plotting                                       options """, className="funcParam"),
    html.P("""plot_network: Plot the network graph according to user choices. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""Contributions are encouraged here, although you should considerstarting with another part if you're new to dash or this project.Main functionality is still lacking in this part. You can use thismodule to add new buttons, input, or other interface-related,element, or maybe a new type of graph (in which case implementit in a new file `graphs.networks.py`). Like with other modules,    working on exporting network graphs is encouraged """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""Network_Options(options): """, className="docstring-contents"), 
html.Div([
    html.P("""Generate the layout of the dashboard """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""options (list(dict)): Available datasets as options for `dcc.Dropdown` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""render_variable_choices_network(dataset_choice): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a menu of dcc components for the user to choose        plotting options """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""dataset_choice (str): Name of the dataset """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list(list(dict)): Key-value pairs to be input as                          `dcc.Dropdown` options """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""plot_network(in_node, out_node, layout_choice, dataset_choice): """, className="docstring-contents"), 
html.Div([
    html.P("""Plot the network graph according to user choices """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""in_node (str): Column name containing the values of                      nodes from where links start """, className="funcParam"),
    html.P("""out_node (str): Column name for nodes where links end """, className="funcParam"),
    html.P("""layout_choice (str): One of the layouts available in                             Cytoscape """, className="funcParam"),
    html.P("""dataset_choice (str): Name of dataset """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""[list(dict), dict]: A list of elements (dicts for Cytoscape)                            and the layout for the graph """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/visualization/maps"] = html.Div([
html.H2("""maps.py""", className="filename"), 
html.Div([
    html.P("""This module handles map plotting. Currently only 3 types of map types aresupported (aggregated choropleth, geo-scatterplot, and lines on map) """, className="funcParam"),
    html.P("""Global Variables: """, className="section"),
    html.P("""Sidebar: To be used for creating side-menus. """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""Map_Options: Generate the layout of the dashboard. """, className="funcParam"),
    html.P("""- country2code: It takes a string and tries to convert it to a country                    code by trying out various encodings """, className="funcParam"),
    html.P("""Dash callbacks: """, className="section"),
    html.P("""- render_variable_choices_maps: Create a menu of dcc components for                                    the user to choose plotting options """, className="funcParam"),
    html.P("""- show_hide_aggregator_dropdown: Disable some dropdowns. Some maps do                                     not handle all the fields """, className="funcParam"),
    html.P("""plot_map: Plot the map according to user choices. """, className="funcParam"),
    html.P("""TODO: """, className="section"),
    html.P("""Implement https://plot.ly/python/choropleth-maps/#choropleth-inset-ma """, className="funcParam"),
    html.P("""TODO: """, className="section"),
    html.P("""Add text/annotations to the various maps """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""Map_Options(options): """, className="docstring-contents"), 
html.Div([
    html.P("""Generate the layout of the dashboard """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""options (list(dict)): Available datasets as options for `dcc.Dropdown` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""render_variable_choices_maps(dataset_choice): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a menu of dcc components for the user to choose    plotting options """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""dataset_choice (str): Name of the dataset """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list(list(dict)): Key-value pairs to be input as                          `dcc.Dropdown` options """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""country2code(value): """, className="docstring-contents"), 
html.Div([
    html.P("""Country(alpha_2='DE', alpha_3='DEU', name='Germany', numeric='276' """, className="funcParam"),
    html.P("""official_name='Federal Republic of Germany' """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""show_hide_aggregator_dropdown(map_type): """, className="docstring-contents"), 
html.Div([
    html.P("""Disable some dropdowns. Some maps do not handle all the fields """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""map_type (str): The type of map """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list(bool): What fields are to be disabled """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""plot_map(lat_var, lon_var, country, z_var, map_type, aggregator_type, """, className="docstring-contents"), 
html.Div([
    html.P("""Plot the map according to user choices """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""lat_var (str): Column name for latitude """, className="funcParam"),
    html.P("""lon_var (str): Column name for latitude """, className="funcParam"),
    html.P("""country (str): Column name for the country. Accepted valuesinclude 3-letter country codes and full names                       or anything else pycountry can decode """, className="funcParam"),
    html.P("""z_var (str): Column name for choropleth colors """, className="funcParam"),
    html.P("""map_type (str): Type of math, one of three choices: Simple or                        Aggregated Choropleth, or Lines on map """, className="funcParam"),
    html.P("""aggregator_type (str): Type of aggregation to perform on the                               data (e.g. mean, max) """, className="funcParam"),
    html.P("""dest_lat (str): Column name for destination latitude, if drawing                        lines on map chart """, className="funcParam"),
    html.P("""dest_long (str): Column name for destination longitude, if drawing                        lines on map chart """, className="funcParam"),
    html.P("""colorscale (str): Colorscale for the choropleth, one of several                          as defined in plotly """, className="funcParam"),
    html.P("""projection_type (str): Projection type, one of several as                               defined by plotly """, className="funcParam"),
    html.P("""dataset_choice_maps (str): Name of dataset """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""dict: The figure to draw """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/visualization/graphs/kpis"] = html.Div([
html.H2("""kpis.py""", className="filename"), 
html.Div([
    html.P("""This module collects functions and utilities for KPI visualizationbut may also be used to add other options and core implementation logic """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""- baseline_graph: Create a baseline graph: a lineplot for the                      timeseries and its baseline, and a barchart """, className="funcParam"),
    html.P("""baseline: Calculate the baseline for a time series. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""Feel free to write code here either to improve current or to addnew functionality. This part is in need of both customization and    presets """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""baseline(values, min_max="min", deg=7, ema_window=7, roll_window=7, """, className="docstring-contents"), 
html.Div([
    html.P("""Calculate the baseline for a time series """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""values (iterable(int)): """, className="section"),
    html.P("""min_max (str): Whether to calculate an upper or lower baseline """, className="funcParam"),
    html.P("""deg (int): The degree of the polynomial fitting """, className="funcParam"),
    html.P("""ema_window (int): Window for the exponential moving average """, className="funcParam"),
    html.P("""roll_window (int): Window for the simple moving average """, className="funcParam"),
    html.P("""max_it (int): Number of iterations for `peakutils.baseline` """, className="funcParam"),
    html.P("""tol (float): Least amount of change before termination of fitting                     in `peakutils.baseline` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""np.array: the baseline """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""baseline_graph(df, xvars, yvars, secondary_yvars): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a baseline graph: a lineplot for the timeseries and    its baseline, and a barchart """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""df (`pd.DataFrame`): The data """, className="funcParam"),
    html.P("""xvars (str): Column of `df`; `x-axis` """, className="funcParam"),
    html.P("""yvars (str or list(str)): Column(s) of `df`; lineplot(s) """, className="funcParam"),
    html.P("""secondary_yvars (str):  Column of `df`; bar-chart """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list: Plotly traces """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/visualization/graphs/utils"] = html.Div([
html.H2("""utils.py""", className="filename"), 
html.Div([
    html.P("""Utilities for the visualization app. This file might later be merged withanother; it is still in active development """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""create_button: Create an image-button for the selected graph type. """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""create_button(graph_type, graph_label, n): """, className="docstring-contents"), 
html.Div([
    html.P("""Create an image-button for the selected graph type """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""graph_type (str): The type of graph, and value of the button. See                          graphs2d_choices for options """, className="funcParam"),
    html.P("""graph_label (str): The label displayed on the button """, className="funcParam"),
    html.P("""n (int): The number/id of the button (needed when creating buttons                 per trace) """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A list of Dash elements """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/visualization/graphs/__init__"] = html.Div([
html.H2("""graphs""", className="filename"), 
html.Div([
    html.P("""Developer notes: """, className="section"),
    html.P("""Some suggestions on what could be done here: """, className="section"),
    html.P("""Define more PDF report layouts (see also `layouts.py`). """, className="funcParam"),
    html.P("""- Add more graph types in any of the categories (but avoid word          vector visualizations) """, className="funcParam"),
    html.P("""Add additional functionality in KPIs. """, className="funcParam"),
    html.P("""Improve baseline graph and/or function. """, className="funcParam"),
    html.P("""Improve network visualizations. """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/visualization/graphs/graphs2d"] = html.Div([
html.H2("""graphs2d.py""", className="filename"), 
html.Div([
    html.P("""This module contains the implementations of graphing functions.I skipped adding docstrings for every function since most of themare one-liners anyway and should be pretty obvious """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""scatterplot: Create a 2D scatterplot. """, className="funcParam"),
    html.P("""line_chart: Create a lineplot. """, className="funcParam"),
    html.P("""bubble_chart: Create a bubble chart. """, className="funcParam"),
    html.P("""bar: Create a bar chart. """, className="funcParam"),
    html.P("""filledarea: Create a lineplot with filled areas. """, className="funcParam"),
    html.P("""errorbar: Create a lineplot with error bars (currently fixed). """, className="funcParam"),
    html.P("""histogram: Create a histogram. """, className="funcParam"),
    html.P("""heatmap: Create a heatmap of column correlations. """, className="funcParam"),
    html.P("""density2d: Create a heatmap. """, className="funcParam"),
    html.P("""pie: Create a pie chart. """, className="funcParam"),
    html.P("""pairplot: Create a grid of plots with matplotlib. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""Feel free to write code here either to improve current or to addnew functionality. Also feel free to add or tamper with styles    and/or helper functions """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""_simple_scatter(x, y, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Internal function used to create a lot of other plots """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""scatterplot(x, y, z=None, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a 2D scatterplot. Parameter `z` is for a unified API """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""x (iterable): Values for x-axis """, className="funcParam"),
    html.P("""y (iterable): Values for y-axis """, className="funcParam"),
    html.P("""**params: Any other keyword argument passed to `go.Scatter` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`go.Scatter """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""line_chart(x, y, z=None, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a lineplot. Parameter `z` is for a unified API """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""x (iterable): Values for x-axis """, className="funcParam"),
    html.P("""y (iterable): Values for y-axis """, className="funcParam"),
    html.P("""**kwargs: Any other keyword argument passed to `go.Scatter` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`go.Scatter """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""bubble_chart(x, y, size, z=None, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a bubble chart. Parameter `z` is for a unified API """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""x (iterable): Values for x-axis """, className="funcParam"),
    html.P("""y (iterable): Values for y-axis """, className="funcParam"),
    html.P("""size (iterable): Sized of bubbles """, className="funcParam"),
    html.P("""**kwargs: Any other keyword argument passed to `go.Scatter` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`go.Scatter """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""bar(x, y, z=None, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a bar chart. Parameter `z` is for a unified API """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""x (iterable): Values for x-axis """, className="funcParam"),
    html.P("""y (iterable): Values for y-axis """, className="funcParam"),
    html.P("""**kwargs: Any other keyword argument passed to `go.Bar` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`go.Bar """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""filledarea(x, y, z=None, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a lineplot with filled areas. Parameter `z` is for a unified API """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""x (iterable): Values for x-axis """, className="funcParam"),
    html.P("""y (iterable): Values for y-axis """, className="funcParam"),
    html.P("""**kwargs: Any other keyword argument passed to `go.Scatter` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`go.Scatter """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""errorbar(x, y, z=None, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a lineplot with error bars (currently fixed). Parameter `z` is    for a unified API """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""x (iterable): Values for x-axis """, className="funcParam"),
    html.P("""y (iterable): Values for y-axis """, className="funcParam"),
    html.P("""**kwargs: Any other keyword argument passed to `go.Scatter` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`go.Scatter """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""histogram(x, y=None, z=None, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a histogram. Parameters `y` and `z` are for a unified API """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""x (iterable): Values for the histogram """, className="funcParam"),
    html.P("""y: Not applicable """, className="funcParam"),
    html.P("""z: Not applicable """, className="funcParam"),
    html.P("""**kwargs: Any other keyword argument passed to `go.Histogram` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`go.Histogram """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""heatmap(x, y, z=None, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a histogram. Parameter `z` is for a unified API """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""x (iterable): Values for x-axis """, className="funcParam"),
    html.P("""y (iterable): Values for y-axis """, className="funcParam"),
    html.P("""z: Not applicable """, className="funcParam"),
    html.P("""**kwargs: Any other keyword argument passed to `go.Histogram` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`go.Heatmap """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""density2d(x, y, z=None, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a histogram. Parameter `z` is for a unified API """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""x (iterable): Values for the density x-axis """, className="funcParam"),
    html.P("""y (iterable): Values for the density y-axis """, className="funcParam"),
    html.P("""z: Not applicable """, className="funcParam"),
    html.P("""**kwargs: Any other keyword argument passed to `go.Histogram2dContour` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list[`go.Scatter`, `go.Histogram2dContour` """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""pie(x, y, z=None, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a pie chart. Parameter `z` is for a unified API """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""x (iterable): The labels for the pie-chart regions """, className="funcParam"),
    html.P("""y (iterable): The values """, className="funcParam"),
    html.P("""z: Not applicable """, className="funcParam"),
    html.P("""**kwargs: Any other keyword argument passed to `go.Histogram2dContour` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""`go.Pie """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""pairplot(x, y=None, z=None, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a grid of plots with matplotlib. Each row/col represents onecolumn from the dataframe. For the main diagonal histograms are    plotted, and for everywhere else scatterplots """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""x (`pd.DataFrame`): The dataset """, className="funcParam"),
    html.P("""y: Not applicable """, className="funcParam"),
    html.P("""z: Not applicable """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A plotly figure """, className="funcParam"),
    html.P("""Implementation details: """, className="section"),
    html.P("""Clipping is needed because the histogram may be a floatand floats often have rounding errors (here the negative        throws a plotly error """, className="funcParam"),
    html.P("""which need to be updated. Example of what that looks like: """, className="section"),
    html.P("""`Rectangle(xy=(4.3, 0), width=0.36, height=9, angle=0) """, className="funcParam"),
    html.P("""I don't know why but it seems it ONLY accepts the first patchto be changed. When I tried looping over all of them it threw        the same error """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""scatterplot3d(x, y, z, **kwargs): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a 3D scatterplot """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""x  (iterable): `x-axis` data """, className="funcParam"),
    html.P("""y  (iterable): `y-axis` data """, className="funcParam"),
    html.P("""z  (iterable): `z-axis` data """, className="funcParam"),
    html.P("""**kwargs: Anything accepted by `plotly.graph_objs.Scatter3d` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list: Plotly traces """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/visualization/graphs/textviz"] = html.Div([
html.H2("""textviz.py""", className="filename"), 
html.Div([
    html.P("""This module collects functions and utilities for text visualizations """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""create_wordcloud: Generate a wordcloud and save it to a file. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""Feel free to write code here either to improve current or to addnew functionality. Avoid word vectors visualizations at this stage    of development as it will simply increase (re)load times for the app """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""create_wordcloud(text, user_id, *, background_color="white", """, className="docstring-contents"), 
html.Div([
    html.P("""Generate a wordcloud and save it to a file """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""text (str): Raw text for the word cloud """, className="funcParam"),
    html.P("""user_id (str): Session/user id. Needed to save the image """, className="funcParam"),
    html.P("""background_color (str):  Color as accepted by wordcloud / matplotlib """, className="funcParam"),
    html.P("""additional_stopwords (list(str)): Stopwords to remove along                                          with the predefined ones """, className="funcParam"),
    html.P("""max_words (int): Max number of words to include in the wordcloud """, className="funcParam"),
    html.P("""save (bool): Whether to save the figure. Currently unimportant """, className="funcParam"),
    html.P("""ret (bool): Whether to return a value. Currently unimportant """, className="funcParam"),
    html.P("""**kwargs: Anything that `wordcloud.WordCloud` accepts """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""Non """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/modeling/server"] = html.Div([
html.H2("""server.py""", className="filename"), 
html.Div([
    html.P("""This module is only here because of the Dash app spanning multiple files.General configurations of the underlying app and server go here as well """, className="funcParam"),
    html.P("""Global Variables: """, className="section"),
    html.P("""- app: The Dash server, imported everywhere that a dash callback           needs to be defined """, className="funcParam"),
    html.P("""r: The connection to Redis. """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/modeling/styles"] = html.Div([
html.H2("""styles.py""", className="filename"), 
html.Div([
    html.P("""This module is meant as a collection of styles that cannot be definedin the CSS (e.g. due to JS/Dash libraries' rendered elements not beingviewable in inspection, or some overriding) """, className="funcParam"),
    html.P("""Available styles: """, className="section"),
    html.P("""- cyto_stylesheet: The style used for the Model Builder, and willprobably also be used for other cytoscape                       visualizations """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/modeling/single_model"] = html.Div([
html.H2("""single_model.py""", className="filename"), 
html.Div([
    html.P("""This module defines the interface for fitting simple models for thethree main machine learning tasks (regression, classification, andclustering. It also reports fitting metrics and a graph """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""single_model_options: Generate the layout of the dashboard. """, className="funcParam"),
    html.P("""Dash callbacks: """, className="section"),
    html.P("""- render_choices: Create a menu for fitting options, depending of                      the problem type """, className="funcParam"),
    html.P("""- fit_model: Take user choices and, if all are present, fit the                 appropriate model """, className="funcParam"),
    html.P("""render_report: Get the results (graph and text metrics) and show them. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""Feel free to experiment as much as you like here, although you    probably want to write code elsewhere """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""single_model_options(options): """, className="docstring-contents"), 
html.Div([
    html.P("""Generate the layout of the dashboard """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""options (list(dict)): Available datasets as options for `dcc.Dropdown` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""render_report(selected_tab, results_metrics, results_visualizations): """, className="docstring-contents"), 
html.Div([
    html.P("""Get the results (graph and text metrics) and show them. This isdone in two steps instead of one because dbc.Tabs does not size    the `dcc.Graph` correctly """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""selected_tab (str): The type of report metrics to show """, className="funcParam"),
    html.P("""results_metrics (Dash elements): The elements showing text metrics """, className="funcParam"),
    html.P("""results_visualizations (Dash elements): The elements showing graphs """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""render_choices(problem_type, dataset_choice): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a menu for fitting options, depending of the problem type. It    returns dropdowns with algorithm choices """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""problem_type (str): One of: regression, classification, clustering """, className="funcParam"),
    html.P("""dataset_choice (str): Name of the dataset """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""fit_model(xvars, yvars, algo_choice, dataset_choice, problem_type): """, className="docstring-contents"), 
html.Div([
    html.P("""Take user choices and, if all are present, fit the appropriate model.The results of fitting are given to hidden divs. When the user uses    the tab menu then the appropriate menu is rendered """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""xvars (list(str)): predictor variables """, className="funcParam"),
    html.P("""yvars (str): target variable """, className="funcParam"),
    html.P("""algo_choice (str): The choice of algorithm type """, className="funcParam"),
    html.P("""dataset_choice (str): Name of the dataset """, className="funcParam"),
    html.P("""problem_type (str): The type of learning problem """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list, dict: Dash element(s) with the results of model fitting """, className="funcParam"),
    html.P("""and parameters for plotting a graph """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/modeling/app"] = html.Div([
html.H2("""app.py""", className="filename"), 
html.Div([
    html.P("""This module takes care of the menu and choices provided when the"Analyze & Predict" high-level tab is selected """, className="funcParam"),
    html.P("""Dash callbacks: """, className="section"),
    html.P("""- tab_subpages: Given the low-level tab choice, render the                    appropriate view """, className="funcParam"),
    html.P("""render_sidemenu: Render the menu in the side-navbar. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""You should probably not write code here, unless you are defininga new level-2 tab. Here you can find functionality to define ortrain ML / NN models. Implementations go to their own modules    down the package hierarchy, in `apps.analyze` """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""tab_subpages(tab): """, className="docstring-contents"), 
html.Div([
    html.P("""Given the low-level tab choice, render the appropriate view """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""tab (str): The tab the user is currently on """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A list of lists of HTML-dash components, usually within a div """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/modeling/model_builder"] = html.Div([
html.H2("""model_builder.py""", className="filename"), 
html.Div([
    html.P("""This module will be used to graphically create models.RapidMiner, Weka, Orange, etc, ain't got sh!t on us : """, className="funcParam"),
    html.P("""You should probably not write code here, UNLESS you knowwhat you're doing """, className="funcParam"),
    html.P("""Dash callbacks: """, className="section"),
    html.P("""- update_radio_buttons_modify_params: List the available options for                                          the selected node and parameter """, className="funcParam"),
    html.P("""modify_graph: Handle everything about the model builder. """, className="funcParam"),
    html.P("""- render_deletion_menu: Update the dropdown that lists the nodes                            available for deletion """, className="funcParam"),
    html.P("""add_node_menu_toggle: Show/hide the menu for adding new nodes. """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/modeling/__init__"] = html.Div([
html.H2("""modeling""", className="filename"), 
html.Div([
    html.P("""Developer notes: """, className="section"),
    html.P("""Some suggestions on what could be done: """, className="section"),
    html.P("""Better reporting on fitting results. """, className="funcParam"),
    html.P("""Download a model. """, className="funcParam"),
    html.P("""Predict a test set. """, className="funcParam"),
    html.P("""Prettier interfaces. """, className="funcParam"),
    html.P("""Implement Econometrics functionality. """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/modeling/pipelines"] = html.Div([
html.H2("""pipelines.py""", className="filename"), 
html.Div([
    html.P("""This module defines the interface for fitting (pre)defined pipelines """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""Pipeline_Options: Generate the layout of the dashboard. """, className="funcParam"),
    html.P("""Dash callbacks: """, className="section"),
    html.P("""- render_variable_choices_pipeline: Create a menu of dcc componentsfor the user to choose fitting                                        options """, className="funcParam"),
    html.P("""fit_pipeline_model: Fits any pipelines defined. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""You should probably not write code here, UNLESS reworking the interface """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""Pipeline_Options(options): """, className="docstring-contents"), 
html.Div([
    html.P("""Generate the layout of the dashboard """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""options (list(dict)): Available datasets as options for `dcc.Dropdown` """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""render_report(selected_tab, results_metrics, results_visualizations): """, className="docstring-contents"), 
html.Div([
    html.P("""Get the results (graph and text metrics) and show them. This isdone in two steps instead of one because dbc.Tabs does not size    the `dcc.Graph` correctly """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""selected_tab (str): The type of report metrics to show """, className="funcParam"),
    html.P("""results_metrics (Dash elements): The elements showing text metrics """, className="funcParam"),
    html.P("""results_visualizations (Dash elements): The elements showing graphs """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""A Dash element or list of elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""render_variable_choices_pipeline(pipeline_choice): """, className="docstring-contents"), 
html.Div([
    html.P("""Create a menu of dcc components to select pipeline and variables """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""algo_choice_pipeline (str): Choice among (pre)defined pipelines """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list: Dash elements """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""fit_model(xvars, yvars, pipeline_choice): """, className="docstring-contents"), 
html.Div([
    html.P("""Take user choices and, if all are present, fit the appropriate model.The results of fitting are given to hidden divs. When the user uses    the tab menu then the appropriate menu is rendered """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""xvars (list(str)): predictor variables """, className="funcParam"),
    html.P("""yvars (str): target variable """, className="funcParam"),
    html.P("""algo_choice (str): The choice of algorithm type """, className="funcParam"),
    html.P("""dataset_choice (str): Name of the dataset """, className="funcParam"),
    html.P("""problem_type (str): The type of learning problem """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list, dict: Dash element(s) with the results of model fitting """, className="funcParam"),
    html.P("""and parameters for plotting a graph """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/modeling/models/pipeline_classes"] = html.Div([
html.H2("""pipeline_classes.py""", className="filename"), 
html.Div([
    html.P("""This module collects every model class, including input and transformers """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""Feel free to tamper with anything or add your own models and classes.Everything should implement an sklearn-like API providing a fit and(more importantly) a transform method. It should also have a`modifiable_params` dictionary with the names of attributes that canbe modified and a list of possible values (keep them limited, for now).Input classes should subclass `GenericInput`. If you add new classes    remember to modify `ml_options` in `graph_structures.py` """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""Input classes should subclass `GenericInput`. If you add new classes \ """, className="docstring-contents"), 
html.Div([
    html.P("""======== Custom classes ======= """, className="funcParam"),
    html.P("""All custom classes should subclass these ones """, className="funcParam"),
    html.P("""This is done for checks down the line tha """, className="funcParam"),
    html.P("""determine properties of nodes of the Grap """, className="funcParam"),
    html.P("""which in turn is useful for selecting datase """, className="funcParam"),
    html.P("""and being able to create custom features o """, className="funcParam"),
    html.P("""handle output """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""InputFile(BaseEstimator, TransformerMixin): """, className="docstring-contents"), 
html.Div([
    html.P("""An input node used for selecting a user-uploaded dataset """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""predict(self, X): """, className="docstring-contents"), 
html.Div([
    html.P("""======== Prebuilt classes ======= """, className="funcParam"),
    html.P("""For EVERY model that is expected to have parametrizatio """, className="funcParam"),
    html.P("""you are expected to give its class a `modifiable_params """, className="funcParam"),
    html.P("""dict with keys being the function argument and values th """, className="funcParam"),
    html.P("""allowed set of values (make it limited, i.e. few choices """, className="funcParam"),
    html.P("""Also, the first is assumed to be the default value whic """, className="funcParam"),
    html.P("""will be passed to the model upon the creation of pipelines """, className="funcParam"),
    html.P("""And of course it must have `fit` and transform methods """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""you are expected to give its a `modifiable_params` """, className="docstring-contents"), 
html.Div([
    html.P("""======== Transformers ======= """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""you are expected to give its a `modifiable_params` """, className="docstring-contents"), 
html.Div([
    html.P("""======== Regression ======= """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""you are expected to give its a `modifiable_params` """, className="docstring-contents"), 
html.Div([
    html.P("""======== Classification ======= """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""you are expected to give its a `modifiable_params` """, className="docstring-contents"), 
html.Div([
    html.P("""======== Clustering ======= """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/modeling/models/__init__"] = html.Div([
html.H2("""models""", className="filename"), 
html.Div([
    html.P("""Developer notes: """, className="section"),
    html.P("""Some suggestions on what could be done: """, className="section"),
    html.P("""Improve handling of pipeline traversal and creation. """, className="funcParam"),
    html.P("""- Add new classes for the pipelines (inputs, transformers,        data cleaners, models) """, className="funcParam"),
    html.P("""Improve handling of data / use better data structures. """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/modeling/models/graph_structures"] = html.Div([
html.H2("""graph_structures.py""", className="filename"), 
html.Div([
    html.P("""This module collects function to traverse the ModelBuilder graph """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""- create_pipelines: Create pipelines from cytoscape elements and a                        dict that maps a node type to relevant parameters """, className="funcParam"),
    html.P("""- find_pipeline_input: """, className="section"),
    html.P("""Classes: """, className="section"),
    html.P("""- Node: A class to hold data for the nodes. Validation and advanced            functionality may be added later """, className="funcParam"),
    html.P("""Global variables: """, className="section"),
    html.P("""- ml_options (list(dict)): The available sklearn-like classes for use                               with the ModelBuilder """, className="funcParam"),
    html.P("""node_options (dict): Reverse mapping of ml_options. """, className="funcParam"),
    html.P("""orders (dict): The vertical ordering (position) of groups of nodes. """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""Feel free to add or modify stuff here, but be cautious. You probablyneed experience with graphs and/or trees and traversal algorithms.    The current implementation (unless I'm mistaken) are Breadth-First """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""Node: """, className="docstring-contents"), 
html.Div([
    html.P("""A class to hold data for a node. Validation and advanced functionality    may be added later """, className="funcParam"),
    html.P("""Create the node either by supplying `options` or `node_type` and    a `note_id` """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""options (dict): A cytoscape element """, className="funcParam"),
    html.P("""node_type (str): One of the keys of node_options """, className="funcParam"),
    html.P("""node_id (str): Unique node identifier """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""NodeCollection: """, className="docstring-contents"), 
html.Div([
    html.P("""A collection of nodes with some added functionality for rendering them """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""nodes (list(dict)): A list of Cytoscape elements """, className="funcParam"),
    html.P("""graph (`_Graph`): The parent instance """, className="funcParam"),
    html.P("""Attributes: """, className="section"),
    html.P("""parent_nodes (list(dict)): Cytoscape elements that function as                                   parent/group nodes """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""remove_node(self, node_id): """, className="docstring-contents"), 
html.Div([
    html.P("""Remove a node and its edges """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""node_id (str): ID of the node to be removed """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""Non """, className="funcParam"),
    html.P("""Notes on implementation: """, className="section"),
    html.P("""Consider whether connecting the nodes that were connected to            the removed node """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""EdgeCollection: """, className="docstring-contents"), 
html.Div([
    html.P("""A collection of edges with some added functionality for rendering them """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""edges (list(dict)): A list of Cytoscape elements """, className="funcParam"),
    html.P("""graph (`_Graph`): The parent instance """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""create_edges(self, selected): """, className="docstring-contents"), 
html.Div([
    html.P("""Add edges between the selected nodes """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""selected (list(dict)): A list of Cytoscape elements """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""Non """, className="funcParam"),
    html.P("""Notes on implementation: """, className="section"),
    html.P("""Currently, edges take their direction according to theorder in which the nodes where clicked, not allowing            going back but allowing connections within the same level """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""_Graph: """, className="docstring-contents"), 
html.Div([
    html.P("""A Graph to hold collections of nodes and edges and perform functions    on them. INTERNAL REPRESENTATION """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""render_graph(self): """, className="docstring-contents"), 
html.Div([
    html.P("""Calculates positions for all nodes in the graph and render it """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list(dict): A list of Cytoscape elements """, className="funcParam"),
], className="func_docstring"),

], className='file_container')



layouts["/home/kmourat/GitHub/EDA_miner_public/EDA_miner/modeling/models/pipeline_creator"] = html.Div([
html.H2("""pipeline_creator.py""", className="filename"), 
html.Div([
    html.P("""This module collects function to traverse the ModelBuilder graph """, className="funcParam"),
    html.P("""Functions: """, className="section"),
    html.P("""- create_pipelines: Create pipelines from cytoscape elements and a                        dict that maps a node type to relevant parameters """, className="funcParam"),
    html.P("""- find_pipeline_node: Given a goal creates a function that searches apipeline for nodes of that type (or itssubclasses). Essentially goes the reverse way                          of `create_pipelines` """, className="funcParam"),
    html.P("""- find_input_node: Find the input node of a pipeline containing                       a `FeatureMaker` """, className="funcParam"),
    html.P("""Notes to others: """, className="section"),
    html.P("""Feel free to add or modify stuff here, but be cautious. You probablyneed experience with graphs and/or trees and traversal algorithms.    The current implementation (unless I'm mistaken) are Breadth-First """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""create_pipelines(graph): """, className="docstring-contents"), 
html.Div([
    html.P("""Create pipelines from cytoscape elements and a dict that maps a node    type to relevant parameters """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""data (list(dict)): Cytoscape elements """, className="funcParam"),
    html.P("""node_options (dict): Parameters to be passed at the classes as                             they are instantiated for the pipeline(s) """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""list, list: The pipelines and the terminal nodes """, className="funcParam"),
    html.P("""Notes on implementation: """, className="section"),
    html.P("""This uses networkx for easier traversal. Feel free to implement        your own travel if you want to """, className="funcParam"),
], className="func_docstring"),

html.Br(), html.H3("""find_pipeline_node(GOAL): """, className="docstring-contents"), 
html.Div([
    html.P("""Given a goal creates a function that searches a pipeline for nodes ofthat type (or its subclasses). Essentially goes the reverse way of    `create_pipelines` """, className="funcParam"),
    html.P("""Args: """, className="section"),
    html.P("""GOAL (sklearn-like class): Stopping criteria / node for the recursion """, className="funcParam"),
    html.P("""Returns: """, className="section"),
    html.P("""The node of type `GOAL`, if found, else `None` """, className="funcParam"),
], className="func_docstring"),

], className='file_container')
