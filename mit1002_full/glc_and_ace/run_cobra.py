import cobra
import pickle
import os

# Set the output directory (where the results.pkl file will be saved)
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Load in the ALT model using COBRApy
alt_cobra = cobra.io.read_sbml_model("../../GEM-repos/mit1002-model/model.xml")

# Make a medium with just glucose
# TODO: Use an uptake rate based on the NMR data
glc_medium = {'EX_cpd00027_e0': 10,  # D-Glucose_e0
              # Not sure what value to use for oxygen
              'EX_cpd00007_e0': 1000,  # O2_e0
              # Remaining minimal media components
              'EX_cpd00058_e0': 1000,  # Cu2+_e0
              'EX_cpd00971_e0': 1000,  # Na+_e0
              'EX_cpd00063_e0': 1000,  # Ca2+_e0
              'EX_cpd00048_e0': 1000,  # Sulfate_e0
              'EX_cpd10516_e0': 1000,  # fe3_e0
              'EX_cpd00254_e0': 1000,  # Mg_e0
              'EX_cpd00009_e0': 1000,  # Phosphate_e0
              'EX_cpd00205_e0': 1000,  # K+_e0
              'EX_cpd00013_e0': 1000,  # NH3_e0
              'EX_cpd00099_e0': 1000,  # Cl-_e0
              'EX_cpd00030_e0': 1000,  # Mn2+_e0
              'EX_cpd00075_e0': 1000,  # Nitrite_e0
              'EX_cpd00001_e0': 1000,  # H2O_e0
              'EX_cpd00635_e0': 1000,  # Cbl_e0
              'EX_cpd00034_e0': 1000,  # Zn2+_e0
              'EX_cpd00149_e0': 1000,  # Co2+_e0
              }

# Make a medium with just acetate
# TODO: Use an uptake rate based on the NMR data
ace_medium = {'EX_cpd00029_e0': 10,  # Acetate_e0
              'EX_cpd00007_e0': 1000,  # O2_e0
              # Remaining minimal media components
              'EX_cpd00058_e0': 1000,  # Cu2+_e0
              'EX_cpd00971_e0': 1000,  # Na+_e0
              'EX_cpd00063_e0': 1000,  # Ca2+_e0
              'EX_cpd00048_e0': 1000,  # Sulfate_e0
              'EX_cpd10516_e0': 1000,  # fe3_e0
              'EX_cpd00254_e0': 1000,  # Mg_e0
              'EX_cpd00009_e0': 1000,  # Phosphate_e0
              'EX_cpd00205_e0': 1000,  # K+_e0
              'EX_cpd00013_e0': 1000,  # NH3_e0
              'EX_cpd00099_e0': 1000,  # Cl-_e0
              'EX_cpd00030_e0': 1000,  # Mn2+_e0
              'EX_cpd00075_e0': 1000,  # Nitrite_e0
              'EX_cpd00001_e0': 1000,  # H2O_e0
              'EX_cpd00635_e0': 1000,  # Cbl_e0
              'EX_cpd00034_e0': 1000,  # Zn2+_e0
              'EX_cpd00149_e0': 1000,  # Co2+_e0
              }

# Make a medium with both glucose and acetate
# FIXME: Need the equivalent amount of carbon available in the medium
mix_medium = {'EX_cpd00027_e0': 10,  # D-Glucose_e0
              'EX_cpd00029_e0': 10,  # Acetate_e0
              'EX_cpd00007_e0': 1000,  # O2_e0
              # Remaining minimal media components
              'EX_cpd00058_e0': 1000,  # Cu2+_e0
              'EX_cpd00971_e0': 1000,  # Na+_e0
              'EX_cpd00063_e0': 1000,  # Ca2+_e0
              'EX_cpd00048_e0': 1000,  # Sulfate_e0
              'EX_cpd10516_e0': 1000,  # fe3_e0
              'EX_cpd00254_e0': 1000,  # Mg_e0
              'EX_cpd00009_e0': 1000,  # Phosphate_e0
              'EX_cpd00205_e0': 1000,  # K+_e0
              'EX_cpd00013_e0': 1000,  # NH3_e0
              'EX_cpd00099_e0': 1000,  # Cl-_e0
              'EX_cpd00030_e0': 1000,  # Mn2+_e0
              'EX_cpd00075_e0': 1000,  # Nitrite_e0
              'EX_cpd00001_e0': 1000,  # H2O_e0
              'EX_cpd00635_e0': 1000,  # Cbl_e0
              'EX_cpd00034_e0': 1000,  # Zn2+_e0
              'EX_cpd00149_e0': 1000,  # Co2+_e0
              }

# Run FBA- Glucose only
alt_cobra.medium = glc_medium
glc_only_fba = alt_cobra.optimize()

# Run pFBA- Glucose only
glc_only_pfba = cobra.flux_analysis.pfba(alt_cobra)

# Run FBA- Acetate only
alt_cobra.medium = ace_medium
ace_only_fba = alt_cobra.optimize()

# Run pFBA- Acetate only
ace_only_pfba = cobra.flux_analysis.pfba(alt_cobra)

# Run FBA- Glucose and Acetate
alt_cobra.medium = mix_medium
mix_fba = alt_cobra.optimize()

# Run pFBA- Glucose and Acetate
mix_pfba = cobra.flux_analysis.pfba(alt_cobra)

# Save results
with open(os.path.join(OUT_DIR, 'results.pkl'), 'wb') as f:
    pickle.dump([glc_only_fba,
                 glc_only_pfba,
                 ace_only_fba,
                 ace_only_pfba,
                 mix_fba,
                 mix_pfba], f)
