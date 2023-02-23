import cobra
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle

# Import my own CUE functions
# I want the CUE functions to eventually be their own package, but for
# now I'm just importing them from a different folder in the same
# repository
import sys
sys.path.insert(0, 'cue_utils')
from utils import (
                   atomExchangeMetabolite,
                   calculate_cue,
                   calculate_gge,
                   extract_c_fates)

# Set a folder for the plots
# Assuming you are running from the root of the repository
output_folder = 'spatial_ecoli_core/plots'

# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the results
with open('spatial_ecoli_core/results.pkl', 'rb') as f:
    experiment = pickle.load(f)

#########
# Biomass
#########
# Plot the biomass over time
# Right now, can use total biomass because the simulation is only the E.
# coli core model, but if I add other species, I will need to change
im = experiment.get_biomass_image('e_coli_core', 600)

# Save the biomass plot
plt.savefig(os.path.join(output_folder, 'biomass.png'))

#######
# Media
#######
# Plot the media concentrations over time
media = experiment.media.copy()
media = media[media.conc_mmol<900]

fig, ax = plt.subplots()
media.groupby('metabolite').plot(x='cycle', ax =ax, y='conc_mmol')
ax.legend(('acetate','ethanol', 'formate', 'glucose'))
ax.set_ylabel("Concentration (mmol)")

# Save the media plot
plt.savefig(os.path.join(output_folder, 'media.png'))

#####
# CUE
#####
# Load the E. coli model (Needed to get the exchange reactions)
e_coli_cobra = cobra.io.load_model('textbook')

# Get the exchange reactions for the E coli core model
# I think I would rather do this in the comets_simulation script, and
# save the exchange reactions with the results, but for now just do it
# here
c_ex_rxns = atomExchangeMetabolite(e_coli_cobra)

# Get the fluxes for each exchange reaction for each cycle of the
# experiment
fluxes = experiment.fluxes_by_species['e_coli_core'].copy()
# Create an empty array to hold the CUE for each cycle
cue_list = []
gge_list = []
# Loop through each cycle and calculate the CUE and the GGE
for index, row in fluxes.iterrows():
    cue_list.append(calculate_cue(row, c_ex_rxns))
    gge_list.append(calculate_gge(row, c_ex_rxns))

# Plot the CUE for each cycle
cycle_list = experiment.fluxes_by_species['e_coli_core']['cycle'].tolist()

# Plot 1: CUE only, zoomed out for the whole experiment
fig, ax = plt.subplots()
plt.plot(cycle_list, cue_list, label = "CUE")
ax.set_ylabel("Value")
ax.set_ylim(0, 1)
ax.set_xlabel("Cycle")
ax.set_xlim(0, 1000)
plt.legend()

plt.savefig(os.path.join(output_folder, 'cue_all_cycles.png'))

# Plot 2: CUE only, zoomed in
fig, ax = plt.subplots()
plt.plot(cycle_list, cue_list, label = "CUE")
ax.set_ylabel("Value")
ax.set_xlabel("Cycle")
plt.legend()

plt.savefig(os.path.join(output_folder, 'cue_zoom_in.png'))

# Plot 3: CUE and GGE for the whole experiment
fig, ax = plt.subplots()
plt.plot(cycle_list, cue_list, label = "CUE")
plt.plot(cycle_list, gge_list, label = "GGE")
ax.set_ylabel("Value")
ax.set_xlabel("Cycle")
ax.set_ylim(0, 1)
ax.set_xlim(0, 1000)
plt.legend()

plt.savefig(os.path.join(output_folder, 'cue_gge_all_cycles.png'))

# Plot 4: CUE and GGE zoomed in
fig, ax = plt.subplots()
plt.plot(cycle_list, cue_list, label = "CUE")
plt.plot(cycle_list, gge_list, label = "GGE")
ax.set_ylabel("Value")
ax.set_xlabel("Cycle")
plt.legend()

plt.savefig(os.path.join(output_folder, 'cue_gge_zoom_in.png'))

##############
# Carbon Fates
# Different from CUE- because it isn't just one value
##############
# Get the carbon fates for each cycle
respiration = []
exudation = []
other = []
for index, row in fluxes.iterrows():
    cycle_resp, cycle_ex, cycle_other = extract_c_fates(row, c_ex_rxns)
    respiration.append(cycle_resp)
    exudation.append(cycle_ex)
    other.append(cycle_other)

# Plot 5: Plot bar chart of carbon fates for each cycle
# width = 0.35
fig, ax = plt.subplots()
ax.bar(cycle_list, other, label='Biomass')
ax.bar(cycle_list, exudation, bottom=other, label='Exudation')
ax.bar(cycle_list, respiration, bottom=np.array(other)+np.array(exudation), label='Respiration')
plt.ylabel('Propotion of Uptaken Carbon')
plt.xlabel('Cycle')
plt.title('Carbon Fates at Each Cycle')
plt.legend()

plt.savefig(os.path.join(output_folder, 'c_fates_per_cycle.png'))