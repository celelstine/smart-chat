import pytz


def timezone_exist(timezone):
    """
    check if a timezone exist
    """
    try:
        pytz.timezone(timezone)
        return True
    except pytz.exceptions.UnknownTimeZoneError:
        return False
