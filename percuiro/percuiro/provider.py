# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import re

from common import GOOGLE_QUERY
from util import req_soup, is_valid_result, is_debrid_host


class BaseProvider(object):
    def __init__(self, name, query_url, get_results, supported_media):
        self.name = name
        if query_url is GOOGLE_QUERY:
            self.query_url = (
                'http://www.google.com/search?q=site:{name}'.format(name=name)
                + '+{query}')
        else:
            self.query_url = query_url
        self.get_results = get_results
        self.supported_media = supported_media

    def search(self, query, query_type):
        url = self.query_url.format(query=query)
        soup = req_soup(url)
        return filter(
            lambda result: is_valid_result(result, query, query_type),
            self.get_results(soup))

    def parse_result_url(self, url):
        soup = req_soup(url)
        hoster_links = filter(
            is_debrid_host,
            map(
                lambda anchor: anchor.get('href'),
                soup.findAll('a')))
        if not hoster_links:
            hoster_links = filter(
                is_debrid_host,
                re.findall(r'[\'"]?(http://[^\'" <>\)]+)\n?', str(soup)))
        return hoster_links
