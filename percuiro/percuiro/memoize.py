# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

from time import time
import json

from cache import Cache


TTL_ONE_DAY = 86400
TTL_TEN_MINUTES = 600
TTL_ONE_HOUR = 3600

class MemoizeDecorator(object):
    def __init__(self, persistent_cache_path, ttl=-1):
        self.persistent_cache_path = persistent_cache_path
        self.ttl = ttl

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            if not args and not kwargs:
                key = hash(func.__name__)
            else:
                key = hash(str(list(args) + kwargs.values()))
            with Cache(self.persistent_cache_path) as cache:
                cached, age = cache.get(key, (0, 0))
                if not cached or (time() - age > self.ttl and self.ttl != -1):
                    cache[key] = (func(*args, **kwargs), time())
                return cache[key][0]
        return wrapped
