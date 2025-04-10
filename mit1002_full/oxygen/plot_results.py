import os
import pickle
import sys

import matplotlib.pyplot as plt
import seaborn as sns

# Import the plot styles (has global variables for colors)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from plot_styles import *

# Set the output directory
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Set a folder for the plots
output_folder = os.path.join(OUT_DIR, "plots")
# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the results
with open(os.path.join(OUT_DIR, "results.pkl"), "rb") as f:
    results = pickle.load(f)

# Line graph of actual oxygen import flux vs oxygen availability
g = results.plot(
    kind="line", x="oxygen_bound", y="oxygen_flux", marker="o", color=LIGHT_BLUE, legend=False
)
g.set_xlabel("Oxygen Availability (mmol/ [gDW h])", color="gray")
g.set_ylabel("Oxygen Flux (mmol/ [gDW h])", color="gray")
set_plot_style(g)
plt.savefig(os.path.join(output_folder, "oxygen.png"))

# Make the oxygen flux the absolute value
results["oxygen_flux"] = results["oxygen_flux"].abs()

# Line graph of CUE vs Oxygen
g = results.plot(
    kind="line", x="oxygen_flux", y="cue", marker="o", color=LIGHT_BLUE, legend=False
)
g.set_xlabel("Oxygen Availability (mmol/ [gDW h])", color="gray")
g.set_ylabel("CUE (mmol C/ mmol C)", color="gray")  # TODO: Check the units
set_plot_style(g)
plt.savefig(os.path.join(output_folder, "cue_oxygen.png"))

# Line graph of GGE vs Oxygen
g = results.plot(
    kind="line", x="oxygen_bound", y="gge", marker="o", color=LIGHT_BLUE, legend=False
)
g.set_xlabel("Oxygen Availability (mmol/ [gDW h])", color="gray")
g.set_ylabel("GGE (mmol C/ mmol C)", color="gray")  # TODO: Check the units
set_plot_style(g)
plt.savefig(os.path.join(output_folder, "gge_oxygen.png"))

# Stacked bar plot of carbon fates vs oxygen
data = results.set_index("oxygen_bound")[["co2", "organic_c", "biomass"]]
g = carbon_fates_bar(data)
g.set_xlabel("Oxygen Availability (mmol/ [gDW h])", color="gray")
g.set_ylabel("Carbon Flux (mmol C/ mmol C)", color="gray")  # TODO: Check the units
plt.savefig(os.path.join(output_folder, "carbon_fates_oxygen.png"))
