# Extract the flux data from the results and get it into a JSON file for Escher

import json
import os
import pickle

# Set the output directory (where the results.pkl file will be saved)
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Load the results.pkl file
with open(os.path.join(OUT_DIR, "results.pkl"), "rb") as f:
    results = pickle.load(f)

# Get the flux data
glc_results = results["glc_medium_real_o2_fba"].fluxes.to_dict()
ace_results = results["ace_medium_real_o2_fba"].fluxes.to_dict()

# Make JSON files from the dictionaries
with open(os.path.join(OUT_DIR, "glc_flux.json"), "w") as f:
    json.dump(glc_results, f)
with open(os.path.join(OUT_DIR, "ace_flux.json"), "w") as f:
    json.dump(ace_results, f)
