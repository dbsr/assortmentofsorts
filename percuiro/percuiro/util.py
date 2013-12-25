# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import re

from BeautifulSoup import BeautifulSoup
import requests

import common
from memoize import MemoizeDecorator, TTL_ONE_DAY

@MemoizeDecorator(common.DATA_DIR + '/req_soup.json', TTL_ONE_DAY)
def _req(url):
    headers = {
        'User-Agent': common.USER_AGENT
    }
    req = requests.get(url, headers=headers)
    return req.content


def req_soup(url):
    return BeautifulSoup(_req(url))


def is_valid_result(result, query, media_type, min_match_percentage=1):
    filter_extensions_rgx = r'[\-.](?:{})[\.\s]?'.format(
        '|'.join(common.MEDIA_TYPE_EXTENSIONS.get(media_type)))
    result_str = repr(result.values())
    if re.search(filter_extensions_rgx, result_str, re.I):
        qsplit = query.split()
        matches = filter(
            lambda split: re.search(split, result_str, re.I),
            qsplit)
        match_percentage = len(matches) / float(len(qsplit)) 
        if match_percentage >= min_match_percentage:
            return True


def is_debrid_host(href):
    print href
    return re.search(common.REAL_DEBRID_REGEX, href) is not None
