from .testing_utils import RedisTest

import sys
import os
import warnings
import numpy as np
import pandas as pd
import dill
from redis import Redis

sys.path.insert(0, os.path.abspath("../EDA_miner"))
warnings.filterwarnings("ignore")

from utils import cleanup, hard_cast_to_float, redis_startup


class TestCleanup(RedisTest):

    def test_cleanup_redis(self):
        self.redis_conn.set("mykey", 5)
        cleanup(self.redis_conn)

        # Correctly flushes Redis
        assert self.redis_conn.get("mykey") is None
        # Correctly saves data to a pickle
        assert os.path.exists("redisData.pkl")


# TODO: properly do set up / tear down & split function & rename
class TestGetData(RedisTest):

    def test_get_data(self):

        # Create a dataframe
        dim = (3, 5)
        columns = [f"col_{x}" for x in range(dim[1])]
        index = [f"col_{x}" for x in range(dim[0])]
        df = pd.DataFrame(np.random.random(dim), columns=columns, index=index)

        # Send values to Redis and assert if they were received
        assert (self.redis_conn.set("userid_data_userdata_random",
                                    dill.dumps(df)) is True)

        # Get data from redis and decode
        user_data = dill.loads(self.redis_conn.get("userid_data_userdata_random"))
        # Test correct decoding
        np.testing.assert_array_equal(df, user_data)


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
        redis_conn = redis_startup()
        assert isinstance(redis_conn, Redis)

        cleanup(redis_conn)
        os.remove("redisData.pkl")
