#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""
from __future__ import annotations

import datetime
import warnings

import altair as alt
import pandas as pd
import requests
import requests_cache
from typing import List, Optional


# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()

# suppress a warning with altair 4 and latest pandas
warnings.filterwarnings("ignore", ".*convert_dtype.*", FutureWarning)


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """
    Fetch one day of electricity price data for a specified location from the hvakosterstrommen.no API.

    Function gathers the electricity price data for a single day at a given location in Norway. If no date is
    provided, the date defaults to todays date. If no location is specified, it defaults
    to "NO1" (Oslo). The function returns a DataFrame with the price in NOK per kWh,
    start and end times of the price data, etc.

    Args:
        date (datetime.date, optional): The date for which to fetch the data, in year, month, day format.
            Defaults to the current date if None.
        location (str, optional): The location code for which to fetch the data. Valid options are
            "NO1", "NO2", "NO3", "NO4", and "NO5", representing different regions in Norway.
            Defaults to "NO1" (Oslo) if None.

    Returns:
        pd.DataFrame: A DataFrame containing electricity prices for the specified date and location.
        The DataFrame includes columns for time start, time end, and price in NOK per kWh, EUR per kWh and  exchange rate EXR.
    """
    if date is None:
        date = datetime.date.today()  # Getting today's date unless otherwise specified

    if location is None:
        location = "NO1"

    year, month, day = (
        date.year,
        date.strftime("%m"),
        date.strftime("%d"),
    )  # Splitting the date into year, month and day, %m and %d make sure we get a leading 0

    # print(date)
    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{year}/{month}-{day}_{location}.json"  # Defining right url
    r = requests.get(url)  # Retrieving url

    json_data = r.json()  # Converting text data from url to json structure

    # Making DataFrame
    df = pd.DataFrame(json_data)  # Converting json data to pandas DataFrame

    # Convert 'time_start' and 'time_end' in the data files from UTC to 'Europe/Oslo' timezone
    df["time_start"] = pd.to_datetime(df["time_start"], utc=True).dt.tz_convert(
        "Europe/Oslo"
    )
    df["time_end"] = pd.to_datetime(df["time_end"], utc=True).dt.tz_convert(
        "Europe/Oslo"
    )

    return df


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen",
}


# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations: list[str] = tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """
    Fetch electricity prices for multiple days and locations from hvakosterstrommen.no API.

    This function gets electricity prices over a specified number of days leading up to an end date
    for given locations. If no parameters are specified, it defaults to a 7-day period ending today,
    for all locations in the dictionary LOCATION_CODES.

    Args:
        end_date (datetime.date, optional): The end date for the data range. Defaults to today's date
            if None is provided.
        days (int, optional): The number of days before the end date to include in the data range.
            Defaults to 7.
        locations (list[str], optional): A list of location codes where electricity prices can be fetched from.
            The location codes should correspond to defined locations in the LOCATION_CODES. If None, prices for
            all locations are fetched.

    Returns:
        pd.DataFrame:  pd.DataFrame: A DataFrame containing electricity prices for the specified dates and locations.
        The DataFrame includes columns for time start, time end, and price in NOK per kWh, EUR per kWh  exchange rate EXR, location code and location.

    Note:
        Prints message if the request to the API fails for any location on any date within the specified range.
    """
    if days is None:
        days = int(7)

    if end_date is None:
        end_date = datetime.date.today()

    if locations is None:
        locations = tuple(LOCATION_CODES.keys())

    start_date = end_date - datetime.timedelta(days=days - 1)

    all_data = []

    # Iterating over the dates
    for i in range(days):
        date = start_date + datetime.timedelta(days=i)
        year, month, day = (
            date.year,
            date.strftime("%m"),
            date.strftime("%d"),
        )  # Splitting the date into year, month and day, %m and %d make sure we get a leading 0

        for location in locations:
            # print(date)
            url = f"https://www.hvakosterstrommen.no/api/v1/prices/{year}/{month}-{day}_{location}.json"  # Defining right url
            r = requests.get(url)  # Retrieving url

            if r.status_code == 200:
                json_data = r.json()  # Converting text data from url to json structure

                df_j = pd.DataFrame(
                    json_data
                )  # Converting json data to pandas DataFrame

                # Convert 'time_start' and 'time_end' in the data files from UTC to 'Europe/Oslo' timezone
                df_j["time_start"] = pd.to_datetime(
                    df_j["time_start"], utc=True
                ).dt.tz_convert("Europe/Oslo")
                df_j["time_end"] = pd.to_datetime(
                    df_j["time_end"], utc=True
                ).dt.tz_convert("Europe/Oslo")

                # Adding location
                df_j["location_code"] = location
                df_j["location"] = LOCATION_CODES[location]

                all_data.append(df_j)

            elif r.status_code != 200:
                print(
                    f"Oh no! {r.status_code}. For date = {date} and location = {location}"
                )

    # Making DataFrame with all data
    df = pd.concat(
        all_data, ignore_index=True
    )  # Concatinating the list so that we can get all datas into one DataFrame

    return df


# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """
    Plot energy prices over time and save the plot as an HTML file.

    This function creates a line chart using Altair, showing electricity
    prices over time. The x-axis represents the time, and the y-axis represents the
    price in NOK per kWh. Each location in the data is represented by a different line
    in the chart. The chart is also saved as an HTML file for easy sharing and viewing.

    Parameters:
        df (pd.DataFrame): A DataFrame containing electricity price data over time.
            Expected to have columns 'time_start', 'NOK_per_kWh', and 'location'.

    Returns:
        alt.Chart: An Altair Chart object. The chart visualizes the
        electricity prices over time, with separate lines for different locations.
        The function also saves this chart as 'Energy_prices_over_time.html'.
    """
    # Plotting with altair
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("time_start:T", axis=alt.Axis(title="Time")),  # Time on x-axis
            y=alt.Y(
                "NOK_per_kWh:Q", axis=alt.Axis(title="Price [NOK per kWh]")
            ),  # Price on y-axis
            color="location:N",  # Different line color for each location
            tooltip=["time_start:T", "NOK_per_kWh:Q", "location:N"],
        )
        .properties(title="Energy prices over time in NOK", width=800, height=400)
        .interactive()
    )

    # saving to an html file
    chart.save(f"Energy_prices_over_time.html")
    return chart


# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    raise NotImplementedError("Remove me when you implement this task (in4110 only)")
    ...


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """
    raise NotImplementedError("Remove me when you implement this optional task")

    ...


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()

    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
