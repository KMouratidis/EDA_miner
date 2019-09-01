"""
This module is responsible for defining actions/helpers for user management.
"""

import config  # LGTM [py/unused-import]
from werkzeug.security import generate_password_hash
from models import db, User


def add_user(username, password, email):
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

    new_user = User(username=username, password=hashed_password, email=email)
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
