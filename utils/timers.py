import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start} sec")
        return result

    return wrapper


def async_timer(async_func):
    @wraps(async_func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await async_func(*args, **kwargs)
        print(f"{async_func.__name__} took {time.perf_counter() - start} sec")
        return result

    return wrapper
