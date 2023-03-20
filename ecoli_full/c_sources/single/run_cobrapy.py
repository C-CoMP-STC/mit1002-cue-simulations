import cobra
import pickle
import pandas as pd
import numpy as np

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
                   extract_c_fates_from_solution)

# This script runs and saves the results from a COBRApy simulation of
# the E. coli full model, with a minimal medium with only one carbon
# source

# Load the E. coli full model, using the built in model from COBRApy
model = cobra.io.load_model("iJO1366")

# Get the exchange reactions
c_ex_rxns = atomExchangeMetabolite(model)

########################################################################
# Loop through the carbon sources
########################################################################
# Make a dataframe to store the results
results = []
# Loop through all the carbon sources
for c_ex_rxn in c_ex_rxns:
    # Make a new medium based on the medium in the model file
    medium = model.medium
    # Remove all the carbon sources from the medium
    for r in medium:
        for met in model.reactions.get_by_id(r).metabolites:
            if 'C' in met.elements:
                medium[r] = 0
    # Constrain the oxygen to something reasonable
    medium['EX_o2_e'] = 6
    medium[c_ex_rxn] = 10 # CHECK: Should I be using the same concentration for all carbon sources? Or have it be based on the number of carbon sources in the metabolite?
    # Then set the medium
    model.medium = medium

    # Run FBA
    sol = model.optimize()

    # Extract the carbon fates for the solution
    c_fates = extract_c_fates_from_solution(sol, c_ex_rxns, norm=False)
    uptake = c_fates[0]
    respiration = c_fates[1]
    exudation = c_fates[2]
    biomass = c_fates[3]

    # Calculate CUE from the c fates (not using my function)
    cue = 1 - respiration/uptake

    # Calculate GGE from the c fates (not using my function)
    gge = 1 - (respiration + exudation)/uptake
    
    # Save
    d = {'c-source': c_ex_rxn,
         'c-source-flux': sol.fluxes[c_ex_rxn],
        'fluxes': sol.fluxes,
        'uptake': uptake, 
        'respiration': respiration,
        'exudation': exudation,
        'biomass': biomass,
        'cue': cue,
        'gge': gge}
    results.append(d)

results = pd.DataFrame(results)

########################################################################
# Save the results
########################################################################
with open('ecoli_full/c_sources/single/results.pkl', 'wb') as f:
    pickle.dump(results, f)