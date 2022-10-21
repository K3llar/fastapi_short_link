import random
import re

from . import constants as cst


def get_unique_short_link(symbols=cst.SYMBOLS,
                          length=cst.LEN_SHORT_URL):
    url_link = ''
    for char in range(length):
        url_link += random.choice(symbols)
    return


def regex_validation(string):
    if re.match(cst.PATTERN, string):
        return True
    return False
