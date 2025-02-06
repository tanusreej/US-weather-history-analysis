import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Load the weather data from a CSV file in the Datasets folder
weather_df = pd.read_csv('Datasets/KPHL.csv', parse_dates=['date'])
print(weather_df.describe())

# Set the style for the plots
with plt.style.context('https://gist.githubusercontent.com/rhiever/d0a7332fe0beebfdc3d5/raw/223d70799b48131d5ce2723cd5784f39d7a3a653/tableau10.mplstyle'):
    # Create histograms for each column except 'date'
    for col in weather_df.columns:
        if col == 'date':
            continue
        plt.figure()
        plt.hist(weather_df[col].values, bins=30, alpha=0.7)
        plt.title(f'Distribution of {col}')
        plt.savefig(f'Results/{col}.png')  # Save to Results folder

    # Filter the data for the period July 2014 to June 2015
    filtered_data = weather_df[(weather_df['date'] >= datetime(2014, 7, 1)) & 
                                (weather_df['date'] < datetime(2015, 7, 1))].copy()
    filtered_data['day_index'] = range(len(filtered_data))

    # Extract temperature data
    day_indices = filtered_data['day_index']
    max_recorded_temps = filtered_data['record_max_temp'].values
    min_recorded_temps = filtered_data['record_min_temp'].values
    avg_max_temps = filtered_data['average_max_temp'].values
    avg_min_temps = filtered_data['average_min_temp'].values
    actual_max_temps = filtered_data['actual_max_temp'].values
    actual_min_temps = filtered_data['actual_min_temp'].values

    # Create a figure for plotting
    fig, ax = plt.subplots(figsize=(15, 7))

    # Plot bars for temperature records
    ax.bar(day_indices, max_recorded_temps - min_recorded_temps, bottom=min_recorded_temps,
           color='#C3BBA4', width=1, edgecolor='none', label='Record Highs and Lows')

    ax.bar(day_indices, avg_max_temps - avg_min_temps, bottom=avg_min_temps,
           color='#9A9180', width=1, edgecolor='none', label='Average Highs and Lows')

    ax.bar(day_indices, actual_max_temps - actual_min_temps, bottom=actual_min_temps,
           color='#5A3B49', width=1, edgecolor='black', linewidth=0.5, label='Actual Highs and Lows')

    # Identify new records
    new_max_records = filtered_data[filtered_data.record_max_temp <= filtered_data.actual_max_temp]
    new_min_records = filtered_data[filtered_data.record_min_temp >= filtered_data.actual_min_temp]

    # Mark new record highs and lows
    ax.scatter(new_max_records['day_index'].values + 0.5,
               new_max_records['actual_max_temp'].values + 1.25,
               s=15, color='#d62728', alpha=0.75, zorder=10)

    ax.scatter(new_min_records['day_index'].values + 0.5,
               new_min_records['actual_min_temp'].values - 1.25,
               s=15, color='#1f77b4', alpha=0.75, zorder=10)

    # Set limits and labels
    ax.set_ylim(-15, 111)
    ax.set_xlim(-5, 370)
    ax.set_ylabel('Temperature (°F)', fontsize=12)

    # Add month labels
    month_starts = filtered_data[filtered_data['date'].dt.day == 1]
    month_indices = list(month_starts['day_index'].values)
    month_names = list(month_starts['date'].dt.strftime("%B").values)
    month_names[0] += '\n\'14'
    month_names[6] += '\n\'15'
    month_indices.append(filtered_data['day_index'].values[-1])
    month_names.append('July')

    ax.set_xticks(month_indices)
    ax.set_xticklabels(month_names, fontsize=10)

    # Add title and save the figure
    ax.set_title('Weather Data for Philadelphia, PA (July 2014 - June 2015)', fontsize=20)
    plt.savefig('Results/philadelphia_weather_july14_june15.png')  # Save to Results folder