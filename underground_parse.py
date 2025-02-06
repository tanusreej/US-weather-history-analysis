from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.request import urlopen


def extract_weather_data(station_code):
    '''
    This function extracts weather data from downloaded web pages on wunderground.com
    into a structured CSV file for the specified station.

    Ensure that the wunderground scraper has been executed first to download the necessary web pages.
    '''

    # Define the date range for data extraction
    start_date = datetime(year=2014, month=7, day=1)
    finish_date = datetime(year=2015, month=7, day=1)

    with open(f'{station_code}.csv', 'w') as output_file:
        output_file.write('date,actual_mean_temp,actual_min_temp,actual_max_temp,'
                          'average_min_temp,average_max_temp,'
                          'record_min_temp,record_max_temp,'
                          'record_min_temp_year,record_max_temp_year,'
                          'actual_precipitation,average_precipitation,'
                          'record_precipitation\n')

        while start_date != finish_date:
            retry = False
            try:
                with open(f'{station_code}/{start_date.year}-{start_date.month}-{start_date.day}.html') as input_file:
                    soup = BeautifulSoup(input_file.read(), 'html.parser')

                    data_rows = soup.find(id='historyTable').find_all('tr')
                    weather_info = []
                    for row in data_rows:
                        weather_info.append(row.find_all('span', class_='wx-value'))
                    weather_info = [info for info in weather_info if info]

                    if len(weather_info[4]) < 2:
                        weather_info[4].extend([None, None])

                    data_units = soup.find(id='historyTable').find_all('td')

                    try:
                        mean_temp = weather_info[0][0].text
                        max_temp = weather_info[1][0].text
                        avg_max_temp = weather_info[1][1].text
                        record_max_temp = weather_info[1][2].text if weather_info[1][2] else None
                        min_temp = weather_info[2][0].text
                        avg_min_temp = weather_info[2][1].text
                        record_min_temp = weather_info[2][2].text
                        record_max_year = data_units[9].text.split('(')[-1].strip(')')
                        record_min_year = data_units[13].text.split('(')[-1].strip(')')

                        precipitation = weather_info[4][0].text
                        if precipitation == 'T':
                            precipitation = '0.0'

                        avg_precipitation = weather_info[4][1].text if weather_info[4][1] else None
                        record_precipitation = weather_info[4][2].text if weather_info[4][2] else None

                        # Validate the parsed data
                        if (record_max_year == '-1' or record_min_year == '-1' or
                                int(record_max_temp) < max(int(max_temp), int(avg_max_temp)) or
                                int(record_min_temp) > min(int(min_temp), int(avg_min_temp)) or
                                ((record_precipitation or avg_precipitation) and 
                                (float(precipitation) > float(record_precipitation) or
                                float(avg_precipitation) > float(record_precipitation)))):
                            raise ValueError("Invalid data")

                        output_file.write(f'{start_date.year}-{start_date.month}-{start_date.day},')
                        output_file.write(','.join([mean_temp, min_temp, max_temp,
                                                     avg_min_temp, avg_max_temp,
                                                     record_min_temp, record_max_temp,
                                                     record_min_year, record_max_year,
                                                     precipitation]))
                        if avg_precipitation:
                            output_file.write(f',{avg_precipitation}')
                        if record_precipitation:
                            output_file.write(f',{record_precipitation}')

                        output_file.write('\n')
                        start_date += timedelta(days=1)

                    except Exception:
                        retry = True

            except FileNotFoundError:
                retry = True

            if retry:
                print(f'Error processing date {start_date}')

                lookup_url = 'http://www.wunderground.com/history/airport/{}/{}/{}/{}/DailyHistory.html'
                formatted_url = lookup_url.format(station_code,
                                                   start_date.year,
                                                   start_date.month,
                                                   start_date.day)
                html_content = urlopen(formatted_url).read().decode('utf-8')

                output_file_name = f'{station_code}/{start_date.year}-{start_date.month}-{start_date.day}.html'

                with open(output_file_name, 'w') as new_file:
                    new_file.write(html_content)


# List of weather stations to process
for station in ['KCLT', 'KCQT', 'KHOU', 'KIND', 'KJAX',
                'KMDW ', 'KNYC', 'KPHL', 'KPHX', 'KSEA', 'KSAF']:
    extract_weather_data(station)