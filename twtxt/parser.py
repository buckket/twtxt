from twtxt.types import Tweet, Source

from itertools import islice


def parse_string(string, source, limit=None):
    tweets = []

    if limit:
        string = islice(string, limit)

    for line in string:
        try:
            parts = line.partition(':')
            timestamp = float(parts[0])
            text = parts[2][1:].rstrip()

            tweet = Tweet(text=text, timestamp=timestamp, source=source)
            tweets.append(tweet)

        except ValueError as e:
            pass

    return tweets
