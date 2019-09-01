from selenium.webdriver.chrome import webdriver, options
from redis import Redis
import warnings
import sys
import os
import subprocess
import signal
import time


sys.path.insert(0, os.path.abspath("../EDA_miner"))
warnings.filterwarnings("ignore")

from utils import cleanup

chromedriver = os.environ.get("CHROMEDRIVER", "chromedriver")
SLEEP_DELAY = float(os.environ.get("SLEEP_DELAY", 3))


class SeleniumTest:

    @classmethod
    def setup_class(cls):

        # Start the server and wait till is loads
        cmd = "cd ../EDA_miner && gunicorn wsgi:application"
        cls.server = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                      shell=True, preexec_fn=os.setsid)
        time.sleep(7)

        # Start a webdriver
        chrome_options = options.Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        cls.chrome = webdriver.WebDriver(chromedriver, options=chrome_options)

    @classmethod
    def teardown_class(cls):
        cls.chrome.close()
        os.killpg(os.getpgid(cls.server.pid), signal.SIGTERM)
        time.sleep(2)

    def login(self):
        self.chrome.get("http://127.0.0.1:8000/login")
        # Wait for potential redirects.
        time.sleep(SLEEP_DELAY)

        username = self.chrome.find_element_by_id("username")
        password = self.chrome.find_element_by_id("password")
        submit = self.chrome.find_element_by_id("submit")

        # Login
        username.send_keys("admin")
        password.send_keys("admin")
        submit.submit()

        # Wait for potential redirects.
        time.sleep(SLEEP_DELAY)

    def logout(self):
        self.chrome.get("http://127.0.0.1:8000/logout")

        # Wait for potential redirects.
        time.sleep(SLEEP_DELAY)


class RedisTest:

    @classmethod
    def setup_class(cls):
        cls.redis_conn = Redis(port=6379, db=0)

    @classmethod
    def teardown_class(cls):
        cleanup(cls.redis_conn)
        os.remove("redisData.pkl")
