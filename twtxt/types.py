import time
import datetime
import textwrap

import humanize


class Tweet:

    def __init__(self, text, timestamp=time.time(), source=None):
        if text:
            self.text = text
        else:
            raise ValueError("empty text")

        self.timestamp = timestamp
        try:
            self.datetime = datetime.datetime.utcfromtimestamp(timestamp)
        except (OverflowError, ValueError, OSError, TypeError):
            raise ValueError("invalid timestamp")

        self.source = source

    def _is_valid_operand(self, other):
        return (hasattr(other, "text") and
                hasattr(other, "timestamp"))

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.timestamp < other.timestamp

    def __le__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.timestamp < other.timestamp or (self.timestamp == other.timestamp and self.text == other.text)

    def __gt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.timestamp > other.timestamp

    def __ge__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.timestamp > other.timestamp or (self.timestamp == other.timestamp and self.text == other.text)

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.timestamp == other.timestamp and self.text == other.text

    def __str__(self):
        return "{timestamp:.0f}: {text}".format(timestamp=self.timestamp,
                                                text=self.text)

    @property
    def relative_datetime(self):
        return "{} ago".format(humanize.naturaldelta(datetime.datetime.utcnow() - self.datetime))

    @property
    def limited_text(self):
        return textwrap.shorten(self.text, 140)


class Source:

    def __init__(self, nick, url):
        self.nick = nick
        self.url = url
