import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def processData(data):
    df = pd.DataFrame(data)

    # Drop rows with missing values
    df.dropna(inplace=True)

    df['hospital_dttm'] = pd.to_datetime(df['hospital_dttm'])
    df['available_dttm'] = pd.to_datetime(df['available_dttm'])

    df['offload_dttm'] = df['available_dttm'] - df['hospital_dttm']

    

    # Calculate the Z-score for offload times
    z_scores = np.abs(stats.zscore(df['offload_dttm'].dt.total_seconds() / 60))

    # Set a Z-score threshold for outliers (e.g., 3 standard deviations)
    z_score_threshold = 3

    # Filter out outliers based on the Z-score threshold
    df = df[(z_scores <= z_score_threshold)]

    # Calculate the minimum and maximum values of offload times
    data_min = 0  # Start at 0 minutes
    data_max = round(df['offload_dttm'].max().total_seconds() / 60)

    # Calculate the number of bins based on the desired bin width of ten minutes
    bin_width = 10
    num_bins = int(np.ceil((data_max - data_min) / bin_width))

    # Calculate the bin edges
    bin_edges = np.arange(data_min, data_max + bin_width, bin_width)

    # Calculate the 90th percentile time
    percentile_90 = np.percentile(df['offload_dttm'].dt.total_seconds() / 60, 90)

    # Create the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(df['offload_dttm'].dt.total_seconds() / 60, bins=bin_edges, edgecolor='black')

    # Set the x-axis ticks at the edges of each bin
    plt.xticks(bin_edges)

    # Create labels for graph
    plt.xlabel('Time at Hospital (min)')
    plt.ylabel('Count')
    plt.title('Histogram of Time at Hospital for 1000 Most Recent Ambulance Transports (Outliers Removed)')

    # Add the number as text below the graph at the specified coordinates (0.5, -0.1)
    plt.text(0.5, -0.1, "Average time: " + str(df['offload_dttm'].mean().total_seconds() / 60) + ' min', ha='center', va='top', fontsize=14, transform=plt.gca().transAxes)

    # Add the 90th percentile time as text
    plt.text(0.5, -0.4, f"90th percentile time: {percentile_90:.2f} min", ha='center', va='top', fontsize=12, transform=plt.gca().transAxes)

    plt.show()
