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

########################################################################
# Set Up
########################################################################
# Set a folder for the plots
# Assuming you are running from the root of the repository
output_folder = 'well_mixed_ecoli_core/plots'

# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the results
with open('well_mixed_ecoli_core/results.pkl', 'rb') as f:
    experiment = pickle.load(f)

# Load the E. coli model (Needed to get the exchange reactions)
e_coli_cobra = cobra.io.load_model('textbook')

# Get the exchange reactions for the E coli core model
c_ex_rxns = atomExchangeMetabolite(e_coli_cobra)

########################################################################
# Calculate Growth Rate and Yield
########################################################################
# Get the growth rate and the yield for each cycle of the experiment
fluxes = experiment.fluxes_by_species['e_coli_core'].copy()
# Create an empty array to hold the growth rate and yields
growth_rate_list = []
gge_list = []
# Loop through each cycle, pull out the biomass flux (which I'm assuming
# is the same as growth rate) and then calculate GGE (same as yield)
for index, row in fluxes.iterrows():
    growth_rate_list.append(row['Biomass_Ecoli_core'])
    gge_list.append(calculate_gge(row, c_ex_rxns))

########################################################################
# Plot
########################################################################
plt.scatter(gge_list, growth_rate_list)
plt.ylabel('Yield (GGE)')
plt.xlabel('Growth Rate (Biomass Reaction Flux))')

# Save the scatter plot
plt.savefig(os.path.join(output_folder, 'growth_rate_vs_yield.png'))