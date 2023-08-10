import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def processData(data):
    df = pd.DataFrame(data)
    print(df.head())
    print(df.info())
    print(df.describe())

    df.dropna(inplace=True)

    df['hospital_dttm'] = pd.to_datetime(df['hospital_dttm'])
    df['available_dttm'] = pd.to_datetime(df['available_dttm'])


    df['offload_dttm'] = df['available_dttm']- df['hospital_dttm'] 

    # Drop any rows with missing values
    df.dropna(inplace=True)
        
    print(df.head())
    plt.figure(figsize=(10, 6))

    # Calculate the minimum and maximum values of offload times
    data_min = round(df['offload_dttm'].min().total_seconds() / 60)
    data_max = round(df['offload_dttm'].max().total_seconds() / 60)

    # Calculate the number of bins based on the desired bin width of ten minutes
    bin_width = 10
    num_bins = int(np.ceil((data_max - data_min) / bin_width))

    # Calculate the adjusted maximum value to ensure consistent 10-minute bins
    data_max_adj = data_min + (num_bins * bin_width)

    hist_values, bin_edges, _ = plt.hist(df['offload_dttm'].dt.total_seconds() / 60, bins=np.linspace(data_min, data_max_adj, num_bins + 1), edgecolor='black')

    # Set the x-axis tick positions and labels in one line
    plt.locator_params(axis='x', nbins=num_bins)

    # Set the x-axis ticks at the center of each bin
    plt.xticks(bin_edges)

    # Function to convert minute tick values to hour:minute format
    # def minute_to_hour_minute(value, tick_number):
    #     hours = int(value // 60)
    #     minutes = int(value % 60)
    #     return f"{hours}:{minutes:02d}"

    # Set the formatter function for the x-axis ticks
    # plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(minute_to_hour_minute))

    # Create labels for graph
    plt.xlabel('Offload Times (min)')
    plt.ylabel('Count')
    plt.title('Histogram of Time at Hospital for 1000 Most Recent Ambulance Transports')

    # Add the number as text below the graph at the specified coordinates (0.5, -0.1)
    plt.text(0.5, -0.1, "Average time: " + str(df['offload_dttm'].mean().total_seconds() / 60), ha='center', va='center', fontsize=18, transform=plt.gca().transAxes)

    plt.show()
