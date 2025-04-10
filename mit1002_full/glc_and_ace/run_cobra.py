import os
import pickle

import cobra

# Set the output directory (where the results.pkl file will be saved)
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Load in the ALT model using COBRApy
alt_cobra = cobra.io.read_sbml_model("../../GEM-repos/GEM-mit1002/model.xml")

# Make a medium with just glucose
# TODO: Use an uptake rate based on the NMR data
glc_medium_inf_o2 = {
    "EX_cpd00027_e0": 10,  # D-Glucose_e0
    "EX_cpd00007_e0": 1000,  # O2_e0
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
ace_medium_inf_o2 = {
    "EX_cpd00029_e0": 30,  # Acetate_e0
    "EX_cpd00007_e0": 1000,  # O2_e0
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
glc_heavy_mix_medium_inf_o2 = {
    "EX_cpd00027_e0": 6.667,  # D-Glucose_e0
    "EX_cpd00029_e0": 10,  # Acetate_e0
    "EX_cpd00007_e0": 1000,  # O2_e0
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
ace_heavy_mix_medium_inf_o2 = {
    "EX_cpd00027_e0": 3.333,  # D-Glucose_e0
    "EX_cpd00029_e0": 20,  # Acetate_e0
    "EX_cpd00007_e0": 1000,  # O2_e0
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


# Make a medium with just glucose
# TODO: Use an uptake rate based on the NMR data
glc_medium_real_o2 = {
    "EX_cpd00027_e0": 10,  # D-Glucose_e0
    "EX_cpd00007_e0": 20,  # O2_e0
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
ace_medium_real_o2 = {
    "EX_cpd00029_e0": 30,  # Acetate_e0
    "EX_cpd00007_e0": 20,  # O2_e0
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
glc_heavy_mix_medium_real_o2 = {
    "EX_cpd00027_e0": 6.667,  # D-Glucose_e0
    "EX_cpd00029_e0": 10,  # Acetate_e0
    "EX_cpd00007_e0": 20,  # O2_e0
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
ace_heavy_mix_medium_real_o2 = {
    "EX_cpd00027_e0": 3.333,  # D-Glucose_e0
    "EX_cpd00029_e0": 20,  # Acetate_e0
    "EX_cpd00007_e0": 20,  # O2_e0
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

# Make a dictionary of the media with names
media = {
    "glc_medium_inf_o2": glc_medium_inf_o2,
    "ace_medium_inf_o2": ace_medium_inf_o2,
    "glc_heavy_mix_medium_inf_o2": glc_heavy_mix_medium_inf_o2,
    "ace_heavy_mix_medium_inf_o2": ace_heavy_mix_medium_inf_o2,
    "glc_medium_real_o2": glc_medium_real_o2,
    "ace_medium_real_o2": ace_medium_real_o2,
    "glc_heavy_mix_medium_real_o2": glc_heavy_mix_medium_real_o2,
    "ace_heavy_mix_medium_real_o2": ace_heavy_mix_medium_real_o2,
}

# Loop through all the media and run FBA and pFBA and put the results in a dictionary
cobra_results = {}
for name, medium in media.items():
    # Run FBA
    alt_cobra.medium = medium
    fba_result = alt_cobra.optimize()
    cobra_results[name + "_fba"] = fba_result
    # Run pFBA
    pfba_result = cobra.flux_analysis.pfba(alt_cobra)
    cobra_results[name + "_pfba"] = pfba_result

# Save results
with open(os.path.join(OUT_DIR, "results.pkl"), "wb") as f:
    pickle.dump(cobra_results, f)
