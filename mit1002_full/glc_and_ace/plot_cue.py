import os
import sys

import cobra
import pandas as pd

# Import the plot styles (has global variables for colors)
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)
from plot_styles import *

# Set the output directory
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Set a folder for the plots
output_folder = os.path.join(OUT_DIR, "plots")
# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the results
results = pd.read_csv(os.path.join(OUT_DIR, "results.csv"))

# Add a column for the condition name with a list of names
# FIXME: This is fragile to the order of the results- find a way to use the solution directly
condition_names = ["glc_inf_o2 (FBA)",
                   "glc_inf_o2 (pFBA)",
                   "glc_lim_o2 (FBA)",
                   "glc_lim_o2 (pFBA)",
                   "ace_inf_o2 (FBA)",
                   "ace_inf_o2 (pFBA)",
                   "ace_lim_o2 (FBA)",
                   "ace_lim_o2 (pFBA)",
                   "mix_inf_o2 (FBA)",
                   "mix_inf_o2 (pFBA)",
                   "mix_lim_o2 (FBA)",
                   "mix_lim_o2 (pFBA)"]
results["condition"] = condition_names

# Stacked bar plot of the carbon fates for the different conditions
data = results.set_index("condition")[["co2", "organic_c", "biomass"]]
g = carbon_fates_bar(data)
g.set_xlabel("Simulation Conditions", color="gray")
g.set_ylabel("Carbon Flux (mmol C/ mmol C)", color="gray")  # TODO: Check the units
plt.savefig(os.path.join(output_folder, "carbon_fates.png"))