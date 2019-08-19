"""
This module is only here because of the Dash app spanning multiple files. \
General configurations of the underlying app and server go here as well.

Global Variables:
    - app: The Dash server, imported everywhere that a dash callback \
           needs to be defined.
    - r: The connection to Redis.
"""

from dash import Dash
from redis import Redis


redis_conn = Redis()

app = Dash(__name__, requests_pathname_prefix="/modeling/",
           assets_external_path="http://127.0.0.1:8000/static/")

app.config["suppress_callback_exceptions"] = True
