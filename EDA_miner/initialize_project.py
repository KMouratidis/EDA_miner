"""
A dummy script to generate the database, a dummy user, and do any other \
initialization action needed to fire up the project.
"""

from users_mgt import add_user
from wsgi import flask_app, db
from config import env_config_get
import os


if __name__ == "__main__":
    if not os.path.exists("users.db"):
        with flask_app.app_context() as ctx:
            # Create the database
            db.create_all()

            # Add dummy users
            add_user("admin", "admin", env_config_get("MAIL_USERNAME"))
            add_user("example", "example", "example@example.com")
