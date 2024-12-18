from functools import wraps
import requests
import time

# TODO: 📋 remove print with logger
# TODO: 📋 Use config file to inject default parameters for `retry_on_500` ?


def retry_on_500(retries=2, delay=3):
    """
    Wrapped function to retry wrapped function when catching 500
    :param retries: Number of times to retry the wrapped function
    :param delay: Number of second to wait for between each try
    :return:
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    # Call the original function
                    return func(*args, **kwargs)
                except requests.HTTPError as e:
                    # Check if the status code is 500
                    if e.response.status_code == 500:
                        attempt += 1
                        print(f"Error: {e}\nAttempt {attempt} failed with status 500. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        # If it's not a 500 error, raise it immediately
                        raise
            # If we reach here, it means all retries have failed
            print("All retries failed.")
            raise

        return wrapper

    return decorator
