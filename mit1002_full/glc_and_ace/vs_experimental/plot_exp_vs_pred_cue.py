import os
import sys

import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Import the plot styles (has global variables for colors)
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
)
from plot_styles import *

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(FILE_DIR, "plots")

# If the output directory doesn't exist, create it
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

# Load the experimental results
# TODO: Recalculate the values myself from the raw data
# For now I'll just hardcode the values with what is in the "BGE for Helen"
# spreadsheet from Mary Ann
# Define the columns of the dataframe to be the different conditions
data = {
    "Glucose Only": [0.76],
    "Acetate Only": [0.38],
    "Glucose 8mM, Acetate 4mM": [0.77],
    "Acetate 8mM, Glucose 4mM (Early)": [0.74],
    "Acetate 8mM, Glucose 4mM (Late)": [0.56],
}
# Convert data to a pandas DataFrame
bge_df = pd.DataFrame(data)
# Set the index of the row to be a helpful name
bge_df.index = ["Experimental"]

# Load the FBA-predicted results
fba_data = pd.read_csv(os.path.join(os.path.dirname(FILE_DIR), "results.csv"), header=0)

# Filter the FBA data to only keep rows where "po_ratio" is "(4,1)"
fba_data = fba_data[fba_data["po_ratio"] == "(4, 1)"]

# Add the FBA-predicted results to the dataframe
bge_df.loc["FBA (O2=10)"] = {
    "Glucose Only": fba_data[
        (fba_data["media_name"] == "Glucose Only") & (fba_data["o2"] == 10)
    ]["bge"].iloc[0],
    "Acetate Only": fba_data[
        (fba_data["media_name"] == "Acetate Only") & (fba_data["o2"] == 10)
    ]["bge"].iloc[0],
    "Glucose 8mM, Acetate 4mM": fba_data[
        (fba_data["media_name"] == "Glucose 8mM, Acetate 4mM") & (fba_data["o2"] == 10)
    ]["bge"].iloc[0],
    "Acetate 8mM, Glucose 4mM (Early)": fba_data[
        (fba_data["media_name"] == "Acetate 8mM, Glucose 4mM") & (fba_data["o2"] == 10)
    ]["bge"].iloc[0],
    "Acetate 8mM, Glucose 4mM (Late)": fba_data[
        (fba_data["media_name"] == "Acetate 8mM, Glucose 4mM") & (fba_data["o2"] == 10)
    ]["bge"].iloc[0],
}
bge_df.loc["FBA (O2=20)"] = {
    "Glucose Only": fba_data[
        (fba_data["media_name"] == "Glucose Only") & (fba_data["o2"] == 20)
    ]["bge"].iloc[0],
    "Acetate Only": fba_data[
        (fba_data["media_name"] == "Acetate Only") & (fba_data["o2"] == 20)
    ]["bge"].iloc[0],
    "Glucose 8mM, Acetate 4mM": fba_data[
        (fba_data["media_name"] == "Glucose 8mM, Acetate 4mM") & (fba_data["o2"] == 20)
    ]["bge"].iloc[0],
    "Acetate 8mM, Glucose 4mM (Early)": fba_data[
        (fba_data["media_name"] == "Acetate 8mM, Glucose 4mM") & (fba_data["o2"] == 20)
    ]["bge"].iloc[0],
    "Acetate 8mM, Glucose 4mM (Late)": fba_data[
        (fba_data["media_name"] == "Acetate 8mM, Glucose 4mM") & (fba_data["o2"] == 20)
    ]["bge"].iloc[0],
}
bge_df.loc["FBA (O2=30)"] = {
    "Glucose Only": fba_data[
        (fba_data["media_name"] == "Glucose Only") & (fba_data["o2"] == 30)
    ]["bge"].iloc[0],
    "Acetate Only": fba_data[
        (fba_data["media_name"] == "Acetate Only") & (fba_data["o2"] == 30)
    ]["bge"].iloc[0],
    "Glucose 8mM, Acetate 4mM": fba_data[
        (fba_data["media_name"] == "Glucose 8mM, Acetate 4mM") & (fba_data["o2"] == 30)
    ]["bge"].iloc[0],
    "Acetate 8mM, Glucose 4mM (Early)": fba_data[
        (fba_data["media_name"] == "Acetate 8mM, Glucose 4mM") & (fba_data["o2"] == 30)
    ]["bge"].iloc[0],
    "Acetate 8mM, Glucose 4mM (Late)": fba_data[
        (fba_data["media_name"] == "Acetate 8mM, Glucose 4mM") & (fba_data["o2"] == 30)
    ]["bge"].iloc[0],
}

# Order the columns in increasing order (for the Experimental data)
bge_df_sorted = bge_df[bge_df.loc["Experimental"].sort_values().index]

# Plot the predicted vs experimental
# Transpose the DataFrame to make rows into columns for easier plotting
bge_df_transposed = bge_df_sorted.T

# Save the transposed DataFrame to a CSV file
bge_df_transposed.to_csv(os.path.join(OUT_DIR, "bge_exp_vs_fba.csv"))

# Define mappings for shapes and colors
# Get unique conditions from the index
conditions = bge_df_transposed.index.unique()
markers = ["o", "s", "^", "D", "v", "P", "*", "X"]
shape_map = {
    condition: markers[i % len(markers)] for i, condition in enumerate(conditions)
}

# Get unique FBA columns
fba_cols = [col for col in bge_df_transposed.columns if col.startswith("FBA")]
colors = [DARK_BLUE, ORANGE, LIGHT_BLUE]
color_map = {col: colors[i] for i, col in enumerate(fba_cols)}

# Create the plot
fig, ax = plt.subplots(figsize=(6, 6))

# Plot each point with the corresponding shape and color
for fba_col in fba_cols:
    for condition in bge_df_transposed.index:
        x = bge_df_transposed.loc[condition, "Experimental"]
        y = bge_df_transposed.loc[condition, fba_col]

        # Only plot if the y-value is not NaN
        if pd.notna(y):
            ax.scatter(
                x,
                y,
                color=color_map[fba_col],
                marker=shape_map[condition],
                s=100,  # Set marker size
                alpha=0.8,
                edgecolors="k",
                linewidths=0.5,
            )

# Plot a diagonal line for reference
min_value = 0
max_value = 1
ax.plot(
    [min_value, max_value],
    [min_value, max_value],
    color="gray",
    linestyle="--",
    linewidth=1,
    label="1:1 Line",
)

# Create custom legends
# For colors (FBA conditions)
color_legend_elements = [
    mlines.Line2D(
        [0],
        [0],
        color=color_map[col],
        marker="o",
        linestyle="None",
        markersize=8,
        label=col,
    )
    for col in fba_cols
]
legend1 = ax.legend(
    handles=color_legend_elements,
    title="FBA Oxygen Level",
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
)

# For shapes (Experimental conditions)
shape_legend_elements = [
    mlines.Line2D(
        [0],
        [0],
        color="gray",
        marker=shape_map[cond],
        linestyle="None",
        markersize=8,
        label=cond,
    )
    for cond in conditions
]
legend2 = ax.legend(
    handles=shape_legend_elements,
    title="Carbon Source(s)",
    bbox_to_anchor=(1.05, 0),
    loc="lower left",
)

# Add the first legend back to the plot
ax.add_artist(legend1)

# Add legend and title
plt.title("Scatter Plot: Experimental vs FBA")

# Make axes, tick, and axis labels gray
plt.gca().spines["top"].set_color("gray")
plt.gca().spines["right"].set_color("gray")
plt.gca().spines["left"].set_color("gray")
plt.gca().spines["bottom"].set_color("gray")
plt.gca().tick_params(axis="x", colors="gray")
plt.gca().tick_params(axis="y", colors="gray")
plt.xlabel("Experimental BGE", color="gray")
plt.ylabel("FBA Predicted BGE", color="gray")

# Save the plot
plt.savefig(os.path.join(OUT_DIR, "exp_vs_fba.png"), dpi=300, bbox_inches="tight")
