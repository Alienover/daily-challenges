#coding=utf-8

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from libs.webdriver import init_webdriver
from utils import mask_secret, kebab_case, setup_logger
import os
import logging

setup_logger()

class Leetcode(object):
    LOGIN_URL = 'https://leetcode.com/accounts/login/'
    PROBLEM_URL = 'https://leetcode.com/problems/%s'
    DAILY_CHALLENGE_URL = 'https://leetcode.com/explore/featured/card/%s-leetcoding-challenge-%s'

    TIMEOUT = 30
    def __init__(self, username, password):
        logging.info('Initializing web driver...')
        self.username = username
        self.password = password
        self.broswer = init_webdriver()
        logging.info('Web driver initialized')

    def check_initial_loader(self):
        return EC.invisibility_of_element_located((By.ID, 'initial-loading'))

    def check_common_loader(self):
        return EC.invisibility_of_element_located((By.CSS_SELECTOR, '[class*=loading]'))

    def check_challenge_item(self):
        return EC.presence_of_element_located((By.CSS_SELECTOR, '.table-item.accessible'))

    def check_challenge_detail(self):
        return EC.presence_of_element_located((By.CSS_SELECTOR, '.question-base.viewer-base'))

    def check_account_menu(self):
        return EC.presence_of_element_located((By.CSS_SELECTOR, '[class*=nav-item-container] [class*=account-icon]'))

    def is_loaded(self, checker = None):
        if checker is not None:
            try:
                WebDriverWait(self.broswer, self.TIMEOUT).until(checker())
                return True
            except TimeoutException:
                logging.error('Take too much time to load', exc_info=True)
                return False
        else:
            return False


    def login(self):
        logging.info('Loading login page url[%s]' % self.LOGIN_URL)
        self.broswer.get(self.LOGIN_URL)
        if self.is_loaded(self.check_initial_loader):
            logging.info('Login page loaded')
            self.broswer.find_element(By.CSS_SELECTOR, 'input[name=login]').send_keys(self.username)
            self.broswer.find_element(By.CSS_SELECTOR, 'input[name=password]').send_keys(self.password)
            logging.info('About to login with [%s] [%s]' % (
                mask_secret(self.username),
                mask_secret(self.password)
            ))
            self.broswer.find_element(By.ID, 'signin_btn').click()
            if (self.is_loaded(self.check_account_menu)):
                logging.info('Login successfully')
                return True

        raise Exception('Failed to login')
        return False

    def navigate_to_challenge(self, index):
        curr_year = datetime.now().strftime("%Y")
        curr_month = datetime.now().strftime('%B').lower()
        url = self.DAILY_CHALLENGE_URL % (curr_month, curr_year)
        self.broswer.get(url)
        logging.info('Loading daily challenge page url[%s]' % url)

        if self.is_loaded(self.check_challenge_item):
            items = self.broswer.find_elements(By.CSS_SELECTOR, '.table-item.accessible')
            logging.info('Found %s challenge in %s' % (len(items), curr_month))
            if len(items) > 0:
                latest_challenge = items[index]
                title = latest_challenge.find_element(By.CLASS_NAME, 'title').text.strip()
                logging.info('Found the latest challenge [%s]' % title)
                latest_challenge.click()
                logging.info('Navigating to the latest challenge detail')
                return True

        raise Exception('Failed to find the challenge')
        return False

    def get_challenge(self):
        url = self.broswer.current_url
        logging.info('Loading latest challenge detail url[%s]' % url)
        if self.is_loaded(self.check_challenge_detail):
            question = self.broswer.find_element(By.CLASS_NAME, 'question-wrapper')
            if question is not None:
                title = question.find_element(By.CLASS_NAME, 'question-title').text.strip()
                content = question.find_element(By.CSS_SELECTOR, '[class*=question-description]').get_attribute('innerHTML')

        if title == '' or content == '':
            raise Exception('Nothing scraped')
            return None

        data = {
            "challenge_url": url,
            'problem_url': self.PROBLEM_URL % kebab_case(title),
            "title": title,
            "content": content
        }
        logging.info('Detail loaded %s' % data)

        return data

    def get_latest_challenge(self):
        challenge = None
        try:
            self.login()
            if self.navigate_to_challenge(-1):
                challenge = self.get_challenge()
        except Exception as e:
            logging.error(e, exc_info=True)

        self.broswer.quit()
        return challenge

    @property
    def client_name(self):
        return 'Leetcode'
