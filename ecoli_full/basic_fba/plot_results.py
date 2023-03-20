import seaborn as sns
import matplotlib.pyplot as plt
import os
import pickle

import sys
sys.path.insert(0, 'cue_utils')
from utils import (
                   atomExchangeMetabolite,
                   calculate_cue,
                   calculate_gge,
                   extract_c_fates)

# Set a folder for the plots
# Assuming you are running from the root of the repository
output_folder = 'ecoli_full/basic_fba/plots'

# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the results
with open('ecoli_full/basic_fba/results.pkl', 'rb') as f:
    results = pickle.load(f)

# Get the dataframes
nitrogen_results = results[0]
carbon_results = results[1]
vm_results = results[2]

########################################################################
# CUE vs Nitrogen and ATPM (Steady Glucose)
########################################################################
# Plot the CUE vs Nitrogen and ATPM
g = sns.relplot(x='ammonia', y='cue', hue='vm', data=nitrogen_results, 
                kind='line', marker='o', height=3)
# Save the plot
plt.savefig(os.path.join(output_folder, 'cue_ammonia_vm.png'))

# Plot the GGE vs Nitrogen and ATPM
g = sns.relplot(x='ammonia', y='gge', hue='vm', data=nitrogen_results,
                kind='line', marker='o', height=3)
# Save the plot
plt.savefig(os.path.join(output_folder, 'gge_ammonia_vm.png'))

# Plot the respiration, exudation, and biomass as a stacked bar plot
# with the x axis being the ammonia concentration, and separate plots
# for each ATPM value
for vm in nitrogen_results['vm'].unique():
    # Get the data needed for plotting for the current vm
    data = nitrogen_results.set_index('ammonia')
    data = data[data['vm'] == vm][['respiration', 'exudation', 'biomass']]
    # Plot the stacked bar plot
    g = data.plot(kind='bar', stacked=True, color=['red', 'skyblue', 'green'])
    # Set the x and y labels
    g.set_xlabel('Ammonia Import Flux (mmol/ [gDW h])')
    g.set_ylabel('Carbon Molecules (mmol/ [gDW h])')
    # Title the plot based on the ATPM value
    g.set_title('Carbon Fates (ATPM = {})'.format(vm))
    # Save the plot
    plt.savefig(os.path.join(output_folder, 'c_fates_ammonia_vm_{}.png'.format(vm)))

########################################################################
# CUE vs Glucose and ATPM (Steady Nitrogen)
########################################################################
# Plot the CUE vs Glucose and ATPM
g = sns.relplot(x='glc', y='cue', hue='vm', data=carbon_results, kind='line',
                marker='o', height=3)
# Save the plot
plt.savefig(os.path.join(output_folder, 'cue_glc_vm.png'))

# Plot the GGE vs Glucose and ATPM
g = sns.relplot(x='glc', y='gge', hue='vm', data=carbon_results, kind='line',
                marker='o', height=3)
# Save the plot
plt.savefig(os.path.join(output_folder, 'gge_glc_vm.png'))

# Plot the respiration, exudation, and biomass as a stacked bar plot
# with the x axis being the ammonia concentration, and separate plots
# for each ATPM value
for vm in carbon_results['vm'].unique():
    # Get the data needed for plotting for the current vm
    data = carbon_results.set_index('glc')
    data = data[data['vm'] == vm][['respiration', 'exudation', 'biomass']]
    # Plot the stacked bar plot
    g = data.plot(kind='bar', stacked=True, color=['red', 'skyblue', 'green'])
    # Set the x and y labels
    g.set_xlabel('Glucose Import Flux (mmol/ [gDW h])')
    g.set_ylabel('Carbon Molecules (mmol/ [gDW h])')
    # Title the plot based on the ATPM value
    g.set_title('Carbon Fates (ATPM = {})'.format(vm))
    # Save the plot
    plt.savefig(os.path.join(output_folder, 'c_fates_glc_vm_{}.png'.format(vm)))

########################################################################
# CUE vs ATPM (Steady Carbon and Nitrogen)
########################################################################
# Plot the cue vs atpm
g = sns.relplot(x='vm', y='cue', data=vm_results, kind='line', marker='o',
                height=3)

# Save the plot
plt.savefig(os.path.join(output_folder, 'cue_vm.png'))

# Plot the gge vs atpm
g = sns.relplot(x='vm', y='gge', data=vm_results, kind='line', marker='o',
                height=3)
# Save the plot
plt.savefig(os.path.join(output_folder, 'gge_vm.png'))

# Plot the respiration, exudation, and biomass as a stacked bar plot
# with the x axis being the ATPM value
# Get the data needed for plotting
data = vm_results.set_index('vm')[['respiration', 'exudation', 'biomass']]
# Plot the stacked bar plot
g = data.plot(kind='bar', stacked=True, color=['red', 'skyblue', 'green'])
# Set the x and y labels
g.set_xlabel('ATPM (mmol/ [gDW h])')
g.set_ylabel('Carbon Molecules (mmol/ [gDW h])')
# Title the plot
g.set_title('Carbon Fates')
# Save the plot
plt.savefig(os.path.join(output_folder, 'c_fates_vm.png'))
