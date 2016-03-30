"""
    twtxt.cache
    ~~~~~~~~~~~

    This module implements a caching system for storing tweets.

    :copyright: (c) 2016 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import logging
import os
import shelve
from time import time as timestamp

from click import get_app_dir

logger = logging.getLogger(__name__)


class Cache:
    cache_dir = get_app_dir("twtxt")
    cache_name = "cache"

    def __init__(self, cache_file, cache, update_interval):
        """Initializes new :class:`Cache` object.

        :param str cache_file: full path to the loaded cache file.
        :param ~shelve.Shelve cache: a Shelve object, with cache loaded.
        :param int update_interval: number of seconds the cache is considered to be
                                    up-to-date without calling any external resources.
        """
        self.cache_file = cache_file
        self.cache = cache
        self.update_interval = update_interval

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    @classmethod
    def from_file(cls, file, *args, **kwargs):
        """Try loading given cache file."""
        try:
            cache = shelve.open(file)
            return cls(file, cache, *args, **kwargs)
        except OSError as e:
            logger.debug("Loading {0} failed".format(file))
            raise e

    @classmethod
    def discover(cls, *args, **kwargs):
        """Make a guess about the cache file location an try loading it."""
        file = os.path.join(Cache.cache_dir, Cache.cache_name)
        return cls.from_file(file, *args, **kwargs)

    @property
    def last_updated(self):
        """Returns *NIX timestamp of last update of the cache."""
        try:
            return self.cache["last_update"]
        except KeyError:
            return 0

    @property
    def is_valid(self):
        """Checks if the cache is considered to be up-to-date."""
        if timestamp() - self.last_updated <= self.update_interval:
            return True
        else:
            return False

    def mark_updated(self):
        """Mark cache as updated at current *NIX timestamp"""
        if not self.is_valid:
            self.cache["last_update"] = timestamp()

    def is_cached(self, url):
        """Checks if specified URL is cached."""
        try:
            return True if url in self.cache else False
        except TypeError:
            return False

    def last_modified(self, url):
        """Returns saved 'Last-Modified' header, if available."""
        try:
            return self.cache[url]["last_modified"]
        except KeyError:
            return None

    def add_tweets(self, url, last_modified, tweets):
        """Adds new tweets to the cache."""
        try:
            self.cache[url] = {"last_modified": last_modified, "tweets": tweets}
            self.mark_updated()
            return True
        except TypeError:
            return False

    def get_tweets(self, url, limit=None):
        """Retrieves tweets from the cache."""
        try:
            tweets = self.cache[url]["tweets"]
            self.mark_updated()
            return sorted(tweets, reverse=True)[:limit]
        except KeyError:
            return []

    def remove_tweets(self, url):
        """Tries to remove cached tweets."""
        try:
            del self.cache[url]
            self.mark_updated()
            return True
        except KeyError:
            return False

    def close(self):
        """Closes Shelve object."""
        try:
            self.cache.close()
            return True
        except AttributeError:
            return False

    def sync(self):
        """Syncs Shelve object."""
        try:
            self.cache.sync()
            return True
        except AttributeError:
            return False
