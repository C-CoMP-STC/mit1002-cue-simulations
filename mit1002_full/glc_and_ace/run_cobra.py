import os
import pickle

import cobra
import pandas as pd

# Set the output directory (where the results.pkl file will be saved)
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Load in the ALT model using COBRApy
alt_cobra = cobra.io.read_sbml_model("../../GEM-repos/GEM-mit1002/model.xml")

o2_values = [0, 5, 10, 20, 30, 1000]

# Make a medium with just glucose
# TODO: Use an uptake rate based on the NMR data
glc_medium = {
    "EX_cpd00027_e0": 10,  # D-Glucose_e0
    # Remaining minimal media components
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
    "EX_cpd00034_e0": 1000,  # Zn2+_e0
    "EX_cpd00149_e0": 1000,  # Co2+_e0
}

# Make a medium with just acetate
# TODO: Use an uptake rate based on the NMR data
ace_medium = {
    "EX_cpd00029_e0": 30,  # Acetate_e0
    # Remaining minimal media components
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
    "EX_cpd00034_e0": 1000,  # Zn2+_e0
    "EX_cpd00149_e0": 1000,  # Co2+_e0
}

# Make a medium with 2/3 glucose and 1/3 acetate
# FIXME: Need the equivalent amount of carbon available in the medium
glc_heavy_mix_medium = {
    "EX_cpd00027_e0": 6.667,  # D-Glucose_e0
    "EX_cpd00029_e0": 10,  # Acetate_e0
    # Remaining minimal media components
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
    "EX_cpd00034_e0": 1000,  # Zn2+_e0
    "EX_cpd00149_e0": 1000,  # Co2+_e0
}

# Make a medium with 1/3 glucose and 2/3 acetate
# FIXME: Need the equivalent amount of carbon available in the medium
ace_heavy_mix_medium = {
    "EX_cpd00027_e0": 3.333,  # D-Glucose_e0
    "EX_cpd00029_e0": 20,  # Acetate_e0
    # Remaining minimal media components
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
    "EX_cpd00034_e0": 1000,  # Zn2+_e0
    "EX_cpd00149_e0": 1000,  # Co2+_e0
}

media_wo_o2 = {
    "Glucose Only": glc_medium,
    "Acetate Only": ace_medium,
    "Glucose Heavy Mix": glc_heavy_mix_medium,
    "Acetate Heavy Mix": ace_heavy_mix_medium,
}

media_to_test = {}
# Make media with different O2 levels
for media in media_wo_o2:
    for o2 in o2_values:
        new_media_id = media + "(O2 = " + str(o2) + ")"
        media_to_test[new_media_id] = media_wo_o2[media].copy()
        media_to_test[new_media_id]["EX_cpd00007_e0"] = o2

# Define a list of P/O ratios to test
po_ratios = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]

# Define lists to hold the results
res_media_name = []
res_glucose = []
res_acetate = []
res_po_ratio = []
res_fba = []

# Loop through all the media
for name, medium in media_to_test.items():
    # Loop through all the P/O ratios
    for po_ratio in po_ratios:
        # Make a copy of the model to work with
        working_model = alt_cobra.copy()
        # Set the P/O ratio in the model
        working_model.reactions.rxn08173_c0.metabolites["cpd00067_e0"] = po_ratio[0]
        working_model.reactions.rxn08173_c0.metabolites["cpd00002_c0"] = po_ratio[1]
        # Run FBA
        working_model.medium = medium
        fba_result = working_model.optimize()
        # Save the results
        res_media_name.append(name)
        res_glucose.append(medium["EX_cpd00027_e0"])
        res_acetate.append(medium["EX_cpd00029_e0"])
        res_po_ratio.append(po_ratio)
        res_fba.append(fba_result)


# Save results
with open(os.path.join(OUT_DIR, "results.pkl"), "wb") as f:
    pickle.dump(cobra_results, f)
