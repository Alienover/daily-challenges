#coding=utf-8

import os
import socket
import smtplib
import logging
from utils import setup_logger
from string import Template
from email.header import Header
from email.mime.text import MIMEText

setup_logger()

tpl_path = os.path.join(os.getcwd(), 'templates')

class EmailCLI(object):
    def __init__(self, host, username, password):
        try:
            self.smtp = smtplib.SMTP_SSL(host)
            self.smtp.connect(host)
        except socket.error as e:
            logging.error('SMTP connect error: %s' % e, exc_info=True)
            self.smtp = smtplib.SMTP()
            self.smtl.connect(host)

        self.smtp.login(username, password)
        logging.info('Connected to SMTP [%s]' % host)

    def close(self):
        self.smtp.quit()
        logging.info('Disconnect from SMTP')

    @classmethod
    def parse_email_template(self, tpl_name, data):
        with open('%s/%s' % (tpl_path, tpl_name), 'r') as f:
            tpl = Template(f.read())
            return tpl.substitute(data)

    def send(self, sender, receivers, subject ,message):
        if message == '' or message == None:
            raise Exception('Invalid email body')

        to =  ','.join(receivers) if type(receivers) is list else receivers
        mime = MIMEText("{0}".format(message), 'text/html', 'utf-8')
        mime["Subject"] = Header(subject, 'utf-8')
        mime["From"] = sender
        mime["To"] = receivers
        try:
            logging.info('Sending message from [%s] to [%s]' % (sender, receivers))
            self.smtp.sendmail(sender, receivers.split(','), mime.as_string())
        except Exception as e:
            logging.error('Failed to send message [%s]: %s' % (receivers, e), exc_info=True)
            raise e
