import sys
import os
import signal
import subprocess
import warnings
import time
from selenium.webdriver.chrome import webdriver, options

sys.path.insert(0, os.path.abspath("../EDA_miner"))
warnings.filterwarnings("ignore")


class TestTabs:

    # Open a selenium webdriver and click over each tab
    def test_clicking(self):
        cmd = "cd ../EDA_miner && python app.py"
        # Thanks: https://stackoverflow.com/a/4791612/6655150
        pro = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               shell=True, preexec_fn=os.setsid)

        # Wait till the server boots up
        time.sleep(10)

        chromedriver = os.environ["CHROMEDRIVER"]

        # Make sure the window is maximized and start a webdriver
        chrome_options = options.Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--no-sandbox')
        chrome = webdriver.WebDriver(chromedriver, options=chrome_options)

        # Navigate to the page
        chrome.get("http://127.0.0.1:8050")
        time.sleep(2)


        # Get and iterate over the high-level and low-level tabs
        high_level_tab_menu = chrome.find_element_by_id("high_level_tabs")
        high_level_tabs = high_level_tab_menu.find_elements_by_class_name("tab")
        for hlt in high_level_tabs:
            hlt.click()
            time.sleep(1)

            low_level_tab_menu = chrome.find_element_by_id("selected_subpage")
            low_level_tabs = low_level_tab_menu.find_elements_by_class_name("tab")

            for llt in low_level_tabs:
                print(llt.text)
                llt.click()
                time.sleep(1)

        # re-run after checking the last element,
        # because that might have broken the page
        llt.click()
        time.sleep(1)

        # Close the webdriver
        chrome.quit()

        # kill the server
        # TODO: Does this indeed kill the server?
        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

