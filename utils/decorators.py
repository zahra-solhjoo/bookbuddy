from __future__ import annotations

from functools import wraps
from time import perf_counter

from config.logger import logger


def log_execution(func):
    """
    Decorator that logs function execution time.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        logger.info(f"Running '{func.__name__}'")

        start = perf_counter()

        try:

            result = func(*args, **kwargs)

            elapsed = perf_counter() - start

            logger.info(
                f"'{func.__name__}' completed "
                f"in {elapsed:.4f} seconds."
            )

            return result

        except Exception as exc:

            logger.exception(
                f"Error in '{func.__name__}': {exc}"
            )

            raise

    return wrapper


def log_method_call(func):
    """
    Logs class method calls.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):

        logger.info(
            f"{self.__class__.__name__}.{func.__name__}() called"
        )

        return func(self, *args, **kwargs)

    return wrapper


def validate_positive_number(argument_index: int):
    """
    Validates that a positional argument is greater than zero.

    Example:
        @validate_positive_number(1)
        def update_progress(self, pages):
            ...
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            value = args[argument_index]

            if value <= 0:
                raise ValueError(
                    "Value must be greater than zero."
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator