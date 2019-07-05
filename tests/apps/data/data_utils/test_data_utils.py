import sys
import os
import warnings
from redis import Redis
import json
import pickle

sys.path.insert(0, os.path.abspath("../EDA_miner"))
warnings.filterwarnings("ignore")

from apps.data import APIs, Upload, View
from apps.data.data_utils import api_connectors, api_layouts
from utils import cleanup


class TestAPIs:

    r = Redis(host="localhost", port=6379, db=0)

    creds = {
        "consumer_key": os.environ["twitter_consumer_key"],
        "consumer_secret": os.environ["twitter_consumer_secret"],
        "access_token_key": os.environ["twitter_access_token_key"],
        "access_token_secret": os.environ["twitter_access_token_secret"],
    }

    def test_twitter_connect(self):
        api = api_connectors.twitter_connect(**self.creds)

        assert api.VerifyCredentials().id_str is not None

    # Test if tweets are returned
    def test_get_tweets(self):
        self.api = api_connectors.twitter_connect(**self.creds)
        self.r.set(f"userid_twitter_api_handle", pickle.dumps(self.api))

        response = (eval(APIs.get_users_tweets(5, None, "userid"))["response"]
                    ["props"]["children"])
        assert isinstance(response, list)

