"""
This module collects / defines the various models. It also initializes the \
login manager since if we were to put it into app_extensions it would cause \
circular dependencies (or we would have to take our User model code there).
"""

import dash_core_components as dcc
from flask import current_app, redirect, request
from flask_login import UserMixin, LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the database extension
db = SQLAlchemy()


class User(db.Model, UserMixin):
    """
    ORM class for the user.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)


# Initialize the login manager extension
login_manager = LoginManager()
login_manager.login_view = '/login'


@login_manager.user_loader
def load_user(user_id):
    """
    Callback to reload the user object (from the docs)
    """
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    """
    The user tries to access a view they are not authorized for. NUKE EM!!

    Returns:
        html or dash elements, essentially a 401
    """

    path = "/login"

    if os.getenv("MODE") in ["DEBUG", "DEV"]:
        user = User.query.filter_by(username="admin").first()
        login_user(user)
        path = "/"

    if current_app.name.startswith("flask"):
        # TODO: Return a 401 or something
        return redirect(path)

    else:
        # If it is a dash app, you can write Dash here.
        # This one "redirects" (sets the url)
        return dcc.Location(id="go_login", pathname=path)
