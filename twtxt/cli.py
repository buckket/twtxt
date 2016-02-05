"""
    twtxt.cli
    ~~~~~~~~~

    This module implements the command-line interface of twtxt.

    :copyright: (c) 2016 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import logging

import click

from twtxt.config import Config
from twtxt.helper import style_tweet, style_source, style_source_with_status
from twtxt.helper import validate_created_at, validate_text
from twtxt.http import get_tweets, get_status
from twtxt.log import init_logging
from twtxt.types import Tweet, Source

logger = logging.getLogger(__name__)


@click.group()
@click.option("--config", "-c",
              type=click.Path(exists=True, readable=True, resolve_path=True),
              help="Specify a custom config file location.")
@click.option("--verbose", "-v",
              is_flag=True, default=False,
              help="Enable verbose output for debugging purposes.")
@click.version_option()
@click.pass_context
def cli(ctx, config, verbose):
    """Decentralised, minimalist microblogging service for hackers."""
    init_logging(debug=verbose)

    try:
        if config:
            conf = Config.from_file(config)
        else:
            conf = Config.discover()
    except ValueError:
        click.echo("Error loading config file.")
        if not config:
            if click.confirm("Do you want to run the twtxt quickstart wizard?", abort=True):
                raise NotImplemented

    ctx.default_map = conf.build_default_map()
    ctx.obj = {'conf': conf}


@cli.command()
@click.option("--created-at",
              callback=validate_created_at,
              help="ISO 8601 formatted datetime string to use in Tweet, instead of current time.")
@click.option("--output", "-o",
              type=click.Path(file_okay=True, writable=True, resolve_path=True),
              help="Location of twtxt file.")
@click.argument("text", callback=validate_text)
@click.pass_context
def tweet(ctx, created_at, output, text):
    """Append a new tweet to your twtxt file."""
    tweet = Tweet(text, created_at) if created_at else Tweet(text)
    with open(output, "a") as fh:
        fh.write("{}\n".format(str(tweet)))


@cli.command()
@click.option("--pager/--no-pager",
              is_flag=True,
              help="Use a pager to display content. (Default: False)")
@click.option("--limit", "-l",
              type=click.INT,
              help="Limit total number of shown tweets. (Default: 20)")
@click.pass_context
def timeline(ctx, pager, limit):
    """Retrieve your personal timeline."""
    sources = ctx.obj['conf'].following
    tweets = get_tweets(sources, limit)

    if pager:
        click.echo_via_pager("\n\n".join(
            (style_tweet(tweet) for tweet in tweets)))
    else:
        click.echo()
        for tweet in tweets:
            click.echo(style_tweet(tweet))
            click.echo()


@cli.command()
@click.option("--check",
              is_flag=True,
              help="Check if source URL is valid and readable.")
@click.pass_context
def following(ctx, check):
    """Return the list of sources you’re following."""
    sources = ctx.obj['conf'].following

    if check:
        sources = get_status(sources)
        for (source, status) in sources:
            click.echo(style_source_with_status(source, status))
    else:
        sources = sorted(sources, key=lambda source: source.nick)
        for source in sources:
            click.echo(style_source(source))


@cli.command()
@click.argument("nick")
@click.argument("url")
@click.pass_context
def follow(ctx, nick, url):
    """Add a new source to your followings."""
    source = Source(nick, url)
    ctx.obj['conf'].add_source(source)
    click.echo("✓ You’re now following {}.".format(
        click.style(source.nick, bold=True)))


@cli.command()
@click.argument("nick")
@click.pass_context
def unfollow(ctx, nick):
    """Remove an existing source from your followings."""
    ret_val = ctx.obj['conf'].remove_source_by_nick(nick)
    if ret_val:
        click.echo("✓ You’ve unfollowed {}.".format(
            click.style(nick, bold=True)))
    else:
        click.echo("✗ You’re not following {}.".format(
            click.style(nick, bold=True)))


@cli.command()
@click.pass_context
def quickstart(ctx):
    """Quickstart wizard for setting up twtxt."""
    pass


main = cli
