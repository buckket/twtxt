import pytest
from datetime import datetime, timezone

from twtxt.types import Source
from twtxt.parser import parse_tweet, parse_tweets


def test_parse_tweet():
    """Test parsing single tweet line"""
    source = Source("foo", "bar")
    raw_line = "2016-02-08T00:00:00\tHallo"
    tweet = parse_tweet(raw_line, source)
    assert tweet.text == "Hallo"
    assert tweet.created_at == datetime(year=2016, month=2, day=8, tzinfo=timezone.utc)

    with pytest.raises(ValueError):
        raw_line = "3000-02-08T00:00:00\tHallo"
        parse_tweet(raw_line, source)


def test_parse_tweets():
    """Test parsing multiple tweet lines"""
    source = Source("foo", "bar")
    raw_tweets = [
        "2016-02-08T00:00:00\tHallo",
        "2016-02-08T00:00:00\tBar\n",
        "2016-02-08T00:00:00\tFoo"
    ]
    tweets = parse_tweets(raw_tweets, source)
    assert len(tweets) == 3
