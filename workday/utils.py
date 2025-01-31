from functools import wraps
from typing import List, Optional
import pandas as pd
from datetime import datetime, timedelta

import requests
import time

# TODO: 📋 remove print with logger
# TODO: 📋 Use config file to inject default parameters for `retry_on_500` ?


def retry_on_500(retries=2, delay=5):
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


def transform_list_to_dict(data: List[str]):
    return {d: True for d in data}


def transform_and_adjust_date(date_string: str, days: Optional[int] = 0) -> datetime.date:
    """
    Transforms an ISO 8601 formatted string with timezone information into a date object
    and adjusts the date by adding or subtracting a specified number of days.

    :param date_string: The date string to transform (e.g., "2025-01-17T08:18:29.400-08:00").
    :param days: The number of days to add (positive) or subtract (negative).
    :return: The adjusted datetime.date object.
    """
    # Parse the ISO 8601 string into a datetime object
    datetime_obj = datetime.fromisoformat(date_string)
    # Adjust the date by adding or subtracting the specified number of days
    adjusted_date = datetime_obj.date() + timedelta(days=days)
    return adjusted_date


def is_timestamp_on_date(timestamp: str, target_date: str) -> bool:
    """
    Checks if a given timestamp belongs to a specific target date.

    :param timestamp: A string with the timestamp (e.g., "2025-01-24T05:46:55.194-08:00").
    :param target_date: A string with the target date (e.g., "2025-01-20").
    :return: True if the timestamp falls on the target date, False otherwise.
    """
    # Parse the timestamp and target date into datetime and date objects
    timestamp_date = datetime.fromisoformat(timestamp).date()
    target_date_obj = datetime.strptime(target_date, "%Y-%m-%d").date()

    # Compare the two dates
    return timestamp_date == target_date_obj


def merge_csv_files(csv_paths: List[str], output_path: str) -> None:
    """
    Merges multiple CSV files into one, keeping the header from the first file
    and dropping headers from subsequent files.

    :param csv_paths: List of paths to the CSV files to merge.
    :param output_path: Path to save the merged CSV file.
    """
    # Initialize an empty list to store DataFrames
    dataframes = []

    for i, csv_path in enumerate(csv_paths):
        try:
            # Read the CSV file
            df = pd.read_csv(csv_path)
            # If it's not the first file, skip the header
            if i > 0:
                df.columns = dataframes[0].columns  # Ensure consistent column names
            dataframes.append(df)
        except FileNotFoundError as error:
            print(error)

    # if any file found !
    if dataframes:
        # Concatenate all DataFrames
        merged_df = pd.concat(dataframes, ignore_index=True)

        # Save the merged DataFrame to the output file
        merged_df.to_csv(output_path, index=False)
    else:
        print('No data found')


def loop_over_date(start_date: str, days: int) -> List[str]:
    """
    Loops over a given string date for a specified number of days.

    :param start_date: The start date as a string in the format 'YYYY-MM-DD'.
    :param days: The number of days to loop over (positive or negative).
    :return: A list of date strings within the range.
    """
    # Parse the start_date into a datetime object
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()

    # Generate the date range
    date_range = [
        (start_date_obj + timedelta(days=day_offset)).isoformat()
        for day_offset in range(days)
    ]
    return date_range
