"""
This module is for loading and creating application-wide configurations.
"""

import os
from sqlalchemy import create_engine


CURRENT_DIR = os.path.dirname(__file__)

if os.path.exists("env.py"):
    # If the env file exists, load it
    import env
    env_config_get = env.var_configs.get

elif os.environ.get("DATABASE_URI") is not None:
    # If not, try to get the variables from the environment
    # by first testing if at least one of them is defined
    env_config_get = os.environ.get

else:
    # Else, get the dummy values from the template
    import env_template
    env_config_get = env_template.var_configs.get

# Create a connection to the database
engine = create_engine(env_config_get("DATABASE_URI"))

# Secret key for user sessions
# https://stackoverflow.com/a/42579388/6655150
SECRET_KEY = os.urandom(16)

config = {
    # Database & session configuration for the apps
    "SECRET_KEY": SECRET_KEY,
    "SQLALCHEMY_DATABASE_URI": env_config_get("DATABASE_URI"),
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,

    # Mail server configuration
    "MAIL_SERVER": "smtp.live.com",
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USERNAME": env_config_get("MAIL_USERNAME"),
    "MAIL_PASSWORD": env_config_get("MAIL_PASSWORD"),
    "MAIL_DEFAULT_SENDER": env_config_get("MAIL_USERNAME"),
}

client_config = {
    "installed": {
        "client_id": env_config_get("GOOGLE_CLIENT_ID"),
        "project_id": env_config_get("GOOGLE_PROJECT_ID"),
        "auth_uri": env_config_get("GOOGLE_AUTH_URI"),
        "token_uri": env_config_get("GOOGLE_TOKEN_URI"),
        "auth_provider_x509_cert_url": env_config_get("GOOGLE_AUTH_PROVIDER"),
        "client_secret": env_config_get("GOOGLE_CLIENT_SECRET"),
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
    }
}


if env_config_get("MODE") in ["DEBUG", "DEV"]:

    # These are good for development so CSS is not saved,
    # but not for production, I guess.
    config.update({
        "TEMPLATES_AUTO_RELOAD": True,
        "SEND_FILE_MAX_AGE_DEFAULT": 0,
    })
