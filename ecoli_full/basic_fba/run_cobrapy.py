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
# the E. coli full model, with varying nitrogen, carbon, and ATP
# maintenance

# Load the E. coli full model, using the built in model from COBRApy
model = cobra.io.load_model("iJO1366")

# Get the exchange reactions
c_ex_rxns = atomExchangeMetabolite(model)

########################################################################
# Varying Nitrogen
########################################################################
# Make a dataframe to store the results
data = []
# Loop through the carbon concentrations
for ammonia in range(0, 101, 10): # What range should I use?
    # Make a new medium based on the medium in the model file
    medium = model.medium
    # Constrain theglucose to something reasonable
    medium['EX_glc__D_e'] = 10
    # Try not constraining the oxygen
    medium['EX_o2_e'] = 1000
    # Upate the ammonia in the medium
    medium['EX_nh4_e'] = ammonia
    # Then set the medium
    model.medium = medium

    # Check that there are no other media components with nitrogen
    # for r in medium:
    #     for met in model.reactions.get_by_id(r).metabolites:
    #         if 'N' in met.elements:
    #             print(r + ": " + str(met.elements['N']))
    # Cob(I)alamin (vitamin B12) is the only other metabolite with
    # nitrogen in the medium
    # Should I be setting that to 0 as well?

    for vm in np.linspace(0, 20, 5):
        # Update maintainance flux
        model.reactions.ATPM.lower_bound = vm

        # Perform FBA
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
        d = {'ammonia': ammonia, 
             'vm': vm,
             'fluxes': sol.fluxes,
             'uptake': uptake, 
             'respiration': respiration,
             'exudation': exudation,
             'biomass': biomass,
             'cue': cue,
             'gge': gge}
        data.append(d)

nitrogen_results = pd.DataFrame(data)

########################################################################
# Varying Carbon
########################################################################
# Make a dataframe to store the results
data = []
# Loop through the carbon concentrations
for glc in range(10, 21):
    # Make a new medium based on the medium in the model file
    medium = model.medium
    # Try not constraining the oxygen
    medium['EX_o2_e'] = 1000
    # Do not contrain the ammonia
    medium['EX_nh4_e'] = 1000
    # Upate the glucose in the medium
    medium['EX_glc__D_e'] = glc
    # Then set the medium
    model.medium = medium

    # Check that the export reaction bounds are 0 for all carbon sources
    # except glucose
    # for rxn in c_ex_rxns:
    #     print(rxn + ": " + str(model.reactions.get_by_id(rxn).bounds))

    for vm in np.linspace(0, 20, 5):
        # Update maintainance flux
        model.reactions.ATPM.lower_bound = vm

        # Perform FBA
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
        d = {'glc': glc,
             'vm': vm,
             'fluxes': sol.fluxes,
             'uptake': uptake, 
             'respiration': respiration,
             'exudation': exudation,
             'biomass': biomass,
             'cue': cue,
             'gge': gge}
        data.append(d)

carbon_results = pd.DataFrame(data)

########################################################################
# Varying ATP Maintenance
########################################################################
# Make a dataframe to store the results
data = []
for vm in np.linspace(0, 20, 5):
    # Can I move this outside the vm loop?
    # Make a new medium based on the medium in the model file
    medium = model.medium
    # Constrain the glucose to something reasonable
    medium['EX_glc__D_e'] = 10
    # Try not constraining the oxygen
    medium['EX_o2_e'] = 1000
    # Do not constain the ammonia in the medium
    medium['EX_nh4_e'] = 1000
    # Then set the medium
    model.medium = medium

    # Update maintainance flux
    model.reactions.ATPM.lower_bound = vm

    # Perform FBA
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
    d = {'vm': vm,
         'fluxes': sol.fluxes,
         'uptake': uptake, 
         'respiration': respiration,
         'exudation': exudation,
         'biomass': biomass,
         'cue': cue,
         'gge': gge}
    data.append(d)

vm_results = pd.DataFrame(data)

########################################################################
# Save the results
########################################################################
results = [nitrogen_results, carbon_results, vm_results]
with open('ecoli_full/basic_fba/results.pkl', 'wb') as f:
    pickle.dump(results, f)