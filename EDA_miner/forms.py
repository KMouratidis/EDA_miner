"""
This module collects the forms of the site that need at least some degree \
of serious implementation (e.g. for security concerns), like the logins. \
Even if you can, don't try to create forms for Dash forms; unless you are \
also willing to teach us :)
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.fields.html5 import EmailField


# TODO: Correct / improve / revise forms

class LoginForm(FlaskForm):
    """
    Login form for the main flask app.
    """

    username = StringField("Username", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])

    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    """
    Register form for the main flask app. Currently not used. May only be \
    used for creating an admin panel.
    """

    username = StringField("Username", validators=[validators.DataRequired()])
    email = EmailField("Email", validators=[validators.Email(),
                                            validators.DataRequired()])

    password = PasswordField("Password", validators=[validators.DataRequired()])
    confirm_password = PasswordField("Confirm password",
                                     validators=[validators.DataRequired()])

    submit = SubmitField('Sign In')


class ResetPassword(FlaskForm):
    """
    Reset password after receiving a randomized URL.
    """

    new_password = PasswordField("New Password",
                                 validators=[validators.DataRequired()])
    confirm_password = PasswordField("Confirm password",
                                     validators=[validators.DataRequired()])

    submit = SubmitField('Change!')


class ChangePassword(ResetPassword):
    """
    Change password form for the main flask app.
    """

    old_password = PasswordField("Old password",
                                 validators=[validators.DataRequired()])

    # Inherited: new_password, confirm_password, submit


class ForgotPassword(FlaskForm):
    """
    Request the reset of password form for the main flask app.
    """

    username = StringField("Username", validators=[validators.DataRequired()])
    submit = SubmitField('Send link')
