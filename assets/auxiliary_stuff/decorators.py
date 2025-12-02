import datetime
import time
from .. import root
import pygame as py

# Threshold in seconds: only logger timing info if function runs longer than this
TIMEIT_THRESHOLD = 0.005  # 5 ms

def logging(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        # Append a short one-line logger to avoid heavy I/O
        try:
            logging_info = f"{datetime.datetime.now()} Function '{func.__name__}' called with args: {args}, kwargs: {kwargs}. Returned: {result}"
            with open("data/logs.txt", "a", encoding="utf-8") as f:
                f.write(logging_info + "\n")
        except Exception:
            pass
        return result
    return wrapper

def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        # Only logger timing info if it exceeds the threshold
        if execution_time >= TIMEIT_THRESHOLD:
            try:
                root.logger.time(f"function '{func.__name__}' executed in {execution_time:.6f} seconds.", f"{func.__module__}.{func.__name__}")
            except Exception: pass
        return result
    return wrapper