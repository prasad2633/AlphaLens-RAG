import time
import random
from functools import wraps
from google.genai import errors


def retry_on_failure(max_retries=5):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            for attempt in range(max_retries):

                try:
                    return func(*args, **kwargs)

                except errors.ServerError as e:

                    wait_time = (2**attempt) + random.uniform(0, 1)

                    print(
                        f"Retrying {func.__name__} "
                        f"({attempt+1}/{max_retries}) "
                        f"in {wait_time:.2f}s"
                    )

                    time.sleep(wait_time)

            raise Exception(f"{func.__name__} failed after " f"{max_retries} retries")

        return wrapper

    return decorator
