from datetime import datetime, timezone, timedelta
from dateutil.tz import tzoffset

import pytest

from twtxt.parser import make_aware, parse_iso8601, parse_string


def test_make_aware():
    aware = datetime.now(timezone.utc)
    unaware = aware.replace(tzinfo=None)
    assert make_aware(unaware) >= aware
    assert make_aware(aware) == aware


def test_parse_iso8601():
    as_string = "2016-02-05T02:52:15.030474+01:00"
    as_datetime = datetime(2016, 2, 5, 2, 52, 15, 30474, tzinfo=tzoffset(None, 3600))
    assert parse_iso8601(as_string) == as_datetime

    as_string = "2016-02-05T02:52:15"
    as_datetime = datetime(2016, 2, 5, 2, 52, 15, tzinfo=timezone.utc)
    assert parse_iso8601(as_string) == as_datetime

    with pytest.raises(ValueError) as e:
        parse_iso8601("foobar")
    assert "Unknown string format" in str(e.value)


def test_parse_string():
    pass
