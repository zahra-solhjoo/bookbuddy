from __future__ import annotations

import time
from functools import wraps


def retry(retries: int = 3, delay: float = 1.0):

    """
    Retry decorator for unstable operations
    (file IO, network, etc.)
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            last_error = None

            for attempt in range(1, retries + 1):

                try:

                    return func(*args, **kwargs)

                except (OSError, IOError):

                    last_error = e

                    if attempt < retries:

                        time.sleep(delay)

                    else:

                        raise last_error

        return wrapper

    return decorator