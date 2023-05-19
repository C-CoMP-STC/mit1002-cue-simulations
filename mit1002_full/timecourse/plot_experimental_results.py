import pandas as pd
import os

# Set a folder for the plots
# Assuming you are running from the root of the repository
output_folder = 'mit1002_full/timecourse/plots'

# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Path to Zac's results
# Assuming you are running from the root of the repository
results_path = '../Zac txt data/'

# Load the results needed to calculate CUE (cumulative CO2 and drawdown)
cumulative_co2 = pd.read_csv(os.path.join(results_path,
                                          'MIT1002_singles_cumulative.txt'),
                             sep='\t')
drawdown = pd.read_csv(os.path.join(results_path,
                                    'MIT1002_singles_drawdown.txt'),
                       sep='\t')

########################################################################
# OD
########################################################################
# Load the OD data
od = pd.read_csv(os.path.join(results_path, 'MIT1002_singles_OD600.txt'),
                 sep='\t')

# Get the mean and double standard deviation of the OD for the replicates
od['glucose_mean'] = od[['MIT1002_glucose',
                         'MIT1002_glucose.1',
                         'MIT1002_glucose.2',
                         'MIT1002_glucose.3',
                         'MIT1002_glucose.4']].mean(axis=1)
od['glucose_double_std'] = od[['MIT1002_glucose',
                               'MIT1002_glucose.1',
                               'MIT1002_glucose.2',
                               'MIT1002_glucose.3',
                               'MIT1002_glucose.4']].std(axis=1) * 2

# Plot the mean and the double standard deviation as a scatter plot with
# error bars
ax = od.plot(x='Time',
             y='glucose_mean',
             kind='scatter',
             yerr='glucose_double_std')

# Label the axes
ax.set_xlabel('Time (hours)')
ax.set_ylabel('OD600')

# Save the plot
plt = ax.get_figure()
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'exp_od.png'))