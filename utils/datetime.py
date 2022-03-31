import pytz
from datetime import datetime


def timezone_exist(timezone):
    """
    check if a timezone exist
    """
    try:
        pytz.timezone(timezone)
        return True
    except pytz.exceptions.UnknownTimeZoneError:
        return False


def get_timezone_utc_offset(timezone_name):
    """
    get the offset a time zone has from UTC
    """
    utc_naive_time = datetime.now()
    timezone = pytz.timezone(timezone_name)

    time_in_timezone = timezone.localize(utc_naive_time)
    return time_in_timezone.utcoffset().total_seconds() / 3600
