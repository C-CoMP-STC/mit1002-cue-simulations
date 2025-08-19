import os
import pickle

import cobra
import pandas as pd
from gem2cue import (
    utils,  # Import the working version (works with the med4-hot1a3 conda env)
)

# Set the output directory
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Load the model and get the exchange reactions
model = cobra.io.read_sbml_model("../../GEM-repos/GEM-mit1002/model.xml")
c_ex_rxns = utils.get_c_ex_rxns(model)

# Load the results
with open(os.path.join(OUT_DIR, "results.pkl"), "rb") as f:
    cobra_results = pickle.load(f)

# Extract the carbon fate results from the FBA fluxes and add them to the cobra_results DataFrame
for index, row in cobra_results.iterrows():
    # Extract the FBA result
    fba_result = row["fba_result"]
    # Add the growth rate to the DataFrame
    growth_rate = fba_result.objective_value
    cobra_results.at[index, "growth_rate"] = growth_rate
    # Escape if the the model isn't growing
    if not growth_rate > 1e-6:
        print(f"Skipping row {index} because the model is not growing")
        continue
    # Extract the carbon fates for the solution (both normalized and not normalized)
    c_fates = utils.extract_c_fates_from_solution(
        fba_result, c_ex_rxns, co2_ex_rxn="EX_cpd00011_e0", norm=False
    )
    uptake = c_fates[0]
    co2 = c_fates[1]
    organic_c = c_fates[2]
    biomass = c_fates[3]

    c_fates_norm = utils.extract_c_fates_from_solution(
        fba_result, c_ex_rxns, co2_ex_rxn="EX_cpd00011_e0", norm=True
    )
    co2_norm = c_fates_norm[0]
    organic_c_norm = c_fates_norm[1]
    biomass_norm = c_fates_norm[2]

    # Calculate CUE from the c fates (not using my function)
    cue = 1 - co2 / uptake

    # Calculate GGE from the c fates (not using my function)
    gge = 1 - (co2 + organic_c) / uptake

    # Calculate the BGE from the c fates
    bge = biomass / (biomass + co2)

    # Add the results to the DataFrame
    cobra_results.at[index, "oxygen_flux"] = fba_result.fluxes["EX_cpd00007_e0"]
    cobra_results.at[index, "uptake"] = uptake
    cobra_results.at[index, "co2"] = co2
    cobra_results.at[index, "organic_c"] = organic_c
    cobra_results.at[index, "biomass"] = biomass
    cobra_results.at[index, "co2_norm"] = co2_norm
    cobra_results.at[index, "organic_c_norm"] = organic_c_norm
    cobra_results.at[index, "biomass_norm"] = biomass_norm
    cobra_results.at[index, "cue"] = cue
    cobra_results.at[index, "gge"] = gge
    cobra_results.at[index, "bge"] = bge

# Drop the fba_result column as it's no longer needed
cobra_results.drop(columns=["fba_result"], inplace=True)

# Save the results
cobra_results.to_csv(os.path.join(OUT_DIR, "results.csv"), index=False)
