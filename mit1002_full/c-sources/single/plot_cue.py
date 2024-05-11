import os
import sys

import cobra
import pandas as pd

# Import the plot styles (has global variables for colors)
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
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

# Filter so that only the feasible growth simulations are included
results = results[results["feasible_growth"]]

# Stacked bar plot of the carbon fates for the different conditions
data = results.set_index("c_source")[["biomass", "organic_c", "co2"]]
g = carbon_fates_bar(data)
plt.savefig(os.path.join(output_folder, "carbon_fates.png"))

# Stacked bar plot of the normalized carbon fates for the different conditions
data_norm = results.set_index("c_source")[["biomass_norm", "organic_c_norm", "co2_norm"]]
# Rename the columns to match the function
data_norm.columns = ["biomass", "organic_c", "co2"]
g_norm = carbon_fates_bar(data_norm)
plt.savefig(os.path.join(output_folder, "carbon_fates_norm.png"))

# Scatter plot of CUE/GGE vs the number of carbons in the carbon source
g = results.plot.scatter(x="c_num", y="cue", color=LIGHT_BLUE)
g.set_xlabel("Number of Carbon Atoms", color="gray")
g.set_ylabel("CUE (mmol C/ mmol C)", color="gray")  # TODO: Check the units
g.set_title("CUE vs Number of Carbon Atoms", color="gray")
set_plot_style(g)
plt.savefig(os.path.join(output_folder, "cue_c_num.png"))

g = results.plot.scatter(x="c_num", y="gge", color=LIGHT_BLUE)
g.set_xlabel("Number of Carbon Atoms", color="gray")
g.set_ylabel("GGE (mmol C/ mmol C)", color="gray")  # TODO: Check the units
g.set_title("GGE vs Number of Carbon Atoms", color="gray")
set_plot_style(g)
plt.savefig(os.path.join(output_folder, "gge_c_num.png"))

# Scatter plot of CUE/GGE vs C:N ratio
g = results.plot.scatter(x="cn_ratio", y="cue", color=LIGHT_BLUE)
g.set_xlabel("C:N Ratio", color="gray")
g.set_ylabel("CUE (mmol C/ mmol C)", color="gray")  # TODO: Check the units
g.set_title("CUE vs C:N Ratio", color="gray")
set_plot_style(g)
plt.savefig(os.path.join(output_folder, "cue_cn_ratio.png"))

g = results.plot.scatter(x="cn_ratio", y="gge", color=LIGHT_BLUE)
g.set_xlabel("C:N Ratio", color="gray")
g.set_ylabel("GGE (mmol C/ mmol C)", color="gray")  # TODO: Check the units
g.set_title("GGE vs C:N Ratio", color="gray")
set_plot_style(g)
plt.savefig(os.path.join(output_folder, "gge_cn_ratio.png"))

# Scatter plot of CUE/GGE vs degree of oxidation
g = results.plot.scatter(x="deg_of_reduction", y="cue", color=LIGHT_BLUE)
g.set_xlabel("Degree of Reduction", color="gray")
g.set_ylabel("CUE (mmol C/ mmol C)", color="gray")  # TODO: Check the units
g.set_title("CUE vs Degree of Reduction", color="gray")
set_plot_style(g)
plt.savefig(os.path.join(output_folder, "cue_deg_of_reduction.png"))

g = results.plot.scatter(x="deg_of_reduction", y="gge", color=LIGHT_BLUE)
g.set_xlabel("Degree of Reduction", color="gray")
g.set_ylabel("GGE (mmol C/ mmol C)", color="gray")  # TODO: Check the units
g.set_title("GGE vs Degree of Reduction", color="gray")
set_plot_style(g)
plt.savefig(os.path.join(output_folder, "gge_deg_of_reduction.png"))
