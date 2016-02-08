"""
    twtxt.helper
    ~~~~~~~~~~~~

    This module implements various helper for use in twtxt.

    :copyright: (c) 2016 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import shlex
import subprocess
import sys

import click

from twtxt.parser import parse_iso8601


def style_timeline(tweets, porcelain=False):
    if porcelain:
        return "\n".join(style_tweet(tweet, porcelain) for tweet in tweets)
    else:
        return "\n{}\n".format("\n\n".join(style_tweet(tweet, porcelain) for tweet in tweets))


def style_tweet(tweet, porcelain=False):
    if porcelain:
        return "{nick}\t{url}\t{tweet}".format(
            nick=tweet.source.nick,
            url=tweet.source.url,
            tweet=str(tweet))
    else:
        return "➤ {nick} ({time}):\n{tweet}".format(
            nick=click.style(tweet.source.nick, bold=True),
            tweet=tweet.limited_text,
            time=click.style(tweet.relative_datetime, dim=True))


def style_source(source, porcelain=False):
    if porcelain:
        return "{nick}\t{url}".format(
            nick=source.nick,
            url=source.url)
    else:
        return "➤ {nick} @ {url}".format(
            nick=click.style(source.nick, bold=True),
            url=source.url)


def style_source_with_status(source, status, porcelain=False):
    if porcelain:
        return "{nick}\t{url}\t{status}".format(
            nick=source.nick,
            url=source.url,
            status=status)
    else:
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
