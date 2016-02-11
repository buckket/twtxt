"""
    twtxt.twhttp
    ~~~~~~~~~~~~

    This module handles HTTP requests via aiohttp/asyncio.

    :copyright: (c) 2016 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import logging
import asyncio
import aiohttp

from .parser import parse_tweets

logger = logging.getLogger(__name__)


@asyncio.coroutine
def retrieve_status(source, timeout):
    status = None
    try:
        with aiohttp.Timeout(timeout):
            response = yield from aiohttp.head(source.url)
        status = response.status
        yield from response.release()
    except Exception as e:
        logger.debug(e)
    finally:
        return source, status


@asyncio.coroutine
def retrieve_file(source, limit, timeout):
    try:
        with aiohttp.Timeout(timeout):
            response = yield from aiohttp.get(source.url)
        content = yield from response.text()
    except Exception as e:
        logger.debug(e)
        return []
    if response.status == 200:
        tweets = parse_tweets(content.splitlines(), source)
        return sorted(tweets, reverse=True)[:limit]
    else:
        return []


@asyncio.coroutine
def process_sources_for_status(sources, timeout):
    g_status = []
    coroutines = [retrieve_status(source, timeout) for source in sources]
    for coroutine in asyncio.as_completed(coroutines):
        status = yield from coroutine
        g_status.append(status)
    return sorted(g_status, key=lambda x: x[0].nick)


@asyncio.coroutine
def process_sources_for_file(sources, limit, timeout):
    g_tweets = []
    coroutines = [retrieve_file(source, limit, timeout) for source in sources]
    for coroutine in asyncio.as_completed(coroutines):
        tweets = yield from coroutine
        g_tweets.extend(tweets)
    return sorted(g_tweets, reverse=True)[:limit]


def get_remote_tweets(sources, limit=None, timeout=5.0):
    loop = asyncio.get_event_loop()
    tweets = loop.run_until_complete(process_sources_for_file(sources, limit, timeout))
    return tweets


def get_remote_status(sources, timeout=5.0):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(process_sources_for_status(sources, timeout))
    return result
