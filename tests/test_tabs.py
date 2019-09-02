from .testing_utils import SeleniumTest, SLEEP_DELAY

import sys
import os
import warnings
import time

sys.path.insert(0, os.path.abspath("../EDA_miner"))
warnings.filterwarnings("ignore")


class TestTabs(SeleniumTest):

    # Open a selenium webdriver and click over each tab
    def test_tabs(self):
        self.login()

        # Wait for potential redirects.
        time.sleep(SLEEP_DELAY)
        # Try to access the apps that need login
        for app in ["data", "visualization", "modeling"]:
            self.chrome.get(f"http://127.0.0.1:8000/{app}/")

            time.sleep(SLEEP_DELAY)

            low_level_tab_menu = self.chrome.find_element_by_id("level2_tabs")
            low_level_tabs = low_level_tab_menu.find_elements_by_class_name("tab")

            for llt in low_level_tabs:
                llt.click()
                time.sleep(SLEEP_DELAY/2)

        # re-run after checking the last element,
        # because that might have broken the page
        llt.click()
        time.sleep(SLEEP_DELAY/2)

        self.logout()
