"""
This module is for loading and creating application-wide configurations.
"""

import os
from sqlalchemy import create_engine
from dotenv import load_dotenv


# Load the sensitive configuration from the .env file
load_dotenv()

CURRENT_DIR = os.path.dirname(__file__)

# Create a connection to the database
engine = create_engine(os.getenv("DATABASE_URI"))

# Secret key for user sessions
# https://stackoverflow.com/a/42579388/6655150
SECRET_KEY = os.urandom(16)

config = {
    # Database & session configuration for the apps
    "SECRET_KEY": SECRET_KEY,
    "SQLALCHEMY_DATABASE_URI": os.getenv("DATABASE_URI"),
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,

    # Mail server configuration
    "MAIL_SERVER": "smtp.live.com",
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USERNAME": os.getenv("MAIL_USERNAME"),
    "MAIL_PASSWORD": os.getenv("MAIL_PASSWORD"),
    "MAIL_DEFAULT_SENDER": os.getenv("MAIL_USERNAME"),
}

client_config = {
    "installed": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
        "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
    }
}

MODE = os.getenv("MODE")
if MODE == "DEBUG":

    # These are good for development so CSS is not saved,
    # but not for production, I guess.
    config.update({
        "TEMPLATES_AUTO_RELOAD": True,
        "SEND_FILE_MAX_AGE_DEFAULT": 0,
    })