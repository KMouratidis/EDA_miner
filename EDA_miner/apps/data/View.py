"""
This module provides views for the data (tables, lists of tweets, etc).

Functions:
    - get_available_choices: Get datasets available to user.

Dash callbacks:
    - display_subdataset_choices: Show/hide input field for Quandl API.
    - render_table: Create a display for the chosen dataset.
    - display_reddit_posts: For the Reddit API, allow the user to \
                            specify a subreddit to get data from.

Note to others:
    You should probably not write code here, UNLESS you defined a \
    new connection to an API, or are doing refactoring.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_table
import dash_bootstrap_components as dbc

from server import app
from utils import r, pretty_print_tweets, create_table, get_data

import pickle


# TODO: This might need to get moved to a higher module
def get_available_choices(redis_conn, user_id):
    """
    Get datasets available to user.

    Args:
        redis_conn (`redis.Redis`):
        user_id (str): Session/user id.

    Returns:
        [list(dict), dict]: A list of options to be used for making \
                            dropdowns, and a dict of the available \
                            dataset keys (and their mapped data).
    """

    results = {
        "twitter_api": redis_conn.get(f"{user_id}_twitter_api_handle"),
        "gsheets_api": redis_conn.get(f"{user_id}_gsheets_api_data"),
        "reddit_api": redis_conn.get(f"{user_id}_reddit_api_handle"),
        "spotify_api": redis_conn.get(f"{user_id}_spotify_api_handle"),
    }

    # Since non-logged in users have this string pre-appended we need to
    # remove not the first but the three-first words
    if user_id.startswith("python_generated_ssid_"):
        splitter = 4

    # Quandl-retrieved datasets (may be many, thus we pattern-match redis keys)
    quandl_datasets = [x.decode() for x
                       in redis_conn.keys(f"{user_id}_quandl_api_*")]
    results.update({"_".join(q.split("_")[splitter:]): q
                    for q in quandl_datasets})

    # user-uploaded datasets (may be many, thus we pattern-match redis keys)
    user_datasets = [x.decode() for x
                     in redis_conn.keys(f"{user_id}_user_data_*")]
    results.update({"_".join(q.split("_")[splitter:]): q
                    for q in user_datasets})

    options = [
        {'label': k, 'value': k}
        for k, v in results.items() if v is not None
    ]
    if len(options) < 1:
        options = [{'label': "No uploaded data yet", 'value': "no_data"}]

    return options, results


def View_Options(user_id):

    options, results = get_available_choices(r, user_id)
    available_choices = html.Div(dcc.Dropdown(options=options,
                                              id="api_choice"),
                                 className="horizontal_dropdowns")

    return [
        html.Br(),
        available_choices,

        dcc.Input(id="dataset_name", style={"display": "none"}),

        html.Div(id="table_view", children=[
            dash_table.DataTable(id='table'),
        ]),
    ]


# TODO: This might need to be removed (or updated)
@app.callback(Output("dataset_name", "style"),
              [Input("api_choice", "value")])
def display_subdataset_choices(api_choice):
    """
    Show/hide input field for Quandl API.

    Args:
        api_choice (str): Value from the dropdown.

    Returns:
        dict: CSS style.
    """
    if api_choice == "quandl_api":
        return {"display": "inline"}
    else:
        return {"display": "none"}


@app.callback(Output("table_view", "children"),
              [Input("api_choice", "value")],
              [State("user_id", "children")])
def render_table(api_choice, user_id):
    """
    Create a display for the chosen dataset.

    Args:
        api_choice (str): Value from the dropdown.
        user_id (str): Session/user id.

    Returns:
        list: A list of dash components.
    """

    if user_id == "<registered_user>":
        # if the user is a registered user, override their
        # name for use within this function
        user_id = current_user.username

    if api_choice is None:
        return [html.H4("Nothing selected.")]

    if api_choice == "twitter_api":
        api = pickle.loads(r.get(f"{user_id}_{api_choice}_handle"))

        return pretty_print_tweets(api, 5)

    elif api_choice == "reddit_api":
        api = r.get(f"{user_id}_{api_choice}_handle")

        return [
            html.H4("Write the name of a subreddit:"),
            dcc.Input(id="subreddit_choice", type="text", value="",),
            html.Button("Gimme dem reddits", id="reddit_submit"),

            html.Br(),
            html.Br(),
            html.Div(id="subreddit_posts"),
        ]

    elif api_choice == "spotify_api":
        spotify = pickle.loads(r.get(f"{user_id}_{api_choice}_handle"))
        top_playlists = spotify.category_playlists("toplists")["playlists"]["items"]

        posts = [
            html.Div([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4(playlist["name"]),
                        html.A("listen on Spotify",
                               href=playlist["external_urls"]["spotify"]),
                    ]),
                    dbc.CardBody([
                        dbc.CardTitle(f"Owner: {playlist['owner']['display_name']}"),
                        dbc.CardText(f"{playlist['tracks']['total']} total tracks"),
                    ]),
                ]),
                html.Br(),
            ]) for playlist in top_playlists
        ]
        return posts

    elif api_choice == "quandl_api":
        df = get_data(api_choice, user_id)

    else:
        df = get_data(api_choice, user_id)

    if df is None:
        return [html.H4("Nothing to display")]

    df = df[df.columns[:10]]
    return [
        html.Br(),
        create_table(df),
    ]


@app.callback(Output("subreddit_posts", "children"),
              [Input("reddit_submit", "n_clicks")],
              [State("subreddit_choice", "value"),
               State("user_id", "children")])
def display_reddit_posts(n_clicks, subreddit_choice, user_id):
    """
    For the Reddit API, allow the user to specify a subreddit \
    to get data from.

    Args:
        n_clicks (int): Number of times button was clicked.
        subreddit_choice (str): The name of the subreddit.
        user_id (str): Session/user id.

    Returns:
        list: A list of dash components.
    """


    if n_clicks is not None and n_clicks >=1:
        if subreddit_choice is not None:

            api = pickle.loads(r.get(f"{user_id}_reddit_api_handle"))
            subreddit = api.subreddit(subreddit_choice)

            posts = [
                html.Div([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H4(post.title),
                            html.A("view at reddit", href=post.permalink),
                        ]),
                        dbc.CardBody([
                            dbc.CardTitle(f"Written by {post.author.name}, "
                                          f"score: {post.score}"),
                            dbc.CardText(dcc.Markdown(post.selftext),),
                        ]),
                    ]),
                    html.Br(),
                ]) for post in subreddit.hot(limit=5)
            ]
            return posts

        else:
            return [html.H4("No subreddit choice")]

    else:
        return [html.H4("No reddit data to display.")]
