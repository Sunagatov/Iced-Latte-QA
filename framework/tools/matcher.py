import re


def is_timestamp_valid(timestamp: str, pattern: str) -> bool:
    """
    Function check if a given timestamp string matches a specified regular expression pattern.

    Args:
        timestamp: The timestamp string to be validated. This should be a string representing a date and/or time.
        pattern:   The regular expression pattern against which the timestamp is to be validated. The pattern should
                       be provided as a string.
    """
    return re.fullmatch(pattern, timestamp) is not None
