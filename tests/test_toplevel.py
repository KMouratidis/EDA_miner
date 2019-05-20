import sys
import os
sys.path.insert(0, os.path.abspath("../EDA_miner"))
import warnings
warnings.filterwarnings("ignore")


from utils import cleanup
from redis import Redis


class TestUtilsCleanup:
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
