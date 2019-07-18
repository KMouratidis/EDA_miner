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

from server import app
from utils import parse_contents



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
               State('upload_data_button', 'last_modified'),
               State("user_id", "children")])
def parse_uploads(list_of_contents, list_of_names,
                  list_of_dates, user_id):
    """
    Load and store the uploaded data.

    Args:
        list_of_contents (list(bytes)): The file contents that need to \
                                        be parsed.
        list_of_names (list(str)): The original filenames.
        list_of_dates (list(str)): The modification (?) dates of files.
        user_id (str): Session/user id.

    Returns:
        list: A list of dash components.
    """


    # TODO: Handle initial schema here
    if list_of_contents is not None:
        response = [parse_contents(c, n, d, user_id) for c, n, d
                    in zip(list_of_contents, list_of_names, list_of_dates)]

        return response
