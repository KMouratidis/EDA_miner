"""
A dummy script to generate the database, a dummy user, and do any other \
initialization action needed to fire up the project.
"""

from users_mgt import add_user, permit_user_app
from flask_app import flask_app
from config import env_config_get, config
from app_extensions import db
import os


if __name__ == "__main__":
    if os.path.exists("users.db"):
        os.remove("users.db")

    flask_app.config.update(config)
    db.init_app(flask_app)
    with flask_app.app_context() as ctx:
        # Create the database
        db.create_all()

        # Add dummy users
        add_user(username="admin", password="admin", superuser=True,
                         email=env_config_get("MAIL_USERNAME"))
        add_user(username="example", password="example",
                           superuser=False, email="example@example.com")

        # Allow admin to use all apps
        permit_user_app("admin", "data")
        permit_user_app("admin", "visualization")
        permit_user_app("admin", "modeling")

        # Allow example to use only two apps
        permit_user_app("example", "data")
        permit_user_app("example", "visualization")
