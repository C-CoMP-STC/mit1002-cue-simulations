import os
import pickle

import cobra
import numpy as np
import pandas as pd
from gem2cue import utils

# Set the output directory
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Load the model
model = cobra.io.read_sbml_model("../../GEM-repos/mit1002-model/model.xml")

# Make a new medium based on the medium in the model file
# Define a medium with no carbon sources
medium = {
    "EX_cpd00027_e0": 10,  # Glucose_e0
    "EX_cpd00007_e0": 1000,  # O2_e0
    "EX_cpd00058_e0": 1000,  # Cu2+_e0
    "EX_cpd00971_e0": 1000,  # Na+_e0
    "EX_cpd00063_e0": 1000,  # Ca2+_e0
    "EX_cpd00048_e0": 1000,  # Sulfate_e0
    "EX_cpd10516_e0": 1000,  # fe3_e0
    "EX_cpd00254_e0": 1000,  # Mg_e0
    "EX_cpd00009_e0": 1000,  # Phosphate_e0
    "EX_cpd00205_e0": 1000,  # K+_e0
    "EX_cpd00013_e0": 1000,  # NH3_e0
    "EX_cpd00099_e0": 1000,  # Cl-_e0
    "EX_cpd00030_e0": 1000,  # Mn2+_e0
    "EX_cpd00075_e0": 1000,  # Nitrite_e0
    "EX_cpd00001_e0": 1000,  # H2O_e0
    "EX_cpd00635_e0": 1000,  # Cbl_e0, technically has C, but it wasn't used during growth on glucose or acetate
    "EX_cpd00034_e0": 1000,  # Zn2+_e0
    "EX_cpd00149_e0": 1000,  # Co2+_e0
}
# Then set the medium
model.medium = medium

# Get the exchange reactions
c_ex_rxns = utils.get_c_ex_rxns(model)


# Function to run the simulation with varying oxygen levels
def run_simulation(oxygen_levels):
    results = []
    for oxygen in oxygen_levels:
        # Set oxygen availability
        medium = model.medium
        medium["EX_cpd00007_e0"] = oxygen
        model.medium = medium

        # Run FBA
        sol = model.optimize()

        # Extract the carbon fates for the solution
        c_fates = utils.extract_c_fates_from_solution(
            sol, c_ex_rxns, co2_ex_rxn="EX_cpd00011_e0", norm=False
        )
        uptake = c_fates[0]
        co2 = c_fates[1]
        organic_c = c_fates[2]
        biomass = c_fates[3]

        # Calculate CUE from the c fates (not using my function)
        cue = 1 - co2 / uptake

        # Calculate GGE from the c fates (not using my function)
        gge = 1 - (co2 + organic_c) / uptake

        results.append(
            {
                "oxygen_bound": oxygen,
                "oxygen_flux": sol.fluxes["EX_cpd00007_e0"],
                "fluxes": sol.fluxes,
                "uptake": uptake,
                "co2": co2,
                "organic_c": organic_c,
                "biomass": biomass,
                "cue": cue,
                "gge": gge,
            }
        )

    return results


# Define a range of oxygen levels
oxygen_levels = np.linspace(0, 30, 31)

# Run the simulation
results = run_simulation(oxygen_levels)

# Convert the results to a DataFrame
results_df = pd.DataFrame(results)

# Save the results
with open(os.path.join(OUT_DIR, "results.pkl"), "wb") as f:
    pickle.dump(results_df, f)
