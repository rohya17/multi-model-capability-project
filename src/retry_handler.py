import time
from functools import wraps

from openai import(
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    InternalServerError,
)

from src.config import config

def retry(func):
    """
    Retry decorator for OpenAI API calls.
    
        Retries on:
        - Rate Limit
        - Timeout
        - Connection Error
        - Internal Server Error
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        max_retries = config.RETRY["max_retries"]

        base_delay = config.RETRY["base_delay"]

        exponential_backoff = config.RETRY["exponential_backoff"]

        for attempt in range(max_retries):

            try:
                return func(*args, **kwargs)

            except(
                APIConnectionError,
                APITimeoutError,
                RateLimitError,
                InternalServerError,
            ) as e :

                if attempt == max_retries - 1:
                    raise e

                if exponential_backoff:
                    sleep_time = base_delay * (2 ** attempt)
                else:
                    sleep_time = base_delay

                print(
                    f"[Retry {attempt + 1} / {max_retries}]"
                    f"{type(e).__name__}. "
                    f"Retrying in {sleep_time} seconds..."
                )

                time.sleep(sleep_time)

    return wrapper