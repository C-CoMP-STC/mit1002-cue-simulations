import cobra
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle

# Import my own CUE functions
# I want the CUE functions to eventually be their own package, but for now
# I'm just importing them from a different folder in the same repository
import sys
sys.path.insert(0, '../cue_utils')
from utils import atomExchangeMetabolite

# Set a folder for the plots
output_folder = 'plots'

# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the results
with open('results.pkl', 'rb') as f:
    experiment = pickle.load(f)

# Plot the biomass over time
ax = experiment.total_biomass.plot(x = 'cycle')
ax.set_ylabel("Biomass (gr.)")

# Save the biomass plot
plt.savefig(os.path.join(output_folder, 'biomass.png'))

# Plot the media concentrations over time
media = experiment.media.copy()
media = media[media.conc_mmol<900]

fig, ax = plt.subplots()
media.groupby('metabolite').plot(x='cycle', ax =ax, y='conc_mmol')
ax.legend(('acetate','ethanol', 'formate', 'glucose'))
ax.set_ylabel("Concentration (mmol)")

# Save the media plot
plt.savefig(os.path.join(output_folder, 'media.png'))

# Calculate CUE
################
# Load the E. coli model (Needed to get the exchange reactions)
e_coli_cobra = cobra.io.load_model('textbook')

# Get the exchange reactions for the E coli core model
c_ex_rxns = atomExchangeMetabolite(e_coli_cobra)

# Get the fluxes for each exchange reaction for each cycle of the experiment
fluxes = experiment.fluxes_by_species['e_coli_core'].copy()
# Create an empty array to hold the CUE for each cycle
cue_list = []
# Loop through each cycle and calculate the CUE from the exchange fluxes
for index, row in fluxes.iterrows():
    # Get the exchange fluxes for the current cycle
    c_ex_fluxes = [float(row[r]) * -c for r, c in c_ex_rxns.items()]
    # Calculate the CUE for the current cycle and add it to the cue array
    uptake = sum([flux for flux in c_ex_fluxes if flux > 0])
    release = sum([flux for flux in c_ex_fluxes if flux < 0])
    if uptake == 0:
        cue_list.append(0)
    else:
        cue = 1 + release/uptake
    cue_list.append(cue)

# Plot the CUE for each cycle
# FIXME: Show the cycle number not the index of the cycle
fig, ax = plt.subplots()
ax.plot(cue_list)

# Save the CUE plot
plt.savefig(os.path.join(output_folder, 'cue.png'))