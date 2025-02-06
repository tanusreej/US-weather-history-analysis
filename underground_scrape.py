# coding: utf-8

from datetime import datetime, timedelta
from urllib.request import urlopen
import os


def fetch_weather_data(station_code):
    '''
    This function fetches weather data web pages from wunderground.com
    for the specified weather station.

    To find your city's weather station, search for it on wunderground.com
    and navigate to the "History" section. The 4-letter station code will
    be displayed on that page.
    '''

    # Define the date range for scraping
    start_date = datetime(year=2014, month=7, day=1)
    finish_date = datetime(year=2015, month=7, day=1)

    # Create a directory for storing the station's web pages
    os.makedirs(station_code, exist_ok=True)

    # URL template for fetching historical weather data
    base_url = 'http://www.wunderground.com/history/airport/{}/{}/{}/{}/DailyHistory.html'

    while start_date != finish_date:

        if start_date.day == 1:
            print(f'Scraping data for: {start_date}')

        # Format the URL with the current date and station code
        formatted_url = base_url.format(station_code,
                                         start_date.year,
                                         start_date.month,
                                         start_date.day)
        html_content = urlopen(formatted_url).read().decode('utf-8')

        # Define the output file name
        output_file_name = f'{station_code}/{start_date.year}-{start_date.month}-{start_date.day}.html'

        # Write the HTML content to a file
        with open(output_file_name, 'w') as output_file:
            output_file.write(html_content)

        # Move to the next day
        start_date += timedelta(days=1)


# List of weather stations to scrape
weather_stations = ['KCLT', 'KCQT', 'KHOU', 'KIND', 'KJAX',
                    'KMDW', 'KNYC', 'KPHL', 'KPHX', 'KSEA']

# Scrape data for each station in the list
for station in weather_stations:
    fetch_weather_data(station)