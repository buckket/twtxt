"""
    twtxt.helper
    ~~~~~~~~~~~~

    This module implements various helper for use in twtxt.

    :copyright: (c) 2016-2022 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import shlex
import subprocess
import sys
import textwrap

import click

from twtxt.mentions import format_mentions
from twtxt.parser import parse_iso8601


def style_timeline(tweets, porcelain=False):
    if porcelain:
        return "\n".join(style_tweet(tweet, porcelain) for tweet in tweets)
    else:
        return "\n{0}\n".format("\n\n".join(filter(None, (style_tweet(tweet, porcelain) for tweet in tweets))))


def style_tweet(tweet, porcelain=False):
    conf = click.get_current_context().obj["conf"]
    limit = conf.character_limit

    if porcelain:
        return "{nick}\t{url}\t{tweet}".format(
            nick=tweet.source.nick,
            url=tweet.source.url,
            tweet=str(tweet))
    else:
        if sys.stdout.isatty() and not tweet.text.isprintable():
            return None
        styled_text = format_mentions(tweet.text)
        len_styling = len(styled_text) - len(click.unstyle(styled_text))
        final_text = textwrap.shorten(styled_text, limit + len_styling) if limit else styled_text
        timestamp = tweet.absolute_datetime if conf.use_abs_time else tweet.relative_datetime
        return "➤ {nick} ({time}):\n{tweet}".format(
            nick=click.style(tweet.source.nick, bold=True),
            tweet=final_text,
            time=click.style(timestamp, dim=True))


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
        return "{nick}\t{url}\t{status}\t{content_length}\t{last_modified}".format(
            nick=source.nick,
            url=source.url,
            status=status.status_code,
            content_length=status.content_length,
            last_modified=status.last_modified)
    else:
        if hasattr(status, "status_code") and status.status_code == 200:
            scolor, smessage = "green", str(status.status_code)
        elif status:
            scolor, smessage = "red", str(status.status_code)
        else:
            scolor, smessage = "red", "ERROR"
        return "➤ {nick} @ {url} [{content_length}, {last_modified}] ({status})".format(
            nick=click.style(source.nick, bold=True, fg=scolor),
            url=source.url,
            status=click.style(smessage, fg=scolor),
            content_length=status.natural_content_length,
            last_modified=status.natural_last_modified)


def validate_created_at(ctx, param, value):
    if value:
        try:
            return parse_iso8601(value)
        except (ValueError, OverflowError) as e:
            raise click.BadParameter("{0}.".format(e))


def validate_text(ctx, param, value):
    conf = click.get_current_context().obj["conf"]
    if isinstance(value, tuple):
        value = " ".join(value)

    if not value and not sys.stdin.isatty():
        value = click.get_text_stream("stdin").read()

    if value:
        value = value.strip()
        if conf.character_warning and len(value) > conf.character_warning:
            click.confirm("✂ Warning: Tweet is longer than {0} characters. Are you sure?".format(
                conf.character_warning), abort=True)
        return value
    else:
        raise click.BadArgumentUsage("Text can’t be empty.")


def validate_config_key(ctx, param, value):
    """Validate a configuration key according to `section.item`."""
    if not value:
        return value

    try:
        section, item = value.split(".", 1)
    except ValueError:
        raise click.BadArgumentUsage("Given key does not contain a section name.")
    else:
        return section, item


def run_pre_tweet_hook(hook, options):
    try:
        command = shlex.split(hook.format(**options))
    except KeyError:
        click.echo("✗ Invalid variables in pre_tweet_hook.")
        raise click.Abort
    try:
        subprocess.check_output(command, shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        click.echo("✗ pre_tweet_hook returned {}.".format(e.returncode))
        if e.output:
            click.echo(e.output)
        raise click.Abort


def run_post_tweet_hook(hook, options):
    try:
        command = shlex.split(hook.format(**options))
    except KeyError:
        click.echo("✗ Invalid variables in post_tweet_hook.")
        return
    try:
        subprocess.check_output(command, shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        click.echo("✗ post_tweet_hook returned {}.".format(e.returncode))
        if e.output:
            click.echo(e.output)


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
    from twtxt import __version__ as version

    conf = click.get_current_context().obj["conf"]
    if conf.disclose_identity and conf.nick and conf.twturl:
        user_agent = "twtxt/{version} (+{url}; @{nick})".format(
            version=version, url=conf.twturl, nick=conf.nick)
    else:
        user_agent = "twtxt/{version}".format(version=version)

    return {"User-Agent": user_agent}
