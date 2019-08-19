import sys
import os
import warnings

sys.path.insert(0, os.path.abspath("../EDA_miner"))
warnings.filterwarnings("ignore")

from data.data_utils import api_layouts


class TestAPIs:

    twitter_creds = {
        "consumer_key": os.environ["twitter_consumer_key"],
        "consumer_secret": os.environ["twitter_consumer_secret"],
        "access_token_key": os.environ["twitter_access_token_key"],
        "access_token_secret": os.environ["twitter_access_token_secret"],
    }

    def test_twitter_connect(self):
        connection = api_layouts.TwitterAPI("testuser")
        connection.connect(**self.twitter_creds)

        assert connection.api is not None
        assert connection.api.VerifyCredentials().id_str is not None
        assert connection.state == "authenticated"
