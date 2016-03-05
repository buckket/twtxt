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

import click

logger = logging.getLogger(__name__)


class Cache:
    cache_dir = click.get_app_dir("twtxt")
    cache_name = "cache"

    def __init__(self, cache_file, cache):
        """Initializes new :class:`Cache` object.

        :param cache_file: full path to the loaded cache file.
        :param cache: a Shelve object, with cache loaded.
        """
        self.cache_file = cache_file
        self.cache = cache
        self.cache["last_update"] = self.cache.get("last_update") or 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    @classmethod
    def from_file(cls, file):
        """Try loading given cache file."""
        try:
            cache = shelve.open(file)
            return cls(file, cache)
        except OSError as e:
            logger.debug("Loading {0} failed".format(file))
            raise e

    @classmethod
    def discover(cls):
        """Make a guess about the cache file location an try loading it."""
        file = os.path.join(Cache.cache_dir, Cache.cache_name)
        return cls.from_file(file)

    def is_cached(self, url):
        """Checks if specified URL is cached."""
        try:
            return True if url in self.cache else False
        except TypeError:
            return False

    def last_updated(self):
        """Returns *NIX timestamp of last update of the cache."""
        return self.cache["last_update"]

    def mark_updated(self):
        """Mark Cache as updated at current *NIX timestamp"""
        self.cache["last_update"] = timestamp()

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
