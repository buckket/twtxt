"""
    twtxt.twfile
    ~~~~~~~~~~~~

    This module handles interaction with the local twtxt file.

    :copyright: (c) 2016-2022 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import logging

from twtxt.parser import parse_tweets

logger = logging.getLogger(__name__)


def get_local_tweets(source, limit):
    try:
        with open(source.file, "r") as fh:
            input_lines = fh.readlines()
    except (FileNotFoundError, PermissionError) as e:
        logger.debug(e)
        return []
    local_tweets = parse_tweets(input_lines, source)
    return sorted(local_tweets, reverse=True)[:limit]


def add_local_tweet(tweet, file):
    try:
        with open(file, "a") as fh:
            fh.write("{0}\n".format(str(tweet)))
    except (FileNotFoundError, PermissionError) as e:
        logger.debug(e)
        return False
    return True
