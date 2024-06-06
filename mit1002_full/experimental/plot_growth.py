import os
import sys

import matplotlib.pyplot as plt
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

# Load Zac's OD results
od_results = pd.read_csv(
    "/Users/helenscott/Documents/PhD/Segre-lab/CUE/Zac txt data/MIT1002_singles_OD600.txt", sep="\t"
)

# Plot OD growth curves
plt.figure()
# Plot each column as its own line with "Time" as the x axis
for col in od_results.columns[1:]:
    # Define the color for the line, based on the column name
    if "glucose" in col:
        color = DARK_BLUE
    elif "acetate" in col:
        color = LIGHT_BLUE
    else:
        color = "gray"
    plt.plot(od_results["Time"], od_results[col], label=col, color=color)
plt.xlabel("Time (hours)")
plt.ylabel("OD600")
# Make a legend that only shows the three possible colors (the first of each type)
handles, labels = plt.gca().get_legend_handles_labels()
# Remove the .1, .2, .3 from the labels
labels = [label.split(".")[0] for label in labels]
unique_labels = set(labels)
unique_handles = [handles[labels.index(label)] for label in unique_labels]
plt.legend(unique_handles, unique_labels)
set_plot_style(plt.gca())
# Save the plot
plt.savefig(os.path.join(output_folder, "growth_curves.png"))
