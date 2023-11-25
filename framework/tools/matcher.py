import re


def is_timestamp_valid(timestamp, pattern):
    """
    Function check if a given timestamp string matches a specified regular expression pattern.

    Args:
        timestamp (str):The timestamp string to be validated. This should be a string representing a date and/or time.
        pattern (str):The regular expression pattern against which the timestamp is to be validated. The pattern should
                       be provided as a string.
    Returns:
          bool: True if the timestamp matches the entire pattern, False otherwise.
    """
    return re.fullmatch(pattern, timestamp) is not None
