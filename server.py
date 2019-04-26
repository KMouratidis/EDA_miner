"""
This module is only here because of the Dash app spanning multiple files.
General configurations of the underlying app and server go here as well.

Global Variables:
    - server: The underlying Flask server, probably needed only for \
              deployment.
    - app: The Dash server, imported everywhere that a dash callback \
           needs to be defined.

Notes to others:
    DO NOT MODIFY WITHOUT PERMISSION! These settings should rarely be
    tampered with, if at all.
"""

from dash import Dash

