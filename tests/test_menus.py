import sys
import os
import warnings
from redis import Redis

sys.path.insert(0, os.path.abspath("../EDA_miner"))
warnings.filterwarnings("ignore")

from menus import button_toggle, serve_layout
from utils import cleanup


class TestMenu:
    r = Redis(host="localhost", port=6379, db=0)

    # Test collapsible div
    def test_sidebar_toggle(self):
        # TODO: This needs a better implementation, or at least a function
        assert (eval(button_toggle(5))["response"]["props"]["style"]["display"]
                == "block")

        assert (eval(button_toggle(4))["response"]["props"]["style"]["display"]
                == "none")

    # Test if at least 1 example dataset is uploaded
    def test_serve_datasets(self):
        _ = serve_layout()
        assert len(self.r.keys("*example*")) >= 1

        cleanup(self.r)
