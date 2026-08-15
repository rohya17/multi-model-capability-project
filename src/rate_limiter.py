import time
from src.config import config

class RateLimiter:
    """
    Simple Requests Per Minute (RPM) rate limiter.
    """

    def __init__(self):
        self.requests_per_minute = config.RATE_LIMIT["requests_per_minute"]
        self.request_timestamps = []

    def wait_if_needed(self):
        current_time = time.time()

        # remove timestamps older than 60 seconds
        self.request_timestamps = [
            timestamp
            for timestamp in self.request_timestamps
            if current_time - timestamp < 60
        ]

        # if RPM limit reached, wait
        if len(self.request_timestamps) >= self.requests_per_minute:
            sleep_time = 60 - (current_time - self.request_timestamps[0])
            print(f"Rate limit reached. sleeping for {sleep_time:.2f} seconds...")

            time.sleep(sleep_time)

            # update current time and request array
            current_time = time.time()
            self.request_timestamps = [
                timestamp
                for timestamp in self.request_timestamps
                if current_time - timestamp < 60
            ]

        self.request_timestamps.append(time.time())

rate_limiter = RateLimiter()