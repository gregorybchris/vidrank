import time


def get_timestamp() -> int:
    return time.time_ns() // int(1e6)
