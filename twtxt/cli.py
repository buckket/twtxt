import click

from twtxt.types import Tweet, Source
from twtxt.config import Config
from twtxt.http import get_tweets, get_status
from twtxt.helper import style_tweet, style_source, style_source_with_status


@click.group()
@click.option("--config", "-c",
              type=click.Path(exists=True, readable=True),
              help="Specify config file location.")
@click.pass_context
def cli(ctx, config):
    """Decentralised, minimalist microblogging service for hackers."""
    try:
        if config:
            conf = Config.from_file(config)
        else:
            conf = Config.discover()
    except ValueError:
        click.echo("Error loading config file.")
        if not config:
            if click.confirm("Wann run quickstart?", abort=True):
                pass

    ctx.obj = {
        'conf': conf
    }


@cli.command()
@click.argument('text')
@click.pass_context
def tweet(ctx, text):
    """Add a new tweet to your twtxt file."""
    print(Tweet(text=text))


@cli.command()
@click.pass_context
def timeline(ctx):
    """Retrieve your personal timeline."""
    sources = ctx.obj['conf'].following
    tweets = get_tweets(sources)
    click.echo()
    for tweet in tweets:
        click.echo(style_tweet(tweet))
        click.echo()


@cli.command()
@click.option("--check",
              is_flag=True, default=False,
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
        sources = sorted(sources, key=lambda x: x.nick)
        for source in sources:
            click.echo(style_source(source))


@cli.command()
@click.pass_context
def follow(ctx):
    """Add a source."""
    pass


@cli.command()
@click.pass_context
def unfollow(ctx):
    """Remove a source."""
    pass


@cli.command()
def config():
    conf = Config.from_file('twtxtrc')
    #conf = Config.discover()
    print(conf.followings)
    print(conf.twtxt_file)

main = cli
