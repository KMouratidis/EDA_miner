"""
    This module provides an interface for uploading and
    handling of files.

    You should probably not write code here, unless you
    mean to implement new filetype uploads or other types
    of upload handling (i.e. multi-file uploads).
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from server import app
import styles
from utils import parse_contents

Upload_Options = [
    dcc.Upload(
        id='upload_data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]), style=styles.upload_button(),
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
]


# TODO: Any inconsistency rises from the fact
# that the guide was meant for multiple-file uploads
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload_data', 'contents'),],
              [State('upload_data', 'filename'),
               State('upload_data', 'last_modified'),
               State("user_id", "children")])
def parse_uploads(list_of_contents, list_of_names,
                  list_of_dates, user_id):

    if list_of_contents is not None:
        response = [parse_contents(c, n, d, user_id) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]

        return response
