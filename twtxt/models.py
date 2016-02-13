"""
    twtxt.models
    ~~~~~~~~~~~~

    This module implements the main models used in twtxt.

    :copyright: (c) 2016 by buckket.
    :license: MIT, see LICENSE for more details.
"""

import textwrap
from datetime import datetime, timezone
from dateutil.tz import tzlocal

import humanize


class Tweet:
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
        now = datetime.now(timezone.utc)
        tense = "from now" if self.created_at > now else "ago"
        return "{} {}".format(humanize.naturaldelta(now - self.created_at), tense)

    @property
    def limited_text(self):
        return textwrap.shorten(self.text, 140)


class Source:
    def __init__(self, nick, url=None, file=None):
        self.nick = nick.lower()
        self.url = url
        self.file = file
