import click


def style_tweet(tweet):
    return "➤ {nick} ({time}):\n{tweet}".format(
            nick=click.style(tweet.source.nick, bold=True),
            tweet=tweet.limited_text,
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
