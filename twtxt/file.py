"""
    twtxt.file
    ~~~~~~~~~~

    This module handles interaction with the local twtxt file.

    :copyright: (c) 2016 by buckket.
    :license: MIT, see LICENSE for more details.
"""
import hashlib
import logging

from twtxt.parser import parse_string

logger = logging.getLogger(__name__)


def get_local_tweets(source, limit):
    try:
        with open(source.file, "r") as fh:
            input_lines = fh.readlines()
    except (FileNotFoundError, PermissionError) as e:
        logger.debug(e)
        return []
    local_tweets = parse_string(input_lines, source)
    return sorted(local_tweets, reverse=True)[:limit]


def add_local_tweet(tweet, file):
    try:
        with open(file, "a") as fh:
            fh.write("{}\n".format(str(tweet)))
    except (FileNotFoundError, PermissionError) as e:
        logger.debug(e)
        return False
    
    try:
        with open(file+"-hashes", "a") as fh:
            fh.write("{}\n".format(str(hashlib.sha224(str(tweet.text).encode()).hexdigest())))
    except (FileNotFoundError, PermissionError) as e:
        logger.debug(e)
        return False
    return True

def check_hashes(tweet, file):
    try:
        with open(file+"-hashes", "r") as fh:
            lines = fh.read().splitlines()
            h = hashlib.sha224(str(tweet.text).encode()).hexdigest()
            if h in lines:
                return 1
            else:
                return 0
    except (FileNotFoundError, PermissionError) as e:
        logger.debug(e)
        return -1
        
