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

from utils import r

import twitter
import praw
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import spotipy
from spotipy import util
import pickle
import quandl


def twitter_connect(consumer_key, consumer_secret, access_token_key,
                    access_token_secret, *, sleep_on_rate_limit=True):
    """
    Connect to Twitter API and store the handle in Redis.
    """

    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret,
                      sleep_on_rate_limit=sleep_on_rate_limit)
    api.VerifyCredentials()

    return api


def google_sheets_connect(credentials_file, gspread_key):
    """
    Connect to Google Sheets and store the data in Redis.
    """

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

    # ws = spreadsheet.get_worksheet(0)
    # TODO: Investigate and store the other components
    # data = ws.get_all_values()
    # data = pd.DataFrame(data[1:], columns=data[0])

    # Here the api handle is both the gc instance and the spreadsheet
    return [gc, spreadsheet]


def reddit_connect(client_id, client_secret):
    """
    Connect to Reddit and store the handle in Redis.
    """

    return praw.Reddit(client_id=client_id,
                       client_secret=client_secret,
                       user_agent='EDA miner')


def spotify_connect(client_id, client_secret):
    """
    Connect to Spotify and store the handle in Redis.
    """

    creds = util.oauth2.SpotifyClientCredentials(client_id, client_secret)
    token = creds.get_access_token()

    return spotipy.Spotify(auth=token)


def quandl_connect(api_key):
    quandl.ApiConfig.api_key = api_key

    # Not actually a handle, but can be used to get data.
    return quandl.get


def facebook_connect():
    raise NotImplementedError


def google_docs_connect():
    raise NotImplementedError


connectors_mapping = {
    "spotify": spotify_connect,
    "reddit": reddit_connect,
    "twitter": twitter_connect,
    "gsheets": google_sheets_connect,
    "quandl": quandl_connect,
}


# A function that serves as the frontend to all others
def api_connect(api_choice, user_id, *args, **kwargs):

    if any(x is None for x in args):
        return False

    func = connectors_mapping[api_choice]

    try:
        api_handle = func(*args, **kwargs)

        # Store in Redis that the API connected, and its handle(s)
        r.set(f"{user_id}_{api_choice}_api", "true")
        r.set(f"{user_id}_{api_choice}_api_handle", pickle.dumps(api_handle))

        return True

    except Exception as e:
        print(e)
        return False