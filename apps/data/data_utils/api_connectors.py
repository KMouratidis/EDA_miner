"""
This module collects the layouts for connecting to the various APIs.

Functions:
    - twitter_connect: Connect to the Twitter API.
    - google_sheets_connect: Connect to the Google Sheets API.
    - reddit_connect: Connect to the Reddit API.
    - spotify_connect: Connect to the Spotify API.

Notes to others:
    You should probably not write code here, unless adding
    a new API connection (or improving existing ones).
"""

from utils import r

import twitter
import praw
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import spotipy
from spotipy import util
import pandas as pd
import pickle


def spotify_connect(client_id, client_secret, user_id):
    """Connect to Spotify and store the handle in Redis."""

    creds = util.oauth2.SpotifyClientCredentials(client_id, client_secret)
    token = creds.get_access_token()

    spotify = spotipy.Spotify(auth=token)

    r.set(f"{user_id}_spotify_api", "true")
    r.set(f"{user_id}_spotify_api_handle", pickle.dumps(spotify))


def reddit_connect(client_id, client_secret, user_id):
    """Connect to Reddit and store the handle in Redis."""

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent='EDA miner')

    r.set(f"{user_id}_reddit_api", "true")
    r.set(f"{user_id}_reddit_api_handle", pickle.dumps(reddit))


def twitter_connect(key, secret_key, access_token, access_token_secret,
                    user_id, sleep_on_rate_limit=True):
    """Connect to Twitter API and store the handle in Redis."""

    api = twitter.Api(consumer_key=key,
                      consumer_secret=secret_key,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret,
                      sleep_on_rate_limit=sleep_on_rate_limit)
    api.VerifyCredentials()

    r.set(f"{user_id}_twitter_api", "true")
    # store the api object to redis so it
    # can be used in other parts
    r.set(f"{user_id}_twitter_api_handle", pickle.dumps(api))


def google_sheets_connect(credentials_file, gspread_key, user_id):
    """Connect to Google Sheets and store the data in Redis."""

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # load credentials from file
    credentials = (ServiceAccountCredentials
                   .from_json_keyfile_name(credentials_file, scope))
    # create an interface to google
    gc = gspread.authorize(credentials)

    # connect to a certain spreadsheet, using it's key
    # e.g. full address: https://docs.google.com/spreadsheets/d/1802UymlFPQE2uvk_T8XI3kX1kWniYOngS6sQSnXoe2U/
    # remember to either allow the service account's email (see the
    # authorization .json file) to access the spreadsheet or to allow
    # access to everyone who has a link (or both)
    spreadsheet = gc.open_by_key(gspread_key)
    ws = spreadsheet.get_worksheet(0)

    data = ws.get_all_values()
    data = pd.DataFrame(data[1:], columns=data[0])

    r.set(f"{user_id}_gsheets_api", "true")
    # TODO: Investigate and store the other components
    r.set(f"{user_id}_gsheets_api_data", pickle.dumps(data))


def facebook_connect():
    raise NotImplementedError


def google_docs_connect():
    raise NotImplementedError
