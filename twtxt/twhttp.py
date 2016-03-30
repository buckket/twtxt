"""
    twtxt.twhttp
    ~~~~~~~~~~~~

    This module handles HTTP requests via aiohttp/asyncio.

    :copyright: (c) 2016 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import asyncio
import logging
from ssl import CertificateError

import aiohttp
import click

from twtxt.cache import Cache
from twtxt.helper import generate_user_agent
from twtxt.parser import parse_tweets

logger = logging.getLogger(__name__)


@asyncio.coroutine
def retrieve_status(client, source):
    status = None
    try:
        response = yield from client.head(source.url)
        status = response.status
        yield from response.release()
    except CertificateError as e:
        click.echo("✗ SSL Certificate Error: The feed's ({0}) SSL certificate is untrusted. Try using HTTP, "
                   "or contact the feed's owner to report this issue.".format(source.url))
        logger.debug("{0}: {1}".format(source.url, e))
    except Exception as e:
        logger.debug("{0}: {1}".format(source.url, e))
    finally:
        return source, status


@asyncio.coroutine
def retrieve_file(client, source, limit, cache):
    is_cached = cache.is_cached(source.url) if cache else None
    headers = {"If-Modified-Since": cache.last_modified(source.url)} if is_cached else {}

    try:
        response = yield from client.get(source.url, headers=headers)
        content = yield from response.text()
    except Exception as e:
        if is_cached:
            logger.debug("{0}: {1} - using cached content".format(source.url, e))
            return cache.get_tweets(source.url, limit)
        else:
            logger.debug("{0}: {1}".format(source.url, e))
            return []

    if response.status == 200:
        tweets = parse_tweets(content.splitlines(), source)

        if cache:
            last_modified_header = response.headers.get("Last-Modified")
            if last_modified_header:
                logger.debug("{0} returned 200 and Last-Modified header - adding content to cache".format(source.url))
                cache.add_tweets(source.url, last_modified_header, tweets)
            else:
                logger.debug("{0} returned 200 but no Last-Modified header - can’t cache content".format(source.url))
        else:
            logger.debug("{0} returned 200".format(source.url))

        return sorted(tweets, reverse=True)[:limit]

    elif response.status == 410 and is_cached:
        # 410 Gone:
        # The resource requested is no longer available,
        # and will not be available again.
        logger.debug("{0} returned 410 - deleting cached content".format(source.url))
        cache.remove_tweets(source.url)
        return []

    elif is_cached:
        logger.debug("{0} returned {1} - using cached content".format(source.url, response.status))
        return cache.get_tweets(source.url, limit)

    else:
        logger.debug("{0} returned {1}".format(source.url, response.status))
        return []


@asyncio.coroutine
def process_sources_for_status(client, sources):
    g_status = []
    coroutines = [retrieve_status(client, source) for source in sources]
    for coroutine in asyncio.as_completed(coroutines):
        status = yield from coroutine
        g_status.append(status)
    return sorted(g_status, key=lambda x: x[0].nick)


@asyncio.coroutine
def process_sources_for_file(client, sources, limit, cache=None):
    g_tweets = []
    coroutines = [retrieve_file(client, source, limit, cache) for source in sources]
    for coroutine in asyncio.as_completed(coroutines):
        tweets = yield from coroutine
        g_tweets.extend(tweets)
    return sorted(g_tweets, reverse=True)[:limit]


def get_remote_tweets(sources, limit=None, timeout=5.0, use_cache=True):
    conn = aiohttp.TCPConnector(conn_timeout=timeout, use_dns_cache=True)
    headers = generate_user_agent()
    with aiohttp.ClientSession(connector=conn, headers=headers) as client:
        loop = asyncio.get_event_loop()

        def start_loop(client, sources, limit, cache=None):
            return loop.run_until_complete(process_sources_for_file(client, sources, limit, cache))

        if use_cache:
            try:
                with Cache.discover() as cache:
                    tweets = start_loop(client, sources, limit, cache)
            except OSError as e:
                logger.debug(e)
                tweets = start_loop(client, sources, limit)
        else:
            tweets = start_loop(client, sources, limit)

    return tweets


def get_remote_status(sources, timeout=5.0):
    conn = aiohttp.TCPConnector(conn_timeout=timeout, use_dns_cache=True)
    headers = generate_user_agent()
    with aiohttp.ClientSession(connector=conn, headers=headers) as client:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(process_sources_for_status(client, sources))
    return result
