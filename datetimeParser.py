from dateparser import parse as parseDateTime
from pytimeparse import parse as parseTimeDelta


def parse_datetime(text: str):
    ret = parseDateTime(text)
    try:
        assert ret is not None
    except AssertionError:
        return None
    return ret


def parse_timedelta(text: str):
    ret = parseTimeDelta(text)
    try:
        assert ret is not None
    except AssertionError:
        return None
    return ret
