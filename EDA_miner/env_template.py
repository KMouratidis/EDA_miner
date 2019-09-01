# This used to be a hidden file with configurations that were passed
# to the environment. Using dotenv was harder for me: finding the
# current dir and adding it to the path below without shell expansions
# (e.g. without something like "$(pwd)"), also for passing said path when
# already configured (e.g. in TravisCI), and finally all of these, including
# docker testing and passing & handling environment variables there.

import os

top_level_dir = os.path.abspath(os.curdir)

var_configs = {
    'MAIL_USERNAME': "admin@example.com",
    'MAIL_PASSWORD': "************",
    'DATABASE_URI': f"sqlite:///{top_level_dir}/users.db",
    'MODE': "TEST",

    'GOOGLE_CLIENT_ID': "************",
    'GOOGLE_PROJECT_ID': "************",
    'GOOGLE_AUTH_URI': "https://accounts.google.com/o/oauth2/auth",
    'GOOGLE_TOKEN_URI': "https://oauth2.googleapis.com/token",
    'GOOGLE_AUTH_PROVIDER': "https://www.googleapis.com/oauth2/v1/certs",
    'GOOGLE_CLIENT_SECRET': "************"
}
