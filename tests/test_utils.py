import sys
import os
import warnings
import base64
import numpy as np
import pandas as pd
import pickle
from redis import Redis

sys.path.insert(0, os.path.abspath("../EDA_miner"))
warnings.filterwarnings("ignore")

from utils import cleanup, get_data, hard_cast_to_float, parse_contents, redis_startup


class TestCleanup:
    r = Redis(host="localhost", port=6379, db=0)

    def test_cleanup_images(self):
        # create an empty file
        with open("../EDA_miner/static/images/python_generated_ssid_file.txt", "w") as f:
            f.write("hello")

        cleanup(self.r)

        # get all files
        images = os.listdir(os.path.abspath("../EDA_miner/static/images"))
        # keep only files that belong to non-registered users
        non_user_images = [img for img in images
                           if "python_generated_ssid" in img]

        assert len(non_user_images) == 0

    def test_cleanup_redis(self):

        self.r.set("mykey", 5)
        cleanup(self.r)
        assert len(self.r.keys("*")) == 0


# TODO: properly do set up / tear down & split function & rename
class TestGetData:
    r = Redis(port=6379, db=0)

    def test_get_data(self):

        # Create a dataframe
        dim = (3,5)
        columns = [f"col_{x}" for x in range(dim[1])]
        index = [f"col_{x}" for x in range(dim[0])]
        df = pd.DataFrame(np.random.random(dim), columns=columns, index=index)

        # Send values to Redis and assert if they were received
        assert self.r.set("userid_user_data_random", pickle.dumps(df)) is True
        assert self.r.set("userid_gsheets_api_data", pickle.dumps(df)) is True

        # test msgpack
        np.testing.assert_array_equal(df, get_data("user_data_random", "userid"))
        # test pickle
        np.testing.assert_array_equal(df, get_data("gsheets_api", "userid"))
        # test non-implemented api
        assert get_data("non_existing_API", "userid") is None

        #cleanup(self.r)


class TestHardCast:

    def test_value(self):
        np.testing.assert_almost_equal(hard_cast_to_float("5.43"), 5.43, 3)
        np.testing.assert_almost_equal(hard_cast_to_float("2"), 2, 3)
        np.testing.assert_almost_equal(hard_cast_to_float("x"), 0, 3)

    def test_type(self):
        assert isinstance(hard_cast_to_float(3.31).item(), float)
        assert isinstance(hard_cast_to_float("3").item(), float)
        assert isinstance(hard_cast_to_float("x"), float)


class TestStartup:

    def test_startup(self):
        r = redis_startup()
        assert isinstance(r, Redis)
