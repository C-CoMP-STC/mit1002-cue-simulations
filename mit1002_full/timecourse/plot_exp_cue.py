import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Path to Zac's results
# Assuming you are running from the root of the repository
results_path = '../Zac txt data/'

# Load the cumulative CO2 data
cumulative_co2 = pd.read_csv(os.path.join(results_path, 'MIT1002_singles_cumulative.txt'),
                             sep='\t')

# Load the cumulative CO2 data
drawdown = pd.read_csv(os.path.join(results_path, 'MIT1002_singles_drawdown.txt'),
                       sep='\t')
drawdown.columns = ['Time (hours)', 'Ac_D', 'Ac_E', 'Ac_F', 'Glc_A', 'Glc_B', 'Glc_C']

# Set the timepoints I am using
drawdow_datapoints = [0, 3, 6, 9, 12]
co2_datapoints = [0, 2.8233, 6.11715, 8.94045, 12.2343]

# Calculate the mean and standard deviation of the CUE foe each timepoint
cue_means = []
cue_std = []

for i in range(1,5):
    cues = []
    for replicate in ['Glc_A', 'Glc_B', 'Glc_C']:
        # Get the data for the current drawdown
        current_drawdown = float(drawdown[drawdown['Time (hours)'] == drawdow_datapoints[i-1]][replicate]) - float(drawdown[drawdown['Time (hours)'] == drawdow_datapoints[i]][replicate])
        # Get the data for the current CO2
        current_co2 = float(cumulative_co2[cumulative_co2['Time (hours)'] == co2_datapoints[i]][replicate]) - float(cumulative_co2[cumulative_co2['Time (hours)'] == co2_datapoints[i-1]][replicate])

        # Calculate the CUE for the current replicate
        if current_drawdown == 0:
            continue
        cues.append(1 - current_co2 / current_drawdown)
    
    # Calcualte the mean and the standard deviation for all the replicate
    cue_means.append(np.mean(cues))
    cue_std.append(np.std(cues))

# Make a scatter plot of the CUE means with error bars at the center of the
# measurement windows
window_centers = [1.5, 4.5, 7.5, 10.5]
# plt.scatter(window_centers, cue_means)
plt.errorbar(window_centers, cue_means, yerr=cue_std, linestyle='')

# Add straight lines to the plot
window_ends = [[0, 3], [3, 6], [6, 9], [9, 12]]
for i in range(4):
    plt.plot(window_ends[i], [cue_means[i], cue_means[i]], linestyle='--', color='black')