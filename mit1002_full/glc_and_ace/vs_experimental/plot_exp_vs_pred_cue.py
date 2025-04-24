import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
    "Acetate Heavy Mix (Early)": fba_data.loc["Acetate Heavy Mix(O2 = 1000)_fba", "bge"],
}

# Order the columns in increasing order (for the Experimental data)
bge_df_sorted = bge_df[bge_df.loc["Experimental"].sort_values().index]

# Plot the predicted vs experimental
# Transpose the DataFrame to make rows into columns for easier plotting
bge_df_transposed = bge_df_sorted.T

# Create a scatter plot of the two rows for each of the conditions
plt.figure(figsize=(8, 8))
plt.plot(
    bge_df_transposed["Experimental"],
    bge_df_transposed["FBA (O2=5)"],
    marker="o",
    label="Model v2 (O2=5)",
)
plt.plot(
    bge_df_transposed["Experimental"],
    bge_df_transposed["FBA (O2=10)"],
    marker="o",
    label="Model v2 (O2=10)",
)
plt.plot(
    bge_df_transposed["Experimental"],
    bge_df_transposed["FBA (O2=20)"],
    marker="o",
    label="Model v2 (O2=20)",
)
plt.plot(
    bge_df_transposed["Experimental"],
    bge_df_transposed["FBA (O2=30)"],
    marker="o",
    label="Model v2 (O2=30)",
)
# Not plotting the O2=1000 data because it is an exact overlap of O2=30

# Save what the bounds are for the axes
# Get the current axis
ax = plt.gca()
# Get the x-axis and y-axis limits
x_limits = ax.get_xlim()
y_limits = ax.get_ylim()

# Add a 1:1 line for reference
x = [0, 1]
y = [0, 1]
plt.plot(x, y, color="red", linestyle="--", label="1:1 Line")

# Add labels and title
plt.xlabel("Experimental")
plt.ylabel("FBA")
plt.title("Scatter Plot: Experimental vs FBA")
plt.legend()

# Save the plot
plt.savefig(os.path.join(FILE_DIR, "exp_vs_fba_full.png"), dpi=300)


# Reset the limits to be what they were before
# (the automatic settings from the scatter plots without the 1:1 line)
ax.set_xlim(x_limits)
ax.set_ylim(y_limits)

# Save the plot
plt.savefig(os.path.join(FILE_DIR, "exp_vs_fba_zoom.png"), dpi=300)
