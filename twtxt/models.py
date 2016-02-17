"""
    twtxt.models
    ~~~~~~~~~~~~

    This module implements the main models used in twtxt.

    :copyright: (c) 2016 by buckket.
    :license: MIT, see LICENSE for more details.
"""

from datetime import datetime, timezone

import humanize
from dateutil.tz import tzlocal


class Tweet:
    """A :class:`Tweet` represents a single tweet.

    :param str text: text of the tweet in raw format
    :param ~datetime.datetime created_at: (optional) when the tweet was created, defaults to :meth:`~datetime.datetime.now` when no value is given
    :param Source source: (optional) the :class:`Source` the tweet is from
    """

    def __init__(self, text, created_at=None, source=None):
        if text:
            self.text = text
        else:
            raise ValueError("empty text")

        if created_at is None:
            created_at = datetime.now(tzlocal())

        try:
            self.created_at = created_at.replace(microsecond=0)
        except AttributeError:
            raise TypeError("created_at is of invalid type")

        self.source = source

    @staticmethod
    def _is_valid_operand(other):
        return (hasattr(other, "text") and
                hasattr(other, "created_at"))

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.created_at < other.created_at

    def __le__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.created_at < other.created_at or (self.created_at == other.created_at and self.text == other.text)

    def __gt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.created_at > other.created_at

    def __ge__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.created_at > other.created_at or (self.created_at == other.created_at and self.text == other.text)

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.created_at == other.created_at and self.text == other.text

    def __str__(self):
        return "{created_at}\t{text}".format(created_at=self.created_at.isoformat(), text=self.text)

    @property
    def relative_datetime(self):
        """Return human-readable relative time string."""
        now = datetime.now(timezone.utc)
        tense = "from now" if self.created_at > now else "ago"
        return "{0} {1}".format(humanize.naturaldelta(now - self.created_at), tense)

    @property
    def absolute_datetime(self):
        """Return human-readable absolute time string."""
        return self.created_at.strftime("%a, %d %b %Y %H:%M:%S")


class Source:
    """A :class:`Source` represents a twtxt feed, remote as well as local.

    :param str nick: nickname of twtxt user
    :param str url: URL to remote twtxt file
    :param str file: path to local twtxt file
    """

    def __init__(self, nick, url=None, file=None):
        self.nick = nick.lower()
        self.url = url
        self.file = file
