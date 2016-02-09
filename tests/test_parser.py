from datetime import datetime, timezone

import pytest
from dateutil.tz import tzoffset

from twtxt.parser import make_aware, parse_iso8601
from twtxt.parser import parse_tweet, parse_tweets
from twtxt.models import Source


def test_make_aware():
    """Test making unaware datetime objects tzinfo aware."""
    aware = datetime.now(timezone.utc)
    unaware = aware.replace(tzinfo=None)
    assert make_aware(unaware) >= aware
    assert make_aware(aware) == aware


def test_parse_iso8601():
    """Test parsing ISO-8601 date/time strings."""
    as_string = "2016-02-05T02:52:15.030474+01:00"
    as_datetime = datetime(2016, 2, 5, 2, 52, 15, 30474, tzinfo=tzoffset(None, 3600))
    assert parse_iso8601(as_string) == as_datetime

    as_string = "2016-02-05T02:52:15"
    as_datetime = datetime(2016, 2, 5, 2, 52, 15, tzinfo=timezone.utc)
    assert parse_iso8601(as_string) == as_datetime

    with pytest.raises(ValueError) as e:
        parse_iso8601("foobar")
    assert "Unknown string format" in str(e.value)


def test_parse_tweet():
    """Test parsing single tweet line."""
    source = Source("foo", "bar")
    raw_line = "2016-02-08T00:00:00\tHallo"
    tweet = parse_tweet(raw_line, source)
    assert tweet.text == "Hallo"
    assert tweet.created_at == datetime(year=2016, month=2, day=8, tzinfo=timezone.utc)

    with pytest.raises(ValueError) as e:
        raw_line = "3000-02-08T00:00:00\tHallo"
        parse_tweet(raw_line, source)
    assert "Tweet is from the future" in str(e.value)


def test_parse_tweets():
    """Test parsing multiple tweet lines"""
    source = Source("foo", "bar")
    raw_tweets = [
        "2016-02-08T00:00:00\tHallo",
        "2016-02-08T00:00:00\tBar\n",
        "2016-02-08T00:00:00\tFoo\n",
        "3000-02-08T00:00:00\tHallo\n",
    ]
    tweets = parse_tweets(raw_tweets, source)
    assert len(tweets) == 3
