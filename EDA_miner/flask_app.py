"""
Flask app handling the home page and redirection.
"""

from flask import Flask, redirect, render_template, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from users_mgt import User, update_password
from forms import LoginForm, ChangePassword, ResetPassword, ForgotPassword
from flask_mail import Message
from app_extensions import mail, redis_conn
from uuid import uuid4


flask_app = Flask(__name__)


@flask_app.route("/")
def index():
    return render_template("base.html")


@flask_app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)

                return redirect(f"/user/{username}")

    return render_template("login.html", form=form)


@flask_app.route("/user/<string:username>/")
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template("profile.html", user=user)


@flask_app.route("/logout/")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect("/")

    return redirect("/login")


@flask_app.route("/change_password/", methods=["GET", "POST"])
@login_required
def change_password():
    username = current_user.username
    user = User.query.filter_by(username=username).first()

    form = ChangePassword()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        if (user and (check_password_hash(user.password, old_password)
                 and (new_password == confirm_password))):

            update_password(user_id=user.id,
                            password=generate_password_hash(new_password))

            return redirect(f"/user/{username}")

    return render_template("change_password.html", form=form)


@flask_app.route("/forgot_password/", methods=["GET", "POST"])
def forgot_password():

    form = ForgotPassword()

    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data

        # Get the user, and if they exist get the email from the database
        user = User.query.filter_by(username=username).first()
        if user:
            email = user.email

            # Generate random key / url for password change
            random_key = str(uuid4())

            # Store the key for the username to Redis with 24hr expiration
            redis_conn.set(f"reset_{username}", random_key, ex=24*60*60)

            # Create and the email
            msg = Message("EDA Miner: Password reset", recipients=[email])
            msg.html = ("To create a new password visit (within 24 hours)"
                        f" <a href='http://127.0.0.1:8000/forgot_password"
                        f"/{username}/{random_key}'>this page</href>.")
            mail.send(msg)

        return "We've sent you the email. Go to <a href='/'>home</a>?"

    else:
        return render_template("forgot_password.html", form=form)


@flask_app.route("/forgot_password/<string:username>/<string:random_key>/",
                 methods=["GET", "POST"])
def reset_password(username, random_key):
    form = ResetPassword()
    stored_key = redis_conn.get(f"reset_{username}")
    user = User.query.filter_by(username=username).first()

    if stored_key is not None:
        # Data are stored as bytes in Redis
        stored_key = stored_key.decode()
        if (stored_key != random_key) or (not user):
            return "Something went wrong. Key expired?"

    if request.method == "GET":
        return render_template("reset_password.html", form=form)

    else:
        if form.validate_on_submit():
            new_password = form.new_password.data
            confirm_password = form.confirm_password.data

            if new_password == confirm_password:

                # Update the password and log the user in
                update_password(user_id=user.id,
                                password=generate_password_hash(new_password))
                login_user(user)

                # Delete the key
                redis_conn.delete(f"reset_{username}")

                return redirect(f"/user/{username}")

        return "Something went wrong. Not matching passwords?"


@flask_app.route("/presentation/show/")
def show_presentation():
    graph_links = [f"/graphs/{graph}" for graph in range(1, 4)
                   ] + ["/graphs/admin_figure_three_vars"]

    return render_template("show_presentation.html", graph_links=graph_links)


@flask_app.route("/presentation/create/")
def create_presentation():
    return render_template("create_presentation.html")
