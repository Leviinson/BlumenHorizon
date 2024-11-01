from functools import wraps
from pprint import pprint
from typing import Callable

from django.db import connection, reset_queries


def inspect_db_queries(function: Callable):
    """
    To inspect method db queries.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        reset_queries()
        result = function(*args, **kwargs)
        print(
            f"Function: {function.__name__}",
            (f"Args: {args}" if args else ""),
            (f"Kwargs: {kwargs}" if kwargs else ""),
            sep="\n",
            end="\n\n",
        )
        print(f"Total queries: {len(connection.queries)}")
        pprint(connection.queries)
        print("\n\n")
        reset_queries()
        return result

    return wrapper
