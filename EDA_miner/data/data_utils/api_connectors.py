"""
This module collects the layouts for connecting to the various APIs.

Functions:
    - twitter_connect: Connect to the Twitter API.
    - google_sheets_connect: Connect to the Google Sheets API.
    - reddit_connect: Connect to the Reddit API.
    - spotify_connect: Connect to the Spotify API.

Notes to others:
    You should probably not write code here, unless adding \
    a new API connection (or improving existing ones).
"""

from ..server import redis_conn
from .api_layouts import TwitterAPI, GSheetsAPI, RedditAPI, QuandlAPI
from .api_layouts import SpotifyAPI, GAnalyticsAPI

import dill
from flask_login import current_user


connectors_mapping = {
    "twitter": TwitterAPI,
    "gsheets": GSheetsAPI,
    "reddit": RedditAPI,
    "quandl": QuandlAPI,
    "spotify": SpotifyAPI,
    "ganalytics": GAnalyticsAPI,
}


def api_connect(api_choice, *args, **kwargs):
    """
    Connect to the selected API. A function that serves as the front \
    end to all others, abstracting them away. ALso stores the API \
    handle in Redis for later usage.

    Args:
        api_choice (str): A key in `connectors_mapping`.
        *args: Arguments to be passed to the appropriate API connector.
        **kwargs: Keyword arguments to be passed to the appropriate \
                  API connector.

    Returns:
        bool: Whether everything succeeded or not (an exception was raised).
    """

    user_id = current_user.username

    # Try to get previous connection
    connection = redis_conn.get(f"{user_id}_connection_{api_choice}")
    if connection is None:
        # If there is none, create a new one
        connection = connectors_mapping[api_choice](user_id)

        try:
            connection.connect(*args, **kwargs)

            # Store in Redis that the API connected, and the connection
            redis_conn.set(f"{user_id}_hasconnected_{api_choice}", "true",
                           ex=24*60*60)
            redis_conn.set(f"{user_id}_connection_{api_choice}",
                           dill.dumps(connection),
                           ex=24*60*60)

        except Exception as e:
            print(e)

    else:
        # Otherwise, load it
        connection = dill.loads(connection)

    return connection
