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
import textwrap

import click
import pkg_resources

from twtxt.mentions import format_mentions
from twtxt.parser import parse_iso8601


def style_timeline(tweets, porcelain=False):
    if porcelain:
        return "\n".join(style_tweet(tweet, porcelain) for tweet in tweets)
    else:
        return "\n{0}\n".format("\n\n".join(style_tweet(tweet, porcelain) for tweet in tweets))


def style_tweet(tweet, porcelain=False):
    conf = click.get_current_context().obj["conf"]
    limit = conf.character_limit

    if porcelain:
        return "{nick}\t{url}\t{tweet}".format(
            nick=tweet.source.nick,
            url=tweet.source.url,
            tweet=str(tweet))
    else:
        styled_text = format_mentions(tweet.text)
        len_styling = len(styled_text) - len(click.unstyle(styled_text))
        final_text = textwrap.shorten(styled_text, limit + len_styling) if limit else styled_text
        return "➤ {nick} ({time}):\n{tweet}".format(
            nick=click.style(tweet.source.nick, bold=True),
            tweet=final_text,
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
            raise click.BadParameter("{0}.".format(e))


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


def run_pre_tweet_hook(hook, options):
    try:
        command = shlex.split(hook.format(**options))
    except KeyError:
        click.echo("✗ Invalid variables in pre_tweet_hook.")
        return False
    return not subprocess.call(command, shell=True, stdout=subprocess.PIPE)


def run_post_tweet_hook(hook, options):
    try:
        command = shlex.split(hook.format(**options))
    except KeyError:
        click.echo("✗ Invalid variables in post_tweet_hook.")
        return False
    return not subprocess.call(command, shell=True, stdout=subprocess.PIPE)


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


def generate_user_agent():
    try:
        version = pkg_resources.require("twtxt")[0].version
    except pkg_resources.DistributionNotFound:
        version = "unknown"

    conf = click.get_current_context().obj["conf"]
    if conf.disclose_identity and conf.nick and conf.twturl:
        user_agent = "twtxt/{version} (+{url}; @{nick})".format(
            version=version, url=conf.twturl, nick=conf.nick)
    else:
        user_agent = "twtxt/{version}".format(version=version)

    return {"User-Agent": user_agent}
