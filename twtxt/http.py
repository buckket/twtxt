"""
    twtxt.http
    ~~~~~~~~~~

    This module handles HTTP requests via aiohttp/asyncio.

    :copyright: (c) 2016 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import asyncio
import logging
from itertools import islice

import aiohttp

from twtxt.parser import parse_string

logger = logging.getLogger(__name__)


@asyncio.coroutine
def retrieve_status(source):
    status = None
    try:
        response = yield from aiohttp.head(source.url)
        status = response.status
        yield from response.release()
    except Exception as e:
        logger.debug(e)
    finally:
        return source, status


@asyncio.coroutine
def retrieve_file(source, limit):
    try:
        response = yield from aiohttp.get(source.url)
        content = yield from response.text()
    except Exception as e:
        logger.debug(e)
        return []
    if response.status == 200:
        tweets = parse_string(content.splitlines(), source, limit)
        return tweets
    else:
        return []


@asyncio.coroutine
def process_sources_for_status(sources):
    g_status = []
    coroutines = [retrieve_status(source) for source in sources]
    for coroutine in asyncio.as_completed(coroutines):
        status = yield from coroutine
        g_status.append(status)
    return sorted(g_status, key=lambda x: x[0].nick)


@asyncio.coroutine
def process_sources_for_file(sources, limit):
    g_tweets = []
    coroutines = [retrieve_file(source, limit) for source in sources]
    for coroutine in asyncio.as_completed(coroutines):
        tweets = yield from coroutine
        g_tweets.extend(tweets)
    return sorted(g_tweets, reverse=True)


def get_tweets(sources, limit=None):
    loop = asyncio.get_event_loop()
    tweets = loop.run_until_complete(process_sources_for_file(sources, limit))
    return islice(tweets, limit) if limit else tweets


def get_status(sources):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(process_sources_for_status(sources))
    return result
