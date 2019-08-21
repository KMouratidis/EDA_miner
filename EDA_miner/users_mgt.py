"""
This module is responsible for creating the database storing the users, \
and defining actions for user management.
"""

import os
import config
from sqlalchemy.sql import select
from werkzeug.security import generate_password_hash
from config import engine, env_config_get
from models import db, User


User_table = db.Table('user', User.metadata)


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

    ins = User_table.insert().values(
        username=username, password=hashed_password, email=email)

    conn = engine.connect()
    conn.execute(ins)
    conn.close()


def del_user(username):
    """
    Delete a user from the database.

    Args:
        username (str): User name. Does not handle logic.

    Returns:
        None
    """

    delete = User_table.delete().where(User_table.c.username == username)

    conn = engine.connect()
    conn.execute(delete)
    conn.close()


def show_users():
    """
    Prints the list of available users.

    Returns:
        None
    """

    select_st = select([User_table.c.username, User_table.c.email])

    conn = engine.connect()
    rs = conn.execute(select_st)

    for row in rs:
        print(row)

    conn.close()


def update_password(user_id, password):
    """
    Update the password for the specified user.

    Args:
        user_id (int): The user id, as in the database.
        password (str): The HASHED password.

    Returns:
        None
    """

    update = (User_table.update().where(User_table.c.id == 1)
              .values(password=password))

    conn = engine.connect()
    conn.execute(update)
    conn.close()


if __name__ == "__main__":
    # Create the user
    if not os.path.exists("users.db"):
        User.metadata.create_all(engine)
        add_user("admin", "admin", env_config_get("MAIL_USERNAME"))
