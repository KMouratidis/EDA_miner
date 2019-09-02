"""
This module is responsible for defining actions/helpers for user management.
"""

from uuid import uuid4
import config  # LGTM [py/unused-import]
from werkzeug.security import generate_password_hash
from models import db, User, UserApps


def add_user(username, password, email, superuser=False):
    """
    Create new user in the database.

    Args:
        username (str): User name. Case-sensitive & unique.
        password (str): User password. Ensure strength during registration.
        email (str): A validated email address.

    Returns:
        None
    """

    hashed_password = generate_password_hash(password, method='sha256')
    api_token = str(uuid4())

    new_user = User(username=username, password=hashed_password,
                    email=email, superuser=superuser,
                    api_token=api_token)
    db.session.add(new_user)
    db.session.commit()


def del_user(username):
    """
    Delete a user from the database.

    Args:
        username (str): User name. Does not handle logic.

    Returns:
        None
    """

    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()


def show_users():
    """
    Prints the list of available users.

    Returns:
        None
    """

    users = User.query.all()
    for user in users:
        print(f"{user.username} ({user.email})")


def update_password(user_id, password):
    """
    Update the password for the specified user.

    Args:
        user_id (int): The user id, as in the database.
        password (str): The HASHED password.

    Returns:
        None
    """

    user = User.query.get(user_id)
    user.password = password
    db.session.commit()


def verify_email(username, activation_key, stored_key):
    stored_key = stored_key.decode()
    user = User.query.filter_by(username=username).first()

    if activation_key == stored_key:
        user.verified_email = 1
        db.session.commit()
        return True, user

    else:
        return False, user


def permit_user_app(username, app_name):
    """
    Allow user to access an app.
    """

    user = User.query.filter_by(username=username).first()
    new_app = UserApps(user_id=user.id, app_name=app_name)
    db.session.add(new_app)
    db.session.commit()


def show_apps(user):
    apps = UserApps.query.filter_by(user_id=user.id).all()
    apps = [app.app_name for app in apps]

    return apps
