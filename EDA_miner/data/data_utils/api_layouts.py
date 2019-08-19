"""
This module collects the layouts for connecting to the various APIs.

Functions:
    - success_message: Notify the user for successful connection.

Global variables:
    - twitter_layout: 4 input fields and a button.
    - gsheets_layout: 2 input fields and a button.
    - reddit_layout: 2 input fields and a button.
    - quandl_layout: 2 input fields and a button.
    - spotify_layout: 2 input fields and a button.

Notes to others:
    You should probably not write code here, unless adding \
    a new API connection.

    IMPORTANT: When designing layouts ALWAYS pre-append the input \
    elements with the API name, and ALWAYS name each input id \
    according to the names of the variables of the respective API \
    connector.
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

import dash_bootstrap_components as dbc

from ..server import redis_conn, cache
from .schema_heuristics import infer_types
from .ganalytics_metrics import all_metrics
from utils import create_table, save_schema
from config import client_config
from exceptions import UnexpectedResponse

import twitter
import praw
from spotipy import util, Spotify
import quandl
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from collections import defaultdict
import requests
import dill
import pandas as pd


def success_message(api):
    """
    Utility to provide feedback on successful connections.

    Args:
        api (str): Name / key of the API.

    Returns:
        list: A list of Dash elements.
    """

    return [
        html.H4(f"Successfully connected to the {api} API."),
        html.Br(),
    ]


# Abstract base class
class APIConnection:

    # Name for Redis keys (e.g. to store data with the key schema:
    # f"{self.user_id}_data_{self.api_name}_{key}"
    api_name = "generic_API"
    # Label for tabs / dropdowns
    label = "API"

    def __init__(self, user_id=None):
        self.state = "login"
        self.user_id = user_id
        self.api = None

    def save_data_and_schema(self, df, key, take_sample=True, ex=None):
        """
        Helper to infer schema and save the it along with the data.

        Args:
            df (`pd.DataFrame`): The data to save.
            key (str): The name of the dataset (subreddit, twitter account \
                       quandl tag, etc).
            take_sample (bool): Whether to sample the data or not.
            ex (int): In how many seconds to expire the data (given to Redis).

        Returns:
            None
        """

        redis_kwargs = {}
        if ex is not None:
            redis_kwargs["ex"] = ex

        # Take a sample, infer and save the schema
        sample = df.sample(n=50, replace=True) if take_sample else df

        # Infer types.
        types, subtypes = infer_types(sample, is_sample=True)

        # Save the data and schema
        redis_conn.set(f"{self.user_id}_data_{self.api_name}_{key}",
                       dill.dumps(df))
        save_schema(f"{self.user_id}_schema_{self.api_name}_{key}",
                    types=types, subtypes=subtypes,
                    head=df.head(), redis_conn=redis_conn,
                    redis_kwargs=redis_kwargs)

    def render_layout(self):
        if self.state == "login":
            return self.login_layout

        elif self.state == "authenticated":
            return self.success_layout

        else:
            return [html.Div("Unknown state, something went wrong")]

    def connect(self, *args, **kwargs):
        """
        Connect, save the API object, and change state.
        """
        raise NotImplementedError

    def fetch_data(self, *args, **kwargs):
        """
        Get data and return a preview
        """
        raise NotImplementedError

    @property
    def login_layout(self):
        """
        Create a Dash layout for accepting credentials for login.
        """

        raise NotImplementedError

    @property
    def success_layout(self):
        """
        Create a Dash layout after a successful login, and a menu \
        to fetch data.
        """

        raise NotImplementedError

    @staticmethod
    def pretty_print(df):
        """
        Display the sample in a appealing manner, given a DataFrame. \
        This is only displayed prettily here, the `view` module only \
        shows tables.
        """

        raise NotImplementedError


class TwitterAPI(APIConnection):

    api_name = "twitter"
    label = "Twitter"

    def connect(self, consumer_key, consumer_secret, access_token_key,
                access_token_secret, *, sleep_on_rate_limit=True):
        """
        Connect to Twitter API.
        """

        api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_token_key,
                          access_token_secret=access_token_secret,
                          sleep_on_rate_limit=sleep_on_rate_limit)
        api.VerifyCredentials()

        self.api = api
        self.state = "authenticated"

    @cache.memoize(10*60)
    def fetch_data(self, acc_name):
        """
        Get tweets by the specified user.

        Args:
            acc_name (str): The account name / handle from Twitter.

        Returns:
            `pd.DataFrame`: A sample of the fetched data.
        """

        query = self.api.GetUserTimeline(screen_name=acc_name)
        tweets = [str(status.text) for status in query]

        # Create a DataFrame, take a sample
        df = pd.DataFrame(tweets, columns=["tweets"])

        # TODO: These are data that can easily be stored in
        #       an SQL database with columns:
        #       (user_id, acc_name, tweet, ...)
        #       We can use Redis to only keep the most recent.
        #       Expiring them is only temporary.
        # Infer and save the schema & data
        self.save_data_and_schema(df, key=acc_name, ex=24*60*60)

        return df.head()

    @property
    def login_layout(self):
        """
        Create a Dash layout for accepting credentials for login.
        """

        return [
            html.Div(id="twitter_login_form", children=[
                html.H5("Consumer key"),
                dcc.Input(id="twitter_consumer_key", type="text"),

                html.H5("Consumer Secret"),
                dcc.Input(id="twitter_consumer_secret", type="text"),

                html.H5("Access Token"),
                dcc.Input(id="twitter_access_token_key", type="text"),

                html.H5("Access Token Secret"),
                dcc.Input(id="twitter_access_token_secret", type="text"),

                html.Button("Connect!", id="twitter_connect_button",
                            style={"display": "inline"}, n_clicks=0),
            ]),

            html.Div(id="twitter_UI"),
        ]

    @property
    def success_layout(self):
        """
        Create a Dash layout after a successful login, and a menu \
        to fetch data.
        """

        return [
            html.Br(),
            dcc.Input(id="twitter_acc_name", placeholder="Enter a twitter handle name"),
            html.Button("Fetch tweets!", id="get_twitter", n_clicks=0),
            html.Div(id="twitter_results"),
        ]

    @staticmethod
    def pretty_print(df):
        """
        Display the sample in a appealing manner, given a DataFrame. \
        This is only displayed prettily here, the `view` module only \
        shows tables.
        """

        return [html.P(tweet) for (i, tweet) in df.iterrows()]


class GSheetsAPI(APIConnection):

    api_name = "gsheets"
    label = "Google Sheets"

    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Each key/list will hold one file and all its sheets.
        # The user might import many files, with many sheets each.
        self.sheets = defaultdict(list)

    def connect(self):
        """
        Connect to Google Sheets API.
        """

        # Opens a new tab that goes to Google, the user agrees to grant
        # permissions, and Google returns credentials
        self.credentials = GSheetsAPI.flow.run_local_server(port=0)
        # Build a service / API instance
        self.api = build("sheets", "v4", credentials=self.credentials)

        self.state = "authenticated"

    @cache.memoize(30 * 60)
    def fetch_data(self, gspread_key):
        """
        Connect to a certain spreadsheet, and get all its sheets using \
        it's key e.g. full address: \
        https://docs.google.com/spreadsheets/d/1802UymlFPQE2uvk_T8XI3kX1kWniYOngS6sQSnXoe2U/ \
        You might need to change file permissions.

        Args:
            gspread_key (str): The ID of the spreadhseet to fetch.

        Returns:
            `pd.DataFrame`: A sample of the fetched data.
        """

        # First get the spreadsheet and its metadata (e.g. the name & sheets)
        response = self.api.spreadsheets().get(spreadsheetId=gspread_key).execute()
        title = response["properties"]["title"]
        sheets = [sheet["properties"]["title"] for sheet in response["sheets"]]
        # Save the individual sheets with the document's name as the key
        self.sheets[title] = sheets

        # Iterate in reverse so we can return the first sheet as a sample
        for sheet in self.sheets[title][::-1]:
            response = self.api.spreadsheets().values().get(
                spreadsheetId=gspread_key,
                range=sheet,
                valueRenderOption="UNFORMATTED_VALUE",
                dateTimeRenderOption="FORMATTED_STRING"
            ).execute()

            # TODO: This try/except should be handled by data validation
            #       e.g. see github: frictionlessdata/goodtables-py
            try:
                # Create a DataFrame, and save it
                data = response["values"]
                df = pd.DataFrame(data[1:], columns=data[0])

                # Infer and save the schema & data
                self.save_data_and_schema(df, key=sheet)

            except ValueError as e:
                # E.g. badly formatted data cause
                print(f"Couldn't parse {sheet}'s data. ERROR:", e)

        # Return only the first spreadsheet's head
        return df.head()

    @property
    def login_layout(self):
        """
        Create a Dash layout for accepting credentials for login.
        """

        return [
            html.Div(id="gsheets_login_form", children=[
                html.H5("Authorize via Google"),
                html.Button("Connect!", id="gsheets_connect_button",
                            style={"display": "inline"}, n_clicks=0),
            ]),

            html.Div(id="gsheets_UI"),
        ]

    @property
    def success_layout(self):
        """
        Create a Dash layout after a successful login, and a menu \
        to fetch data.
        """

        return [
            html.H5("Spreadsheet key:"),
            dcc.Input(id="gsheets_gspread_key", type="text"),

            html.Button("Fetch spreadsheet", id="get_gsheets", n_clicks=0),
            html.Div(id="gsheets_results"),
        ]

    @staticmethod
    def pretty_print(df):
        """
        Display the sample in a appealing manner, given a DataFrame. \
        This is only displayed prettily here, the `view` module only \
        shows tables.
        """

        return create_table(df)


class RedditAPI(APIConnection):

    api_name = "reddit"
    label = "Reddit"

    def connect(self, client_id, client_secret):
        """
        Connect to Reddit API.
        """

        self.api = praw.Reddit(client_id=client_id,
                               client_secret=client_secret,
                               user_agent='EDA miner')
        self.state = "authenticated"

    @cache.memoize(15*60)
    def fetch_data(self, subreddit_choice, limit):
        """
        Fetch the `limit` latest posts from the specified subreddit.

        Args:
            subreddit_choice (str): The name of the subreddit to fetch.
            limit (int): How many topics to fetch.

        Returns:
            `pd.DataFrame`: A sample of the fetched data.
        """

        subreddit = self.api.subreddit(subreddit_choice)
        topics = subreddit.hot(limit=limit)

        # Parse the data and create a DataFrame
        data = [[topic.title, topic.permalink, topic.score,
                 topic.author.name, topic.selftext] for topic in topics]
        columns = ["title", "permalink", "score", "author", "text"]
        df = pd.DataFrame(data, columns=columns)

        # Infer and save the schema & data
        self.save_data_and_schema(df, key=subreddit_choice)

        # Return a preview
        return df.head()

    @property
    def login_layout(self):
        """
        Create a Dash layout for accepting credentials for login.
        """

        return [
            html.Div(id="reddit_login_form", children=[
                html.H5("Client id"),
                dcc.Input(id="reddit_client_id", type="text"),

                html.H5("Client secret"),
                dcc.Input(id="reddit_client_secret", type="text"),

                html.Button("Connect!", id="reddit_connect_button",
                            style={"display": "inline"}, n_clicks=0)
            ]),

            html.Div(id="reddit_UI")
        ]

    @property
    def success_layout(self):
        """
        Create a Dash layout after a successful login, and a menu \
        to fetch data.
        """

        return [
            html.H4("Write the name of a subreddit:"),
            dcc.Input(id="reddit_subreddit", type="text", value="",),

            html.H4("How many topics to fetch?"),
            daq.NumericInput(id="reddit_ntopics", value=5),

            html.Button("Gimme dem reddits", id="get_reddit", n_clicks=0),

            html.Br(),
            html.Div(id="reddit_results"),
        ]

    @staticmethod
    def pretty_print(df):
        """
        Display the sample in a appealing manner, given a DataFrame. \
        This is only displayed prettily here, the `view` module only \
        shows tables.
        """

        return [
            html.Div([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4(title),
                        html.A(">> View at reddit", href=permalink),
                    ]),
                    dbc.CardBody([
                        html.H5(f"Written by {author}, "
                                f"score: {score}",
                                className='card-title'),
                        html.P(dcc.Markdown(text),
                               className="card-text"),
                    ]),
                ]),
                html.Br(),
            ]) for i, (title, permalink, score,
                       author, text) in df.iterrows()
        ]


class GAnalyticsAPI(APIConnection):

    api_name = "ganalytics"
    label = "Google Analytics"

    def connect(self, client_email, private_key):
        """
        Connect to a Google Analytics account.
        """

        response = requests.post("http://127.0.0.1:5000/", json={
            "client_email": client_email,
            "user_id": self.user_id,
            "private_key": private_key
        })

        if response.status_code != 201:
            raise UnexpectedResponse("Connection to Google Analytics failed with "
                                     f"status code {response.status_code}")

        # no api to save
        self.state = "authenticated"

    @cache.memoize(5 * 60)
    def fetch_data(self, metrics):
        """
        Fetch Google Analytics (realtime) data for the selected metrics.

        Args:
            metrics (list(str)): The metrics to fetch, e.g.: pageviews.

        Returns:
            `pd.DataFrame`: A sample of the fetched data.
        """

        if not isinstance(metrics, list):
            metrics = [metrics]

        # Drop the first three characters:
        # "ga:pageviews" -> pageviews
        metrics = [metric[3:] if ":" in metric else metric
                   for metric in metrics]
        # Ask the ganalytics service to fetch the user's metrics
        response = requests.get(f"http://127.0.0.1:5000/"
                                f"{self.user_id}/{','.join(metrics)}")

        # Parse the results, create a DataFrame, and store it in Redis
        samples = []
        results = response.json()
        for metric in metrics:
            df = pd.DataFrame(results["data"][metric], columns=[metric])

            # Infer and save the schema & data
            self.save_data_and_schema(df, key=metric)

            samples.append(results["data"][metric][:5])

        samples = pd.DataFrame(samples, index=metrics).T
        return samples

    @property
    def login_layout(self):
        """
        Create a Dash layout for accepting credentials for login.
        """

        return [
            html.Div(id="ganalytics_login_form", children=[
                html.H5("Client email"),
                dcc.Input(id="ganalytics_client_email", type="text"),

                html.H5("Private key"),
                dcc.Textarea(id="ganalytics_private_key"),

                html.Button("Connect!", id="ganalytics_connect_button",
                            style={"display": "inline"}, n_clicks=0)
            ]),

            html.Div(id="ganalytics_UI"),
        ]

    @property
    def success_layout(self):
        """
        Create a Dash layout after a successful login, and a menu \
        to fetch data.
        """

        return [
            html.Br(),
            dcc.Dropdown(id="ganalytics_metrics", placeholder="Select metrics to fetch",
                         options=[{"value": metric["id"], "label": metric["name"]}
                                  for metric in all_metrics["metrics"]],
                         multi=True),
            html.Button("Fetch metrics!", id="get_ganalytics",
                        n_clicks=0),
            html.Div(id="ganalytics_results"),
        ]

    @staticmethod
    def pretty_print(df):
        """
        Display the sample in a appealing manner, given a DataFrame. \
        This is only displayed prettily here, the `view` module only \
        shows tables.
        """

        return create_table(df)


class SpotifyAPI(APIConnection):

    api_name = "spotify"
    label = "Spotify"

    def connect(self, client_id, client_secret):
        """
        Connect to Spotify API.
        """

        creds = util.oauth2.SpotifyClientCredentials(client_id, client_secret)
        token = creds.get_access_token()

        self.api = Spotify(auth=token)
        self.state = "authenticated"

    @cache.memoize(24 * 60 * 60)
    def fetch_data(self, category="toplists"):
        """
        Fetch information about Spotify playlists in a given category.

        Args:
            category (str): The category in Spotify for playlists, e.g.: \
                            "toplists".

        Returns:
            `pd.DataFrame`: A sample of the fetched data.
        """

        top_playlists = self.api.category_playlists(category)["playlists"]
        playlist_items = top_playlists["items"]

        data = [[
            playlist['name'],
            playlist['owner']['display_name'],
            playlist['tracks']['total'],
            playlist["external_urls"]["spotify"]
        ] for playlist in playlist_items]

        df = pd.DataFrame(data, columns=["name", "owner", "total_tracks", "link"])

        # Infer and save the schema & data
        self.save_data_and_schema(df, category)

        return df.head()

    @property
    def login_layout(self):
        """
        Create a Dash layout for accepting credentials for login.
        """

        return [
            html.Div(id="spotify_login_form", children=[
                html.H5("Client id"),
                dcc.Input(id="spotify_client_id", type="text"),

                html.H5("Client secret"),
                dcc.Input(id="spotify_client_secret", type="text"),

                html.Button("Connect!", id="spotify_connect_button",
                            style={"display": "inline"}, n_clicks=0)
            ]),

            html.Div(id="spotify_UI"),
        ]

    @property
    def success_layout(self):
        """
        Create a Dash layout after a successful login, and a menu \
        to fetch data.
        """

        return [
            dcc.Input(id="spotify_category", placeholder="Enter a category..."),
            html.Button("Fetch playlists!", id="get_spotify",
                        n_clicks=0),
            html.Div(id="spotify_results"),
        ]

    @staticmethod
    def pretty_print(df):
        """
        Display the sample in a appealing manner, given a DataFrame. \
        This is only displayed prettily here, the `view` module only \
        shows tables.
        """

        return [
            html.Div([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4(playlist["name"]),
                        html.A("listen on Spotify",
                               href=playlist["external_urls"]["spotify"]),
                    ]),
                    dbc.CardBody([
                        html.H5(f"Owner: {playlist['owner']['display_name']}",
                                className='card-title'),
                        html.P(f"{playlist['tracks']['total']} total tracks",
                               className='card-text'),
                    ]),
                ]),
                html.Br(),
            ]) for (i, playlist) in df.iterrows()
        ]


class QuandlAPI(APIConnection):

    api_name = "quandl"
    label = "Quandl"

    def connect(self, api_key):
        """
        Connect to Quandl API.
        """

        # Make a dummy call to the Quandl API since there is no
        # other mechanism to check the validity of requests.
        # If it fails, is is handled by the caller.
        quandl.get("NSE/OIL", api_key=api_key, rows=5)

        # If the assertion was successful,
        self.api_key = api_key
        self.state = "authenticated"

    @cache.memoize(24 * 60 * 60)
    def fetch_data(self, dataset_tag):
        """
        Fetch a dataset from Quandl.

        Args:
            dataset_tag (str): The dataset tag in Quandl, e.g. "NSE/OIL".

        Returns:
            `pd.DataFrame`: A sample of the fetched data.
        """

        df = quandl.get(dataset_tag, api_key=self.api_key)

        # Infer and save the schema & data
        self.save_data_and_schema(df, key=dataset_tag)

        return df.head()

    @property
    def login_layout(self):
        """
        Create a Dash layout for accepting credentials for login.
        """

        return [
            html.Div(id="quandl_login_form", children=[
                html.H5("Quandl API key"),
                dcc.Input(id="quandl_api_key", type="text"),

                html.Button("Connect!", id="quandl_connect_button",
                            style={"display": "inline"}, n_clicks=0)
            ]),

            html.Div(id="quandl_UI"),
        ]

    @property
    def success_layout(self):
        """
        Create a Dash layout after a successful login, and a menu \
        to fetch data.
        """

        return [
            dcc.Input(id="quandl_dataset_tag", placeholder="Input a dataset tag..."),
            html.Button("Fetch dataset!", id="get_quandl",
                        n_clicks=0),
            html.Div(id="quandl_results"),
        ]

    @staticmethod
    def pretty_print(df):
        """
        Display the sample in a appealing manner, given a DataFrame. \
        This is only displayed prettily here, the `view` module only \
        shows tables.
        """

        return create_table(df)
