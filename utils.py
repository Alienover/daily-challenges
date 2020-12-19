# coding=utf-8

import re
import logging

def mask_secret(str):
    return re.sub(r'^([\s\S]{3})(?:.*)([\s\S]{3})$', '\\1***\\2', str)

def kebab_case(str):
    return '-'.join(list(map(lambda x: x.lower(), str.split(' '))))

def setup_logger():
    LOG_FORMAT = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
