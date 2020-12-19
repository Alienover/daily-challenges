# coding=utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import sys
import os

driver_names = {
    "linux": 'chromedriver',
    "mac": "chromedriver_mac"
}

def init_webdriver():
    platform = 'linux'
    if 'darwin' in sys.platform:
        platform = 'mac'

    options = Options()
    options.add_argument('--headless')

    driver_path = os.path.join(os.getcwd(), 'libs', driver_names.get(platform))

    return webdriver.Chrome(executable_path=driver_path, options=options)
