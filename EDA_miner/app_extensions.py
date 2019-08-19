"""
Use this module to collect all the extensions used. These can be defined in \
other modules, but do import them here and then from here to `wsgi.py`.
"""

from models import db, login_manager  # LGTM [py/unused-import]
from flask_mail import Mail
from redis import Redis


# Initialize the mail extension
mail = Mail()

# A connection to the Redis database, for various purposes
redis_conn = Redis()
