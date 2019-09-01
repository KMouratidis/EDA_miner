"""
This is the main application from which to run EDA Miner. Use a command \
like `gunicorn wsgi:application`. It is also here where you can add new apps.

Notes to others:
    * To add a new app follow the instructions below (steps 0 - 4). If the \
    app doesn't need login then skip steps 2.1 - 2.3. Also skip the 0th step \
    if it is not a Dash app.
"""

from flask_app import flask_app
from config import config
from utils import redis_startup
from data_server import app as data_app
from viz_server import app as viz_app
from model_server import app as model_app
from docs_server import app as docs_app
from presentation_server import app as presentation_app

from app_extensions import mail, login_manager, db

from werkzeug.wsgi import DispatcherMiddleware
from templates import base_dash


# Handle generic configurations, DO NOT MODIFY unless you
# want to change server stuffs.

flask_app.config.update(config)


# If you're adding a new app, follow the steps below here

# STEP 0
# Dash applications initial html can be modified by using
# index strings. This one is responsible for the menus.
# Flask apps don't need this (nor can they use it).
data_app.index_string = base_dash.dash_appstring
viz_app.index_string = base_dash.dash_appstring
model_app.index_string = base_dash.dash_appstring
docs_app.index_string = base_dash.dash_appstring

# STEP 1
# Update each app's server configurations
flask_app.config.update(config)
data_app.server.config.update(config)
viz_app.server.config.update(config)
model_app.server.config.update(config)
presentation_app.server.config.update(config)

# STEP 2
# Initialize extensions for the apps to use
# For the Dash apps, initialize the underlying Flask server

# STEP 2.1
# Initialize the login manager for each of the apps
login_manager.init_app(flask_app)
login_manager.init_app(data_app.server)
login_manager.init_app(viz_app.server)
login_manager.init_app(model_app.server)
login_manager.init_app(presentation_app.server)

# STEP 2.2
# Initialize the database extension
db.init_app(flask_app)
db.init_app(data_app.server)
db.init_app(viz_app.server)
db.init_app(model_app.server)
db.init_app(presentation_app.server)

# STEP 2.3
# Initialize the mail extension for the apps that use it
mail.init_app(flask_app)

# TODO: Add a dash app for monitoring flask_prometheus
#       https://github.com/pilosus/flask_prometheus_metrics
# from flask_prometheus_metrics import register_metrics
# from prometheus_client import make_wsgi_app
# register_metrics(flask_app, app_version="v0.1.2", app_config="staging")
# register_metrics(data_app.server, app_version="v0.1.2", app_config="staging")


# Initialize the Redis server with some datasets
with flask_app.app_context() as ctx:
    redis_conn = redis_startup()


# STEP 3
# Give them a sub-domain to use
application = DispatcherMiddleware(flask_app, {
    "/data": data_app.server,
    "/viz": viz_app.server,
    "/modeling": model_app.server,
    "/docs": docs_app.server,
    "/graphs": presentation_app.server,
    # "/metrics": make_wsgi_app()
})
