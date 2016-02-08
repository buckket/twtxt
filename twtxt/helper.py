"""
    twtxt.helper
    ~~~~~~~~~~~~

    This module implements various helper for use in twtxt.

    :copyright: (c) 2016 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import re
import sys
import shlex
import subprocess
import textwrap

import click

from twtxt.parser import parse_iso8601


def style_tweet(tweet):
    return "➤ {nick} ({time}):\n{tweet}".format(
        nick=click.style(tweet.source.nick, bold=True),
        tweet=textwrap.shorten(format_mention(tweet.text), 140),
        time=click.style(tweet.relative_datetime, dim=True))


def style_source(source):
    return "➤ {nick} @ {url}".format(
        nick=click.style(source.nick, bold=True),
        url=source.url)


def style_source_with_status(source, status):
    if status == 200:
        scolor, smessage = "green", str(status)
    elif status:
        scolor, smessage = "red", str(status)
    else:
        scolor, smessage = "red", "ERROR"
    return "➤ {nick} @ {url} ({status})".format(
        nick=click.style(source.nick, bold=True, fg=scolor),
        url=source.url,
        status=click.style(smessage, fg=scolor))


def validate_created_at(ctx, param, value):
    if value:
        try:
            return parse_iso8601(value)
        except (ValueError, OverflowError) as e:
            raise click.BadParameter("{}.".format(e))


def validate_text(ctx, param, value):
    if isinstance(value, tuple):
        value = " ".join(value)

    if not value and not sys.stdin.isatty():
        value = click.get_text_stream("stdin").read()

    if value:
        value = value.strip()
        if len(value) > 140:
            click.confirm("✂ Warning: Tweet is longer than 140 characters. Are you sure?", abort=True)
        return value
    else:
        raise click.BadArgumentUsage("Text can’t be empty.")


def run_post_tweet_hook(hook, options):
    try:
        command = shlex.split(hook.format(**options))
    except KeyError:
        click.echo("✗ Invalid variables in post_tweet_hook.")
        return False
    subprocess.call(command, shell=True, stdout=subprocess.PIPE)


def sort_and_truncate_tweets(tweets, direction, limit):
    if direction == "descending":
        return sorted(tweets, reverse=True)[:limit]
    elif direction == "ascending":
        if limit < len(tweets):
            return sorted(tweets)[len(tweets) - limit:]
        else:
            return sorted(tweets)
    else:
        return []

mention_re = re.compile(r'@<(?:(?P<name>.*?)\s)?(?P<url>.*?://.*?)>')
short_mention_re = re.compile(r'@(?P<name>\S+)')


def expand_mention(text, embed_names=True):
    """ Searches the text for mentions in the format of @Mention and formats them to @<Mention url>
    """
    if embed_names:
        format = '@<{name} {url}>'
    else:
        format = '@<{url}>'

    def handle_mention(match):
        source = get_source_by_name(match.group(1))
        if source is None:
            return '@' + match.group(1)
        return format.format(name=source.nick,
                             url=source.url)

    return short_mention_re.sub(handle_mention, text)


def get_source_by_url(url):
    return next((source for source in click.get_current_context().obj["conf"].following if source.url == url), None)


def get_source_by_name(nick):
    return next((source for source in click.get_current_context().obj["conf"].following if source.nick == nick), None)


def format_mention(text, embedded_names=False):
    """ Decodes every mention in the format of @<Some Name http://url/to/twtxt.txt> to a more (human-)readable format
    """
    def handle_mention(match):
        name, url = match.groups()
        source = get_source_by_url(url)
        if source is not None and (not name or embedded_names is False):
            name = source.nick
            url = source.url
        return '@' + name
    return mention_re.sub(handle_mention, text)
