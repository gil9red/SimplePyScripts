#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from functools import wraps
from typing import Any, Callable


def ttl_cache(ttl_seconds: int) -> Callable:
    """
    A decorator that caches the results of a function for a specified time (TTL).
    """
    cache: dict[Any, Any] = dict()

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a unique key for the cache based on function arguments
            key = (args, frozenset(kwargs.items()))

            # Check if the result is in the cache and still valid
            if key in cache:
                cached_time, cached_result = cache[key]
                if time.time() - cached_time < ttl_seconds:
                    return cached_result

            # If not in cache or expired, call the original function
            result = func(*args, **kwargs)
            # Store the result with the current timestamp
            cache[key] = (time.time(), result)
            return result

        return wrapper

    return decorator


if __name__ == "__main__":
    # Example usage:
    @ttl_cache(ttl_seconds=5)
    def get_data(item_id):
        print(f"Fetching data for item_id: {item_id} (expensive operation)...")
        time.sleep(1)  # Simulate a slow operation
        return f"Data for {item_id} at {time.time()}"

    print(get_data(1))  # First call, fetches data
    print(get_data(1))  # Second call within 5 seconds, uses cache
    print(get_data(1))  # Third call within 5 seconds, uses cache
    print(get_data(1))  # Fourth call within 5 seconds, uses cache

    print()

    time.sleep(6)  # Wait for cache to expire
    print(get_data(1))  # Third call after 5 seconds, fetches data again
