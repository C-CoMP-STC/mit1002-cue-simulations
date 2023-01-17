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
# I think I would rather do this in the comets_simulation script, and
# save the exchange reactions with the results, but for now just do it
# here
c_ex_rxns = atomExchangeMetabolite(e_coli_cobra)

# Calculate cimmulative fluxes across the entire simulation
fluxes_by_cycle = experiment.fluxes_by_species['e_coli_core']
cumulative_fluxes = fluxes_by_cycle.iloc[:,3:].sum(axis=0).to_dict()
cumulative_ex_fluxes = {r: cumulative_fluxes[r] * -c for r, c in c_ex_rxns.items()}

# Calculate cumulative CUE
uptake = sum([flux for rxn, flux in cumulative_ex_fluxes.items() if flux > 0])
respiration = cumulative_ex_fluxes['EX_co2_e']
cumulative_cue = 1 + respiration/uptake

print(cumulative_cue)