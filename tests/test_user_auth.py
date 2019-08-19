from .testing_utils import SeleniumTest, SLEEP_DELAY

import sys
import os
import warnings
import time

sys.path.insert(0, os.path.abspath("../EDA_miner"))
warnings.filterwarnings("ignore")


class TestUserAuth(SeleniumTest):

    def test_login(self):
        self.login()

        # Wait for potential redirects.
        time.sleep(SLEEP_DELAY)
        # Login redirection successful
        assert self.chrome.current_url.endswith("/user/admin/")

        # Try to access the apps that need login
        for app in ["data", "viz", "modeling"]:
            self.chrome.get(f"http://127.0.0.1:8000/{app}/")

            # Wait for potential redirects. The .get function
            # waits only for the first page, not the redirection
            time.sleep(SLEEP_DELAY)

            # Allowed to stay on the app's page
            # (if not, the app was expected to redirect)
            assert self.chrome.current_url.endswith(f"/{app}/")

        self.logout()

    def test_logout(self):
        self.login()
        self.logout()

        # Wait for potential redirects.
        time.sleep(SLEEP_DELAY)

        # Logout redirection is correct
        assert self.chrome.current_url.endswith("/")

        # Try to access the apps that need login
        for app in ["data", "viz", "modeling"]:
            self.chrome.get(f"http://127.0.0.1:8000/{app}/")

            # Wait for potential redirects.
            time.sleep(SLEEP_DELAY)

            # Not allowed to stay on the app's page
            # and redirected elsewhere (e.g. /login or 401)
            assert not self.chrome.current_url.endswith(f"/{app}/")

        # Try to access a profile page
        self.chrome.get("http://127.0.0.1:8000/user/admin/")

        # Wait for potential redirects.
        time.sleep(SLEEP_DELAY)

        # Should not be able to view user page unless logged in
        assert not self.chrome.current_url.endswith("/user/admin/")


