"""
This module collects / defines the various models. It also initializes the \
login manager since if we were to put it into app_extensions it would cause \
circular dependencies (or we would have to take our User model code there).
"""

import dash_core_components as dcc
from flask import current_app, redirect, g
from flask_login import UserMixin, LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy
from config import env_config_get
from sqlalchemy.orm import validates


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
    superuser = db.Column(db.Boolean, nullable=False, default=False)
    api_token = db.Column(db.String(36), nullable=False, unique=True)
    verified_email = db.Column(db.Boolean, nullable=False, default=False)

    # Connections to other models
    user_apps = db.relationship('UserApps', backref='user', lazy=True)

    # Connections to other models
    data_schemas = db.relationship('DataSchemas', backref='user', lazy=True)


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

    if env_config_get("MODE") in ["DEBUG", "DEV"]:
        user = User.query.filter_by(username="admin").first()
        login_user(user)
        path = "/"

    if current_app.name.startswith("flask"):
        # TODO: Return a 401 or something
        return redirect(path)

    else:
        # If it is a dash app, you can write Dash here.
        # This one "redirects" (sets the url). We return
        # Two items because some callbacks expect an item
        # for the side-navbar.
        return dcc.Location(id="go_login", pathname=path), []


class DataSchemas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime)

    # a dictionary consisting of 2 dictionaries and a pandas.DataFrame
    schema = db.Column(db.PickleType)

    # The schema can be either the auto-inferred one (e.g. heuristics)
    # or it can be the user-modified one. Annotate appropriately, and
    # perform validation.
    schema_status = db.Column(db.String(20))

    @validates('schema_status')
    def validate_schema_status(self, _, value):
        assert value in ["inferred", "ground_truth"]
        return value


class UserApps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    app_name = db.Column(db.String(50), nullable=False)

    # Create a line for every app a user is permitted to use.
    # Each user may
    __table_args__ = (
        db.UniqueConstraint('user_id', 'app_name', name='one_line_per_app'),
    )
