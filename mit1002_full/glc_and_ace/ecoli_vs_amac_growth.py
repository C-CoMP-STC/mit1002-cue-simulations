import os
import pickle
import sys

import cobra
import matplotlib.pyplot as plt
import pandas as pd

# Import the plot styles (has global variables for colors)
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)
from plot_styles import *

# Set the output directory (where the results.pkl file will be saved)
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Set a folder for the plots
output_folder = os.path.join(OUT_DIR, "plots")
# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load in the ALT model
amac = cobra.io.read_sbml_model("../../GEM-repos/mit1002-model/model.xml")
amac.id = "amac"

# Load the E. coli full model
ecoli = cobra.io.read_sbml_model("../../GEM-repos/ecoli/iJO1366.xml")

# Define a medium with glucose only
glc_medium = {
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
    "EX_cpd00635_e0": 1000,  # Cbl_e0
    "EX_cpd00034_e0": 1000,  # Zn2+_e0
    "EX_cpd00149_e0": 1000,  # Co2+_e0
}

# Define a medium with acetate only
ace_medium = {
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
    "EX_cpd00635_e0": 1000,  # Cbl_e0
    "EX_cpd00034_e0": 1000,  # Zn2+_e0
    "EX_cpd00149_e0": 1000,  # Co2+_e0
}

# Define a medium with glucose and acetate (at the same levels as when they were alone)
mix_medium = {
    "EX_cpd00027_e0": 10,  # D-Glucose_e0
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
    "EX_cpd00635_e0": 1000,  # Cbl_e0
    "EX_cpd00034_e0": 1000,  # Zn2+_e0
    "EX_cpd00149_e0": 1000,  # Co2+_e0
}

models = [ecoli, amac]
media = {"Glucose": glc_medium, "Acetate": ace_medium, "Mixture": mix_medium}

results = {}

# Run the E. coli model super manually because it uses BiGG IDs, not ModelSEED IDs
# Glucose
ecoli.reactions.get_by_id("EX_glc__D_e").lower_bound = -10
ecoli.reactions.get_by_id("EX_ac_e").lower_bound = 0
o2_results = []
for o2 in [1000, 20]:
    ecoli.reactions.get_by_id("EX_o2_e").lower_bound = -o2
    o2_results.append(ecoli.optimize().objective_value)
results["E. coli on Glucose"] = o2_results
# Acetate
ecoli.reactions.get_by_id("EX_glc__D_e").lower_bound = 0
ecoli.reactions.get_by_id("EX_ac_e").lower_bound = -30
o2_results = []
for o2 in [1000, 20]:
    ecoli.reactions.get_by_id("EX_o2_e").lower_bound = -o2
    o2_results.append(ecoli.optimize().objective_value)
results["E. coli on Acetate"] = o2_results
# Mixture
ecoli.reactions.get_by_id("EX_glc__D_e").lower_bound = -10
ecoli.reactions.get_by_id("EX_ac_e").lower_bound = -30
o2_results = []
for o2 in [1000, 20]:
    ecoli.reactions.get_by_id("EX_o2_e").lower_bound = -o2
    o2_results.append(ecoli.optimize().objective_value)
results["E. coli on Mixture"] = o2_results

# Run the Amac model
for medium in media:
    # Set the medium
    amac.medium = media[medium]
    # Make a list to hold the results of the high and low O2 conditions
    o2_results = []
    for o2 in [1000, 20]:
        amac.reactions.get_by_id("EX_cpd00007_e0").lower_bound = -o2
        o2_results.append(amac.optimize().objective_value)
    results["A. mac on " + medium] = o2_results

# Make a pandas DataFrame with the results
df = pd.DataFrame.from_dict(results, orient="index")

# Rename the columns
df.columns = ["Infinite O2", "Realistic O2"]

# Make the index a column
df.reset_index(inplace=True)

# Plot a grouped bar chart with the infinite and realistic O2 conditions for each model/medium pair
g = df.plot(x="index", kind="bar", stacked=False, title="Growth on Glucose and Acetate", color=[DARK_BLUE, LIGHT_BLUE])
# Plot style
g.set_xlabel(None)
g.set_ylabel("Biomass Flux (mmol/gDW hr)", color="gray")
plt.tight_layout()
set_plot_style(g)
# Save
plt.savefig(os.path.join(output_folder, "growth_comparison.png"))

# Plot just the realistic O2 conditions
g = df.plot(x="index", y="Realistic O2", kind="bar", title="Growth on Glucose and Acetate", color=LIGHT_BLUE)
# Plot style
g.set_xlabel(None)
g.set_ylabel("Biomass Flux (mmol/gDW hr)", color="gray")
plt.tight_layout()
set_plot_style(g)
# Save
plt.savefig(os.path.join(output_folder, "growth_comparison_realistic_o2.png"))
