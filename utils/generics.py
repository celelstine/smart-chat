import re
import sre_constants


def matches_regex(pattern, text):
    try:
        regex = re.compile(pattern)
    except sre_constants.error:
        # probably send a error about the pattern
        return False
    return bool(re.fullmatch(regex, text))
