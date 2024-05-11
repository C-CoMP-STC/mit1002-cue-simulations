import os
import pickle

import cobra
import numpy as np
import pandas as pd
from gem2cue import (
    utils,  # Import the working version (works with the med4-hot1a3 conda env)
)

# Set the output directory (where the results.pkl file will be saved)
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Load in the ALT model using COBRApy
model = cobra.io.read_sbml_model("../../GEM-repos/mit1002-model/model.xml")

# Get the exchange reactions
c_ex_rxns = utils.get_c_ex_rxns(model)

# Define a medium with no carbon sources
minimal_medium = {
    "EX_cpd00007_e0": 20,  # O2_e0
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

########################################################################
# Loop through the carbon sources
########################################################################
# Make a dataframe to store the results
cobra_results = {}
# Loop through all the carbon sources
for c_ex_rxn in c_ex_rxns:
    # Get the number of carbon atoms in the metabolite
    c_num = c_ex_rxns[c_ex_rxn]
    # Make a new medium based on the defined minimal medium
    medium = minimal_medium.copy()
    medium[c_ex_rxn] = (
        60 / c_num  # Same as a LB of 10 for glucose, but scaled by the number of carbons
    )
    # Then set the medium
    model.medium = medium

    # Run FBA
    sol = model.optimize()

    # Add the FBA results to the results dictionary
    cobra_results[c_ex_rxn] = sol

# Save the results
with open(os.path.join(OUT_DIR, "results.pkl"), "wb") as f:
    pickle.dump(cobra_results, f)
