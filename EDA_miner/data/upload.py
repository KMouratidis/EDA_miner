"""
This module provides an interface for uploading and handling of files.

Global Variables:
    - Upload_Options: Generate the layout for uploading datasets.

Dash callbacks:
    - parse_uploads: Load and store the uploaded data.

Notes to others:
    You should probably not write code here, unless you mean to \
    implement new filetype uploads or other types of upload handling, \
    or other similar functionality.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from .server import app, redis_conn
from utils import parse_contents

from flask_login import current_user


Upload_Options = [
    html.A(dcc.Upload(
        id='upload_data_button',
        children=html.Div([
            html.I(className="fas fa-upload"),
            '  Drag and Drop or Select Files'
        ]),
        # Allow multiple files to be uploaded
        multiple=True
    )),
    html.Div(id='output-data-upload'),
]


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload_data_button', 'contents')],
              [State('upload_data_button', 'filename'),
               State('upload_data_button', 'last_modified')])
def parse_uploads(list_of_contents, list_of_names,
                  list_of_dates):
    """
    Load and store the uploaded data.

    Args:
        list_of_contents (list(bytes)): The file contents that need to \
                                        be parsed.
        list_of_names (list(str)): The original filenames.
        list_of_dates (list(str)): The modification (?) dates of files.

    Returns:
        list: A list of dash components.
    """

    user_id = current_user.username

    if list_of_contents is not None:
        response = [parse_contents(contents=c, filename=n, date=d,
                                   user_id=user_id, redis_conn=redis_conn)
                    for c, n, d in zip(list_of_contents, list_of_names,
                                       list_of_dates)]

        return response
