"""
    This module is only here because of the Dash app spanning multiple files.
    General configurations of the underlying app and server go here.

    DO NOT MODIFY WITHOUT PERSMISSION!
"""

from dash import Dash
import dash_bootstrap_components as dbc


DEBUG = True


external_stylesheets = ["https://use.fontawesome.com/releases/v5.8.1/css/all.css",
                        "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"]


app = Dash(__name__, external_stylesheets=external_stylesheets)

# Only to be used in production, safely ignore for now
server = app.server

# Any other configurations for the Dash/Flask server go here
app.config['suppress_callback_exceptions'] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>

        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

        {%metas%}
        <title>EDA Miner</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div class="app0">{%app_entry%}</div>

        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
