"""
    twtxt.cli
    ~~~~~~~~~

    This module implements the command-line interface of twtxt.

    :copyright: (c) 2016 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import logging
import os
import subprocess
import sys
import textwrap

import click

from twtxt.config import Config
from twtxt.twfile import get_local_tweets, add_local_tweet
from twtxt.helper import run_post_tweet_hook
from twtxt.helper import sort_and_truncate_tweets
from twtxt.helper import style_timeline, style_source, style_source_with_status
from twtxt.helper import validate_created_at, validate_text
from twtxt.twhttp import get_remote_tweets, get_remote_status
from twtxt.log import init_logging
from twtxt.models import Tweet, Source

logger = logging.getLogger(__name__)


@click.group()
@click.option("--config", "-c",
              type=click.Path(exists=True, file_okay=True, readable=True, writable=True, resolve_path=True),
              help="Specify a custom config file location.")
@click.option("--verbose", "-v",
              is_flag=True, default=False,
              help="Enable verbose output for debugging purposes.")
@click.version_option()
@click.pass_context
def cli(ctx, config, verbose):
    """Decentralised, minimalist microblogging service for hackers."""
    init_logging(debug=verbose)

    if ctx.invoked_subcommand == "quickstart":
        return

    try:
        if config:
            conf = Config.from_file(config)
        else:
            conf = Config.discover()
    except ValueError:
        click.echo("✗ Config file not found or not readable. You may want to run twtxt quickstart.")
        sys.exit()

    ctx.default_map = conf.build_default_map()
    ctx.obj = {'conf': conf}


@cli.command()
@click.option("--created-at",
              callback=validate_created_at,
              help="ISO 8601 formatted datetime string to use in Tweet, instead of current time.")
@click.option("--twtfile", "-f",
              type=click.Path(file_okay=True, writable=True, resolve_path=True),
              help="Location of your twtxt file. (Default: twtxt.txt)")
@click.argument("text", callback=validate_text, nargs=-1)
@click.pass_context
def tweet(ctx, created_at, twtfile, text):
    """Append a new tweet to your twtxt file."""

    """spell check the tweet before sending, and let the user know!"""
    subprocessReturn = subprocess.check_output(["aspell", "-a"], input=text, universal_newlines=True)
    if subprocessReturn.find("&") != -1:
        click.echo("Theres a spelling mistake in your tweet:\n"+text+"\n")
        if not click.confirm("Would you like to send your tweet anyway?"):
            return

    tweet = Tweet(text, created_at) if created_at else Tweet(text)
    if not add_local_tweet(tweet, twtfile):
        click.echo("✗ Couldn’t write to file.")
    else:
        hook = ctx.obj["conf"].post_tweet_hook
        if hook:
            run_post_tweet_hook(hook, ctx.obj["conf"].options)


@cli.command()
@click.option("--pager/--no-pager",
              is_flag=True,
              help="Use a pager to display content. (Default: False)")
@click.option("--limit", "-l",
              type=click.INT,
              help="Limit total number of shown tweets. (Default: 20)")
@click.option("--twtfile", "-f",
              type=click.Path(exists=True, file_okay=True, readable=True, resolve_path=True),
              help="Location of your twtxt file. (Default: twtxt.txt")
@click.option("--ascending", "sorting", flag_value="ascending",
              help="Sort timeline in ascending order.")
@click.option("--descending", "sorting", flag_value="descending",
              help="Sort timeline in descending order. (Default)")
@click.option("--timeout", type=click.FLOAT,
              help="Maximum time requests are allowed to take. (Default: 5.0)")
@click.option("--porcelain", is_flag=True,
              help="Style output in an easy-to-parse format. (Default: False)")
@click.option("--source", "-s",
              help="Only show feed of the given source. (Can be nick or URL)")
@click.pass_context
def timeline(ctx, pager, limit, twtfile, sorting, timeout, porcelain, source):
    """Retrieve your personal timeline."""
    if source:
        source_obj = ctx.obj["conf"].get_follower_source_by_nick(source)
        if not source_obj:
            logger.debug("Not following {}, trying as URL".format(source))
            source_obj = Source(source, source)
        sources = [source_obj]
    else:
        sources = ctx.obj["conf"].following

    tweets = get_remote_tweets(sources, limit, timeout)

    if twtfile and not source:
        source = Source(ctx.obj["conf"].nick, ctx.obj["conf"].twturl, file=twtfile)
        tweets.extend(get_local_tweets(source, limit))

    tweets = sort_and_truncate_tweets(tweets, sorting, limit)

    if not tweets:
        return

    if pager:
        click.echo_via_pager(style_timeline(tweets, porcelain))
    else:
        click.echo(style_timeline(tweets, porcelain))


@cli.command()
@click.option("--pager/--no-pager",
              is_flag=True,
              help="Use a pager to display content. (Default: False)")
@click.option("--limit", "-l",
              type=click.INT,
              help="Limit total number of shown tweets. (Default: 20)")
@click.option("--ascending", "sorting", flag_value="ascending",
              help="Sort timeline in ascending order.")
@click.option("--descending", "sorting", flag_value="descending",
              help="Sort timeline in descending order. (Default)")
@click.option("--timeout", type=click.FLOAT,
              help="Maximum time requests are allowed to take. (Default: 5.0)")
@click.option("--porcelain", is_flag=True,
              help="Style output in an easy-to-parse format. (Default: False)")
@click.argument("source")
@click.pass_context
def view(ctx, pager, limit, sorting, timeout, porcelain, source):
    """Show feed of given source."""
    ctx.forward(timeline)


@cli.command()
@click.option("--check/--no-check",
              is_flag=True,
              help="Check if source URL is valid and readable. (Default: True)")
@click.option("--timeout", type=click.FLOAT,
              help="Maximum time requests are allowed to take. (Default: 5.0)")
@click.option("--porcelain", is_flag=True,
              help="Style output in an easy-to-parse format. (Default: False)")
@click.pass_context
def following(ctx, check, timeout, porcelain):
    """Return the list of sources you’re following."""
    sources = ctx.obj['conf'].following

    if check:
        sources = get_remote_status(sources, timeout)
        for (source, status) in sources:
            click.echo(style_source_with_status(source, status, porcelain))
    else:
        sources = sorted(sources, key=lambda source: source.nick)
        for source in sources:
            click.echo(style_source(source, porcelain))


@cli.command()
@click.argument("nick")
@click.argument("url")
@click.pass_context
def follow(ctx, nick, url):
    """Add a new source to your followings."""
    source = Source(nick, url)
    sources = ctx.obj['conf'].following

    if source.nick in (source.nick for source in sources):
        click.confirm("➤ You’re already following {}. Overwrite?".format(
            click.style(source.nick, bold=True)), default=False, abort=True)
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
    width = click.get_terminal_size()[0]
    width = width if width <= 79 else 79

    click.secho("twtxt - quickstart", fg="cyan")
    click.secho("==================", fg="cyan")
    click.echo()

    help = "This wizard will generate a basic configuration file for twtxt with all mandatory options set. " \
           "Have a look at the README.rst to get information about the other available options and their meaning."
    click.echo(textwrap.fill(help, width))

    click.echo()
    nick = click.prompt("➤ Please enter your desired nick", default=os.environ.get("USER", ""))
    twtfile = click.prompt("➤ Please enter the desired location for your twtxt file", "~/twtxt.txt", type=click.Path())

    click.echo()
    add_news = click.confirm("➤ Do you want to follow the twtxt news feed?", default=True)

    conf = Config(None)
    conf.create_config(nick, twtfile, add_news)
    open(os.path.expanduser(twtfile), 'a').close()

    click.echo()
    click.echo("✓ Created config file at '{}'.".format(click.format_filename(conf.config_file)))


main = cli
