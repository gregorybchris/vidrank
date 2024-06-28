"""Datetime utilities."""

import time


def get_timestamp() -> int:
    """Get the current timestamp in milliseconds.

    Returns
    -------
    int: The current timestamp in milliseconds

    """
    return time.time_ns() // int(1e6)
