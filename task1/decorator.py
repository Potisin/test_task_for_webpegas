import time
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def retry_on_exception(exceptions, max_attempts=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logging.error(f"Attempt {attempts} failed with error: {e}")
                        raise
                    time.sleep(1)

        return wrapper

    return decorator


@retry_on_exception([ValueError, TypeError, ZeroDivisionError], max_attempts=3)
def test_function(x, y):
    return x / y


try:
    result = test_function(5, 0)
except Exception as e:
    result = str(e)
