import pytest

from twtxt.types import Tweet, Source


def test_source():
    source = Source("foo", "bar")
    assert source.nick == "foo"
    assert source.url == "bar"

    with pytest.raises(TypeError):
        source = Source()


def test_tweet_init():
    with pytest.raises(ValueError) as e:
        tweet = Tweet("", 1454334870)
    assert "empty text" in str(e.value)

    with pytest.raises(ValueError) as e:
        tweet = Tweet("foobar", "invalid")
    assert "invalid timestamp" in str(e.value)

    with pytest.raises(ValueError) as e:
        tweet = Tweet("foobar", 900000000000)
    assert "invalid timestamp" in str(e.value)

    source = Source("foo", "bar")
    tweet = Tweet("foobar", 1454334870, source)
    assert tweet.text == "foobar"
    assert tweet.timestamp == 1454334870
    assert tweet.source == source


def test_tweet_relative_datetime():
    tweet = Tweet("foobar")
    assert tweet.relative_datetime == "a moment ago"

    # test future


def test_tweet_limited_text():
    tweet = Tweet("A " * 100)
    assert tweet.text == "A " * 100
    assert len(tweet.limited_text) <= 140


def test_tweet_ordering():
    tweet_1 = Tweet("A", 1454493697)
    tweet_2 = Tweet("B", 1454493698)
    tweet_3 = Tweet("C", 1454493699)
    tweet_4 = Tweet("D", 1454493699)
    tweet_5 = Tweet("D", 1454493699)

    # explicit testing
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
