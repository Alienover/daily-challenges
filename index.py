# coding=utf-8

import os
import sys
import json
import logging
import settings
from datetime import datetime
from optparse import OptionParser
from libs.email_lib import EmailCLI
from crawlers.leetcode import Leetcode
from utils import kebab_case, setup_logger

setup_logger()

class DailyChallenge:
    def crawl(self, client, output = '/tmp/%s-%s.json'):
        logging.info('Start crawling daily challenge from [%s]' % client.client_name)
        challenge = client.get_latest_challenge()
        logging.info('Crawling end')

        if challenge is not None:
            filename = output % (
                kebab_case(datetime.now().strftime("%b %d")),
                kebab_case(challenge["title"])
            )

            try:
                logging.info('Saving the crawled output to file [%s]' % filename)
                with open(filename, 'w') as outfile:
                    json.dump(challenge, outfile)
                    return filename
            except Exception as e:
                logging.error('Failed to save data to file [%s] %s' % (filename, e), exc_info=True)
                sys.exit(1)
        return None

    def send(self, email_cli, filename, sender = '', receivers = ''):
        if sender == '' or sender == None:
            logging.error('Invalid sender [%s]' % sender, exc_info=True)
            return
        if receivers == '' or receivers == None:
            logging.error('Invalid receivers [%s]' % receivers, exc_info=True)
            return

        try:
            logging.info('Loading message parameters from [%s]' % filename)
            with open(filename, 'r') as inputfile:
                data = json.load(inputfile)
        except Exception as e:
            loging.error('Failed to load message parameters from [%s] %s' % (filename, e))
            sys.exit(1)

        email_body = EmailCLI.parse_email_template(settings.templates["LEETCODE_DAILY"], data)

        subject = "Daily Challenge %s - %s" % (
            datetime.now().strftime('%b %d'),
            data["title"]
        )
        email_cli.send(sender, receivers, subject, email_body)
        email_cli.close()

if __name__ == "__main__":
    parser = OptionParser()
    dc = DailyChallenge()

    parser.add_option("--mode", "-m")
    parser.add_option("--host")
    parser.add_option("--filename", "-f")
    parser.add_option("--username", "-u")
    parser.add_option("--password", "-p")
    parser.add_option("--sender" "-s")
    parser.add_option("--receivers", "-r")

    (options, args) = parser.parse_args()

    if options.username and options.password:
        if options.mode == 'crawl':
            lc = Leetcode(options.username, options.password)
            filename = dc.crawl(lc)
            print(filename)

        elif options.mode == 'email' and options.host and options.filename and options.sender and options.receivers:
            email_cli = EmailCLI(options.host, options.username, options.password)
            dc.send(email_cli, options.filename, sender=options.sender, receivers=options.receivers)
