"""
    This module provides utilities, functions, and other code that is
    meant to be used across the app. This may undergo changes soon.

    Functions included:
        - create_dropdown: Create an H4 and a dropdown.
        - cleanup: Handle app's exit.
        - encode_image:

    You should probably not write code here.
"""

import dash_html_components as html
import dash_core_components as dcc

import dash_table

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBClassifier
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler

import pandas as pd
import base64
import json
import io
import redis
import pickle
import os


def redis_startup():
    r = redis.Redis(host="localhost", port=6379, db=0)

    return r

r = redis_startup()


mapping = {
    "logr": LogisticRegression,
    "linr": LinearRegression,
    "xgb": XGBClassifier,
    "dtr": DecisionTreeRegressor,
    "svr": SVR,
    "kmc": KMeans,
    "dbscan": DBSCAN,
    "stdsc": StandardScaler,
}


def create_dropdown(name, options, **kwargs):
    """Simple utility that makes titled dropdowns"""
    return [
        html.H5(name+":"),
        dcc.Dropdown(
            options=options,
            **kwargs
        )]


def get_data(api_choice, user_id):

    if api_choice is None:
        df = None

    elif api_choice == "gsheets_api":
        df = pickle.loads(r.get(f"{user_id}_{api_choice}_data"))

    # uploaded data
    elif api_choice == "user_data":
        df = pd.read_msgpack(r.get(f"{user_id}_{api_choice}"))

    elif api_choice.startswith("quandl_api"):
        df = pickle.loads(r.get(f"{user_id}_{api_choice}"))

    return df


# TODO: Implement user_id correctly:
# create a Redis entry with all `user_id`s that
# joined the session and cleanup for each of them
# TODO: Persist data from logged in users
def cleanup(redisConn):
    """
        Clean up after the Dash app exits.

        Flush every key stored in the Redis database. If there
        are users that have logged in and uploaded data, store
        those on disk.

        Arguments:
        redisConn -- A `redis.Redis` connection.
    """

    print("Cleaning up...")
    redisConn.flushdb()




def encode_image(image_path):
    """Read and base64-encode an image for the dash app."""

    return 'data:image/png;base64,{}'.format(base64.b64encode(
        open(image_path, 'rb').read()).decode())


def pretty_print_tweets(api, n_tweets):
    return [
        html.H5(str(tweet.text))
        for tweet in api.GetUserTimeline()[:n_tweets]
    ]

def create_table(df, table_id="table"):

    return dash_table.DataTable(
        id=table_id,
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        style_table={
            'maxHeight': '400',
            'overflowY': 'scroll'
        },
        sorting=True,
        editable=True,
        pagination_mode='fe',
        pagination_settings={
            "displayed_pages": 1,
            "current_page": 0,
            "page_size": 10,
        },
        navigation="page",
        # n_fixed_rows=1,
        style_cell={
            'width': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
            'paddingLeft': '15px',
            # 'paddingRight': '15px',
        },
        style_cell_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(218, 218, 218)'
            },
            {
                'if': {'row_index': 'even'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
        ],
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'rgb(230,230,230)',
            "fontWeight": "bold",
        },
    )


# TODO: this function needs to be reviewed because
# it doesn't work correctly on error (i.e. returns a Div).
def parse_contents(contents, filename, date, user_id):
    """
        After decoding the uploaded file, handle any
        remaining operations here. This was stolen
        from the dash docs.
    """

    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'json' in filename:
            # Assume that the user uploaded an excel file
            try:
                df = pd.DataFrame.from_dict(json.loads(decoded.decode('utf-8')))
            except ValueError:
                # JSON file is probably only one row, so convert it to list
                df = pd.DataFrame.from_dict([json.loads(decoded.decode('utf-8'))])

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    # Store to redis for caching
    r.set(f"{user_id}_user_data", df.to_msgpack(compress='zlib'))

    return html.Div([
        "Data uploaded sucessfully."
    ])
