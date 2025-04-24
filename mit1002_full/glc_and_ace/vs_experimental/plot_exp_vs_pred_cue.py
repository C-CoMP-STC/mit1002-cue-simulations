import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import linregress

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
    "Glucose Only": [0.78],
    "Acetate Only": [0.66],
    "Glucose Heavy Mix": [0.75],
    "Acetate Heavy Mix (Early)": [0.74],
    "Acetate Heavy Mix (Late)": [0.66],
}
# Convert data to a pandas DataFrame
bge_df = pd.DataFrame(data)
# Set the index of the row to be a helpful name
bge_df.index = ["Experimental"]

# Load the FBA-predicted results
fba_data = pd.read_csv(
    os.path.join(os.path.dirname(FILE_DIR), "results.csv"), index_col=0, header=0
)

# Add the FBA-predicted results to the dataframe
bge_df.loc["FBA (O2=5)"] = {
    "Glucose Only": fba_data.loc["Glucose Only(O2 = 5)_fba", "bge"],
    "Acetate Only": fba_data.loc["Acetate Only(O2 = 5)_fba", "bge"],
    "Glucose Heavy Mix": fba_data.loc["Glucose Heavy Mix(O2 = 5)_fba", "bge"],
    "Acetate Heavy Mix (Early)": fba_data.loc["Acetate Heavy Mix(O2 = 5)_fba", "bge"],
}
bge_df.loc["FBA (O2=10)"] = {
    "Glucose Only": fba_data.loc["Glucose Only(O2 = 10)_fba", "bge"],
    "Acetate Only": fba_data.loc["Acetate Only(O2 = 10)_fba", "bge"],
    "Glucose Heavy Mix": fba_data.loc["Glucose Heavy Mix(O2 = 10)_fba", "bge"],
    "Acetate Heavy Mix (Early)": fba_data.loc["Acetate Heavy Mix(O2 = 10)_fba", "bge"],
}
bge_df.loc["FBA (O2=20)"] = {
    "Glucose Only": fba_data.loc["Glucose Only(O2 = 20)_fba", "bge"],
    "Acetate Only": fba_data.loc["Acetate Only(O2 = 20)_fba", "bge"],
    "Glucose Heavy Mix": fba_data.loc["Glucose Heavy Mix(O2 = 20)_fba", "bge"],
    "Acetate Heavy Mix (Early)": fba_data.loc["Acetate Heavy Mix(O2 = 20)_fba", "bge"],
}
bge_df.loc["FBA (O2=30)"] = {
    "Glucose Only": fba_data.loc["Glucose Only(O2 = 30)_fba", "bge"],
    "Acetate Only": fba_data.loc["Acetate Only(O2 = 30)_fba", "bge"],
    "Glucose Heavy Mix": fba_data.loc["Glucose Heavy Mix(O2 = 30)_fba", "bge"],
    "Acetate Heavy Mix (Early)": fba_data.loc["Acetate Heavy Mix(O2 = 30)_fba", "bge"],
}
bge_df.loc["FBA (O2=1000)"] = {
    "Glucose Only": fba_data.loc["Glucose Only(O2 = 1000)_fba", "bge"],
    "Acetate Only": fba_data.loc["Acetate Only(O2 = 1000)_fba", "bge"],
    "Glucose Heavy Mix": fba_data.loc["Glucose Heavy Mix(O2 = 1000)_fba", "bge"],
    "Acetate Heavy Mix (Early)": fba_data.loc[
        "Acetate Heavy Mix(O2 = 1000)_fba", "bge"
    ],
    "Acetate Heavy Mix (Late)": fba_data.loc["Acetate Heavy Mix(O2 = 1000)_fba", "bge"],
}

# Order the columns in increasing order (for the Experimental data)
bge_df_sorted = bge_df[bge_df.loc["Experimental"].sort_values().index]

# Plot the predicted vs experimental
# Transpose the DataFrame to make rows into columns for easier plotting
bge_df_transposed = bge_df_sorted.T

# Set the figure size
plt.figure(figsize=(4, 4))

# Create a scatter plot of the two rows for one condition (O2=1000)
plt.scatter(
    bge_df_transposed["Experimental"],
    bge_df_transposed["FBA (O2=1000)"],
    label="Model v2 (O2=1000)",
    c="#60B1BE"
)

# Perform linear regression to get the slope, intercept, and R-value
slope, intercept, r_value, p_value, std_err = linregress(
    bge_df_transposed["Experimental"], bge_df_transposed["FBA (O2=1000)"]
)

# Calculate the line of best fit
line_of_best_fit = slope * bge_df_transposed["Experimental"] + intercept

# Add the line of best fit to the plot
plt.plot(
    bge_df_transposed["Experimental"],
    line_of_best_fit,
    color="#024064",
    linestyle="-",
    label=f"Best Fit (R={r_value:.2f})",
)

# Add legend and title
plt.title("Scatter Plot: Experimental vs FBA")
plt.legend()

# Make axes, tick, and axis labels gray
plt.gca().spines["top"].set_color("gray")
plt.gca().spines["right"].set_color("gray")
plt.gca().spines["left"].set_color("gray")
plt.gca().spines["bottom"].set_color("gray")
plt.gca().tick_params(axis="x", colors="gray")
plt.gca().tick_params(axis="y", colors="gray")
plt.xlabel("Experimental", color="gray")
plt.ylabel("FBA", color="gray")

# Save the plot
plt.savefig(os.path.join(OUT_DIR, "exp_vs_fba.png"), dpi=300)
