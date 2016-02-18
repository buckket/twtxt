import pytest
from datetime import datetime, timezone, timedelta

from twtxt.models import Tweet, Source


def test_source():
    source = Source("foo", "bar")
    assert source.nick == "foo"
    assert source.url == "bar"

    with pytest.raises(TypeError):
        Source()


def test_tweet_init():
    with pytest.raises(ValueError) as e:
        Tweet("")
    assert "empty text" in str(e.value)

    with pytest.raises(TypeError) as e:
        Tweet("foobar", 0)
    assert "created_at is of invalid type" in str(e.value)

    source = Source("foo", "bar")
    created_at = datetime.now(timezone.utc)
    tweet = Tweet("foobar", created_at, source)
    assert tweet.text == "foobar"
    assert tweet.created_at == created_at.replace(microsecond=0)
    assert tweet.source == source


def test_tweet_str():
    tweet = Tweet("foobar", datetime(2000, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc))
    assert str(tweet) == "2000-01-01T01:01:01+00:00\tfoobar"


def test_tweet_relative_datetime():
    tweet = Tweet("foobar")
    assert tweet.relative_datetime == "a moment ago"

    tweet = Tweet("foobar", datetime.now(timezone.utc) + timedelta(hours=1, minutes=1))
    assert tweet.relative_datetime == "an hour from now"

    tweet = Tweet("foobar", datetime.now(timezone.utc) - timedelta(hours=1, minutes=1))
    assert tweet.relative_datetime == "an hour ago"


def test_tweet_absolute_datetime():
    tweet = Tweet("foobar", datetime(2000, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc))
    assert tweet.absolute_datetime == "Sat, 01 Jan 2000 01:01:01"


def test_tweet_ordering():
    now = datetime.now(timezone.utc)
    tweet_1 = Tweet("A", now)
    tweet_2 = Tweet("B", now + timedelta(hours=1))
    tweet_3 = Tweet("C", now + timedelta(hours=2))
    tweet_4 = Tweet("D", now + timedelta(hours=2))
    tweet_5 = Tweet("D", now + timedelta(hours=2))

    source = Source("foo", "bar")

    # explicit testing
    with pytest.raises(TypeError):
        tweet_1 < source

    with pytest.raises(TypeError):
        tweet_1 <= source

    with pytest.raises(TypeError):
        tweet_1 > source

    with pytest.raises(TypeError):
        tweet_1 >= source

    assert tweet_1 != source

    assert tweet_1 < tweet_2
    assert tweet_1 <= tweet_2
    assert tweet_2 > tweet_1
    assert tweet_2 >= tweet_1
    assert tweet_3 != tweet_4
    assert tweet_5 == tweet_4
    assert tweet_5 >= tweet_4
    assert tweet_5 <= tweet_4
    assert not(tweet_3 <= tweet_4)
    assert not(tweet_3 >= tweet_4)
