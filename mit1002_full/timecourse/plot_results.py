import cobra
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import pandas as pd

# Import my own CUE functions
# I want the CUE functions to eventually be their own package, but for
# now I'm just importing them from a different folder in the same
# repository
import sys
sys.path.insert(0, 'cue_utils')
from utils import (get_c_ex_rxns,
                   get_c_ex_rxn_fluxes,
                   get_biomass_carbon,
                   calculate_cue,
                   calculate_gge,
                   extract_c_fates,
                   get_co2_secretion,
                   get_org_c_secretion,
                   get_c_uptake)

# Set a folder for the plots
# Assuming you are running from the root of the repository
output_folder = 'mit1002_full/timecourse/plots'

# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the results
with open('mit1002_full/timecourse/results.pkl', 'rb') as f:
    experiment = pickle.load(f)

# Path to Zac's results
# Assuming you are running from the root of the repository
results_path = '../Zac txt data/'

########################################################################
# Biomass
########################################################################
# Plot the biomass over time
# Right now, can use total biomass because the simulation is only the E.
# coli core model, but if I add other species, I will need to change
ax = experiment.total_biomass.plot(x = 'cycle')
ax.set_ylabel("Biomass (gr.)")

# Convert the x ticks to hours by dividing by 100
ax.set_xticklabels([tick._x/100 for tick in ax.get_xticklabels()])
ax.set_xlabel("Time (hours)")

# Save the biomass plot
plt.savefig(os.path.join(output_folder, 'biomass.png'))

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
od.plot(x = 'Time',
        y = 'glucose_mean',
        kind='scatter',
        yerr='glucose_double_std',
        ax = ax,
        label = 'Experimental OD600')

# Convert the cycles in the total biomass dataframe to hours by dividing
# by 100 and shift it to account for the lag phase
experiment.total_biomass['Time'] = experiment.total_biomass['cycle']/100 + 4

# Plot the FBA restul as Biomass on the secondary y axis
experiment.total_biomass.plot(x = 'Time',
                              y = '', # Because the model doesn't have a name
                              ax = ax,
                              secondary_y = True,
                              label = 'FBA Predicted Biomass')

# Label the axes
ax.set_xlabel('Time (hours)')
ax.set_ylabel('OD600')
ax.right_ax.set_ylabel('Biomass (gr.)')

# Save the plot
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'exp_vs_pred_biomass.png'))

########################################################################
# Fluxes
########################################################################
# Plot the fluxes over time
# The model doesn't have a name, it is just called ''
ax = experiment.fluxes_by_species[''].plot(x="cycle", # FIXME: Add an ID to the model file
                                      y=["EX_cpd00007_e0", # EX_o2_e
                                         "EX_cpd00011_e0", # EX_co2_e
                                         "EX_cpd00027_e0", # Glucose
                                         "EX_cpd00029_e0"], # Acetate 
                                      kind="line")

# Convert the x ticks to hours by dividing by 100
ax.set_xticklabels([tick._x/100 for tick in ax.get_xticklabels()])
ax.set_xlabel("Time (hours)")

# Make a more human-friendly legend
plt.legend(('O2 Exchange', 'CO2 Exchange', 'Glucose Exchange', 'Acetate Exchange'))

# Save the biomass plot
plt.savefig(os.path.join(output_folder, 'fluxes.png'))

########################################################################
# Media
########################################################################
# Load the model (needed to get human friendly names)
alt_cobra = cobra.io.read_sbml_model("../../GEM-repos/mit1002-model/model.xml")

# Plot the media concentrations over time
media = experiment.media.copy()
media = media[media.conc_mmol<900]

fig, ax = plt.subplots()
for name, group in media.groupby('metabolite'):
    group.plot(x='cycle',
               ax = ax,
               y='conc_mmol',
               label=alt_cobra.metabolites.get_by_id(name).name)
ax.set_ylabel("Concentration (mmol)")

# Convert the x ticks to hours by dividing by 100
ax.set_xticklabels([tick._x/100 for tick in ax.get_xticklabels()])
ax.set_xlabel("Time (hours)")

# Save the media plot with the default y lims
plt.savefig(os.path.join(output_folder, 'media.png'))

# Zoom in so I can see what the low metabolites are doing
# FIXME: It still shows the legend of O2 which is confusing, maybe make
# a new media df with a lower concentration threshold than 900
ax.set_ylim(0, 0.022) # Can only get this number by actually looking at it
plt.savefig(os.path.join(output_folder, 'media-zoom-in.png'))

########################################################################
# CUE
########################################################################
# Need the model loaded to get the exchange reactions, already done
# for the media plot

# Get the exchange reactions for the E coli core model
# I think I would rather do this in the comets_simulation script, and
# save the exchange reactions with the results, but for now just do it
# here
c_ex_rxns = get_c_ex_rxns(alt_cobra)

# Get the fluxes for each exchange reaction for each cycle of the
# experiment
fluxes = experiment.fluxes_by_species[''].copy()
# Create an empty array to hold the CUE for each cycle
cue_list = []
gge_list = []
# Loop through each cycle and calculate the CUE and the GGE
for index, row in fluxes.iterrows():
    uptake_fluxes, secretion_fluxes = get_c_ex_rxn_fluxes(row, c_ex_rxns,
                                                          'COMETS')
    cue_list.append(calculate_cue(uptake_fluxes, secretion_fluxes,
                                  co2_ex_rxn = "EX_cpd00011_e0"))
    gge_list.append(calculate_gge(uptake_fluxes, secretion_fluxes,
                                  co2_ex_rxn = "EX_cpd00011_e0"))

# Plot the CUE for each cycle
cycle_list = experiment.fluxes_by_species['']['cycle'].tolist()

# Plot 1: CUE only
fig, ax = plt.subplots()
plt.plot(cycle_list, cue_list, label = "CUE")
ax.set_ylabel("Value")
# ax.set_ylim(0, 1) # Would need to increase the upper limit so that the line is visible
ax.set_xlim(0, max(cycle_list))
ax.set_xticklabels([tick._x/100 for tick in ax.get_xticklabels()])
ax.set_xlabel("Time (hours)")
plt.legend()

plt.savefig(os.path.join(output_folder, 'cue.png'))

# Plot 3: CUE and GGE for the whole experiment
fig, ax = plt.subplots()
plt.plot(cycle_list, cue_list, label = "CUE")
plt.plot(cycle_list, gge_list, '--', label = "GGE") # Dashed line so you can see that the two are directly on top of one another
ax.set_ylabel("Value")
ax.set_xlim(0, max(cycle_list))
ax.set_xticklabels([tick._x/100 for tick in ax.get_xticklabels()])
ax.set_xlabel("Time (hours)")
plt.legend()

plt.savefig(os.path.join(output_folder, 'cue_gge.png'))

########################################################################
# Experimental and Predicted CUE
########################################################################
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
        # Multiply the drawdown by 6 to account for the 6 carbon atoms in the glucose
        cues.append(1 - current_co2 / (current_drawdown * 6))

    # Calcualte the mean and the standard deviation for all the replicate
    cue_means.append(np.mean(cues))
    cue_std.append(np.std(cues))

# Make a scatter plot of the CUE means with error bars at the center of the
# measurement windows
window_centers = [1.5, 4.5, 7.5, 10.5]
fig, ax = plt.subplots()
plt.errorbar(window_centers, cue_means, yerr=cue_std, linestyle='')

# Add straight lines to the plot
window_ends = [[0, 3], [3, 6], [6, 9], [9, 12]]
for i in range(4):
    plt.plot(window_ends[i], [cue_means[i], cue_means[i]], linestyle='-', color='C0')

# Plot the FBA predicted CUE
plt.plot(np.array(cycle_list)/100 + 4, cue_list, label = "FBA Predicted CUE")

# Label the axes
ax.set_xlabel("Time (hours)")
ax.set_ylabel("CUE")
# Save the figure
plt.savefig(os.path.join(output_folder, 'exp_vs_pred_cue.png'))

########################################################################
# Carbon Fates
# Different from CUE- because it isn't just one value
########################################################################
# Get the carbon fates for each cycle
unaccounted = []
respiration = []
exudation = []
biomass = []
for index, row in fluxes.iterrows():
    cycle_biomass = get_biomass_carbon(row, 'bio1_biomass', alt_cobra, 'COMETS')
    uptake_fluxes, secretion_fluxes = get_c_ex_rxn_fluxes(row, c_ex_rxns,
                                                          'COMETS')
    cycle_uptake = get_c_uptake(uptake_fluxes)
    cycle_co2 = get_co2_secretion(secretion_fluxes, 'EX_cpd00011_e0')
    cycle_secretion = get_org_c_secretion(secretion_fluxes, 'EX_cpd00011_e0')

    unaccounted.append(cycle_uptake - (cycle_co2 + cycle_secretion + cycle_biomass))
    respiration.append(cycle_co2)
    exudation.append(cycle_secretion)
    biomass.append(cycle_biomass)

# Plot 5: Plot bar chart of carbon fates for each cycle
# width = 0.35
fig, ax = plt.subplots()
ax.bar(cycle_list, biomass, label='Biomass')
ax.bar(cycle_list, exudation, bottom=biomass, label='Organic C')
ax.bar(cycle_list, respiration, bottom=np.array(biomass)+np.array(exudation),
       label='CO2')
ax.bar(cycle_list, unaccounted,
       bottom=np.array(biomass)+np.array(exudation)+np.array(respiration),
       label='Unaccounted')
plt.ylabel('Carbon Atom Flux')
ax.set_xticklabels([tick._x/100 for tick in ax.get_xticklabels()])
ax.set_xlabel("Time (hours)")
plt.title('Carbon Fates at Each Cycle')
plt.legend()

plt.savefig(os.path.join(output_folder, 'c_fates_per_cycle.png'))