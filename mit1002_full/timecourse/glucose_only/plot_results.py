import cobra
import matplotlib.pyplot as plt
import os
import pickle
import pandas as pd

import helpers

# Set the output directory (where the results.pkl file will be saved)
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Set a folder for the plots
# Assuming you are running from the root of the repository
output_folder = os.path.join(OUT_DIR, 'plots')

# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the results
with open(os.path.join(OUT_DIR, 'results.pkl'), 'rb') as f:
    experiment = pickle.load(f)

# Path to Zac's results
# Assuming you are running from the root of the repository
results_path = '../Zac txt data/'

# Read in the model file
# Assuming you are running from the root of the repository
model_path = '../../GEM-repos/mit1002-model/model.xml'
alt_cobra = cobra.io.read_sbml_model(model_path)

# Get the ID of the biomass reaction
# TODO: Just get this from the model objective
biomass_rxn = 'bio1_biomass'

# Plot the biomass
helpers.plot_biomass(experiment, output_folder)

# Plot the fluxes
helpers.plot_fluxes(experiment, output_folder)

# Plot concentrations of metabolites in the media
helpers.plot_media(alt_cobra, experiment, output_folder)

# Plot all of the due definitions on one graph
helpers.plot_cue(alt_cobra, experiment, biomass_rxn, output_folder)

# Plot the carbon fates
helpers.plot_c_fates(alt_cobra, experiment, biomass_rxn, output_folder)

########################################################################
# Experimental and Predicted Biomass
########################################################################
# Load the OD data
od = pd.read_csv(os.path.join(results_path, 'MIT1002_singles_OD600.txt'),
                 sep='\t')

# Get the mean and double standard deviation of the OD for the replicates of
# growth on glucose only
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

fig, ax = plt.subplots(figsize=(20,10)) 

# Plot the OD data on one y axis, with the mean as a scatter plot and the
# double standard deviation as error bars
od.plot(x='Time',
        y='glucose_mean',
        kind='scatter',
        yerr='glucose_double_std',
        ax=ax,
        label='Experimental OD600')

# Convert the cycles in the total biomass dataframe to hours by dividing
# by 100 and shift it to account for the lag phase
experiment.total_biomass['Time'] = experiment.total_biomass['cycle']/100 + 4

# Plot the FBA restul as Biomass on the secondary y axis
experiment.total_biomass.plot(x='Time',
                              y='', # Because the model doesn't have a name
                              ax=ax,
                              secondary_y=True,
                              label='FBA Predicted Biomass')

# Label the axes
ax.set_xlabel('Time (hours)')
ax.set_ylabel('OD600')
ax.right_ax.set_ylabel('Biomass (gr.)')

# Save the plot
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'exp_vs_pred_biomass.png'))


# ########################################################################
# # Experimental and Predicted CUE
# ########################################################################
# # Load the cumulative CO2 data
# cumulative_co2 = pd.read_csv(os.path.join(results_path, 'MIT1002_singles_cumulative.txt'),
#                              sep='\t')

# # Load the cumulative CO2 data
# drawdown = pd.read_csv(os.path.join(results_path, 'MIT1002_singles_drawdown.txt'),
#                        sep='\t')
# drawdown.columns = ['Time (hours)', 'Ac_D', 'Ac_E', 'Ac_F', 'Glc_A', 'Glc_B', 'Glc_C']

# # Set the timepoints I am using
# drawdow_datapoints = [0, 3, 6, 9, 12]
# co2_datapoints = [0, 3.29385, 6.11715, 8.94045, 12.2343]

# # Calculate the mean and standard deviation of the CUE for each timepoint
# cue_means = []
# cue_std = []

# for i in range(1,5):
#     cues = []
#     for replicate in ['Glc_A', 'Glc_B', 'Glc_C']:
#         # Get the data for the current drawdown
#         current_drawdown = float(drawdown[drawdown['Time (hours)'] == drawdow_datapoints[i-1]][replicate]) - float(drawdown[drawdown['Time (hours)'] == drawdow_datapoints[i]][replicate])
#         # Get the data for the current CO2
#         current_co2 = float(cumulative_co2[cumulative_co2['Time (hours)'] == co2_datapoints[i]][replicate]) - float(cumulative_co2[cumulative_co2['Time (hours)'] == co2_datapoints[i-1]][replicate])

#         # Calculate the CUE for the current replicate
#         if current_drawdown == 0:
#             continue
#         cues.append(1 - current_co2 / (current_drawdown))

#     # Calcualte the mean and the standard deviation for all the replicate
#     cue_means.append(np.mean(cues))
#     cue_std.append(np.std(cues))

# # Make a scatter plot of the CUE means with error bars at the center of the
# # measurement windows
# window_centers = [1.5, 4.5, 7.5, 10.5]
# fig, ax = plt.subplots()
# plt.errorbar(window_centers, cue_means, yerr=cue_std, linestyle='')

# # Add straight lines to the plot
# window_ends = [[0, 3], [3, 6], [6, 9], [9, 12]]
# for i in range(4):
#     plt.plot(window_ends[i], [cue_means[i], cue_means[i]], linestyle='-', color='C0')

# # Plot the FBA predicted CUE
# plt.plot(np.array(cycle_list)/100 + 4, cue_list, label = "FBA Predicted CUE")

# # Label the axes
# ax.set_xlabel("Time (hours)")
# ax.set_ylabel("CUE")
# # Save the figure
# plt.savefig(os.path.join(output_folder, 'exp_vs_pred_cue.png'))
