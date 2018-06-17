"""
    twtxt.twhttp
    ~~~~~~~~~~~~

    This module handles HTTP requests via aiohttp/asyncio.

    :copyright: (c) 2016-2017 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import asyncio
import logging
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from ssl import CertificateError

import aiohttp
import click
import humanize

from twtxt.helper import generate_user_agent
from twtxt.parser import parse_tweets

logger = logging.getLogger(__name__)


class SourceResponse:
    """A :class:`SourceResponse` contains information about a :class:`Source`’s HTTP request.

    :param int status_code: response status code
    :param str content_length: Content-Length header field
    :param str last_modified: Last-Modified header field
    """

    def __init__(self, status_code, content_length, last_modified):
        self.status_code = status_code
        self.content_length = content_length
        self.last_modified = last_modified

    @property
    def natural_content_length(self):
        return humanize.naturalsize(self.content_length)

    @property
    def natural_last_modified(self):
        last_modified = parsedate_to_datetime(self.last_modified)
        now = datetime.now(timezone.utc)
        tense = "from now" if last_modified > now else "ago"
        return "{0} {1}".format(humanize.naturaldelta(now - last_modified), tense)


@asyncio.coroutine
def retrieve_status(client, source):
    status = None
    try:
        response = yield from client.head(source.url)
        if response.headers.get("Content-Length"):
            content_length = response.headers.get("Content-Length")
        else:
            content_length = 0
        status = SourceResponse(status_code=response.status,
                                content_length=content_length,
                                last_modified=response.headers.get("Last-Modified"))
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
    headers['Accept'] = 'text/plain,*/*;q=0.8'

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


def get_remote_tweets(sources, limit=None, timeout=5.0, cache=None):
    conn = aiohttp.TCPConnector(use_dns_cache=True)
    headers = generate_user_agent()
    headers['Accept'] = 'text/plain,*/*;q=0.8'
    with aiohttp.ClientSession(connector=conn, headers=headers, conn_timeout=timeout) as client:
        loop = asyncio.get_event_loop()

        def start_loop(client, sources, limit, cache=None):
            return loop.run_until_complete(process_sources_for_file(client, sources, limit, cache))

        tweets = start_loop(client, sources, limit, cache)

    return tweets


def get_remote_status(sources, timeout=5.0):
    conn = aiohttp.TCPConnector(use_dns_cache=True)
    headers = generate_user_agent()
    headers['Accept'] = 'text/plain,*/*;q=0.8'
    with aiohttp.ClientSession(connector=conn, headers=headers, conn_timeout=timeout) as client:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(process_sources_for_status(client, sources))
    return result
