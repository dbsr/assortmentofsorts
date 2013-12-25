# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import json


class Cache(object):
    def __init__(self, path):
        self.path = path
        try:
            with open(self.path) as f:
                self._cache = json.load(f)
        except IOError:
            self._cache = {}
        self.updated = False

    def __getitem__(self, key):
        return self._cache[key]

    def __setitem__(self, key, val):
        self._cache[key] = val
        self.updated = True

    def get(self, key, default):
        return self._cache.get(key, default)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.updated:
            with open(self.path, 'w') as f:
                json.dump(self._cache, f)
