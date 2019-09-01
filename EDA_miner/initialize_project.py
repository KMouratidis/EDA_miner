"""
A dummy script to generate the database, a dummy user, and do any other \
initialization action needed to fire up the project.
"""

from users_mgt import add_user
from flask_app import flask_app
from config import env_config_get, config
from app_extensions import db
import os


if __name__ == "__main__":
    if not os.path.exists("users.db"):

        flask_app.config.update(config)
        db.init_app(flask_app)
        with flask_app.app_context() as ctx:
            # Create the database
            db.create_all()

            # Add dummy users
            add_user("admin", "admin", env_config_get("MAIL_USERNAME"))
            add_user("example", "example", "example@example.com")
