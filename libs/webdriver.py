# coding=utf-8

from selenium import webdriver
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

    driver_path = os.path.join(os.getcwd(), 'lib', driver_names.get(platform))

    return webdriver.Chrome(executable_path=driver_path)
