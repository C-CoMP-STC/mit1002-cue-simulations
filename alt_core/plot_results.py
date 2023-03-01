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
output_folder = 'alt_core/plots'

# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the results
with open('alt_core/results.pkl', 'rb') as f:
    experiment = pickle.load(f)

########################################################################
# Biomass
########################################################################
# Plot the biomass over time
# Right now, can use total biomass because the simulation is only the E.
# coli core model, but if I add other species, I will need to change
ax = experiment.total_biomass.plot(x = 'cycle')
ax.set_ylabel("Biomass (gr.)")

# Remove the legend since there is only one species (and there is no ID)
ax.get_legend().remove()

# Save the biomass plot
plt.savefig(os.path.join(output_folder, 'biomass.png'))

########################################################################
# Fluxes
########################################################################
# Plot the fluxes over time
# The model doesn't have a name, it is just called ''
experiment.fluxes_by_species[''].plot(x="cycle",
                                      y=["EX_cpd00007_e0", # Exchange for O2_e0
                                         "EX_cpd00011_e0", # Exchange for CO2_e0
                                         "EX_cpd00027_e0"], # Exchange for G-glucose
                                      kind="line")
# Make a more human-friendly legend
plt.legend(('O2 Exchange', 'CO2 Exchange', 'Glucose Exchange'))
# Save the biomass plot
plt.savefig(os.path.join(output_folder, 'fluxes.png'))

########################################################################
# Media
########################################################################
# Plot the media concentrations over time
media = experiment.media.copy()
media = media[media.conc_mmol<900]

fig, ax = plt.subplots()
media.groupby('metabolite').plot(x='cycle', ax =ax, y='conc_mmol')
ax.legend(('D-Glucose_e0', 'H+_e0', 'Nitrite_e0')) # TODO: Find a way to get the metabolite names from the media dataframe
ax.set_ylabel("Concentration (mmol)")

# Save the media plot
plt.savefig(os.path.join(output_folder, 'media.png'))

########################################################################
# CUE
########################################################################
# Load the model (Needed to get the exchange reactions)
alt_cobra = cobra.io.read_sbml_model("../../GEM-repos/mit1002-core-model/core_314275.5_GP.SBML/core_314275.5_GP.xml")

# Get the exchange reactions for the E coli core model
# I think I would rather do this in the comets_simulation script, and
# save the exchange reactions with the results, but for now just do it
# here
c_ex_rxns = atomExchangeMetabolite(alt_cobra, ex_nomenclature = {'e0'})

# Get the fluxes for each exchange reaction for each cycle of the
# experiment
fluxes = experiment.fluxes_by_species[''].copy()
# Create an empty array to hold the CUE for each cycle
cue_list = []
gge_list = []
# Loop through each cycle and calculate the CUE and the GGE
for index, row in fluxes.iterrows():
    cue_list.append(calculate_cue(row, c_ex_rxns, resp_rxn = 'EX_cpd00011_e0'))
    gge_list.append(calculate_gge(row, c_ex_rxns))

# Plot the CUE for each cycle
cycle_list = experiment.fluxes_by_species['']['cycle'].tolist()

# Plot 1: CUE only
fig, ax = plt.subplots()
plt.plot(cycle_list, cue_list, label = "CUE")
ax.set_ylabel("Value")
# ax.set_ylim(0, 1) # Would need to increase the upper limit so that the line is visible
ax.set_xlabel("Cycle")
ax.set_xlim(0, 600)
plt.legend()

plt.savefig(os.path.join(output_folder, 'cue.png'))

# Plot 3: CUE and GGE for the whole experiment
fig, ax = plt.subplots()
plt.plot(cycle_list, cue_list, label = "CUE")
plt.plot(cycle_list, gge_list, '--', label = "GGE") # Dashed line so you can see that the two are directly on top of one another
ax.set_ylabel("Value")
ax.set_xlabel("Cycle")
# ax.set_ylim(0, 1) # Would need to increase the upper limit so that the lines are visible
ax.set_xlim(0, 600)
plt.legend()

plt.savefig(os.path.join(output_folder, 'cue_gge.png'))

########################################################################
# Carbon Fates
# Different from CUE- because it isn't just one value
########################################################################
# Get the carbon fates for each cycle
respiration = []
exudation = []
other = []
for index, row in fluxes.iterrows():
    cycle_resp, cycle_ex, cycle_other = extract_c_fates(row, c_ex_rxns, resp_rxn = 'EX_cpd00011_e0')
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