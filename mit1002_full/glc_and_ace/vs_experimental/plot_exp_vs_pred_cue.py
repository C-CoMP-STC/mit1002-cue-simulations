import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(FILE_DIR, "plots")

# If the output directory doesn't exist, create it
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

# Load the experimental results
# TODO: Recalculate the values myself from the raw data
# For now I'll just hardcode the values with what I had on the slide I
# presented at the all center meeting in Oct 2024, but I'm not entirely
# sure where those values came from/if they are correct
# Define the columns of the dataframe to be the different conditions
data = {
    "Glucose Only": [0.80],
    "Acetate Only": [0.49],
    "Glucose Heavy Mix": [0.71],
    "Acetate Heavy Mix": [0.62],
}
# Convert data to a pandas DataFrame
gge_df = pd.DataFrame(data)
# Set the index of the row to be a helpful name
gge_df.index = ["Experimental"]

# Load the FBA-predicted results
fba_data = pd.read_csv(
    os.path.join(os.path.dirname(FILE_DIR), "results.csv"), index_col=0, header=0
)

# Add the FBA-predicted results to the dataframe
gge_df.loc["FBA (O2=5)"] = {
    "Glucose Only": fba_data.loc["Glucose Only(O2 = 5)_fba", "gge"],
    "Acetate Only": fba_data.loc["Acetate Only(O2 = 5)_fba", "gge"],
    "Glucose Heavy Mix": fba_data.loc["Glucose Heavy Mix(O2 = 5)_fba", "gge"],
    "Acetate Heavy Mix": fba_data.loc["Acetate Heavy Mix(O2 = 5)_fba", "gge"],
}
gge_df.loc["FBA (O2=10)"] = {
    "Glucose Only": fba_data.loc["Glucose Only(O2 = 10)_fba", "gge"],
    "Acetate Only": fba_data.loc["Acetate Only(O2 = 10)_fba", "gge"],
    "Glucose Heavy Mix": fba_data.loc["Glucose Heavy Mix(O2 = 10)_fba", "gge"],
    "Acetate Heavy Mix": fba_data.loc["Acetate Heavy Mix(O2 = 10)_fba", "gge"],
}
gge_df.loc["FBA (O2=20)"] = {
    "Glucose Only": fba_data.loc["Glucose Only(O2 = 20)_fba", "gge"],
    "Acetate Only": fba_data.loc["Acetate Only(O2 = 20)_fba", "gge"],
    "Glucose Heavy Mix": fba_data.loc["Glucose Heavy Mix(O2 = 20)_fba", "gge"],
    "Acetate Heavy Mix": fba_data.loc["Acetate Heavy Mix(O2 = 20)_fba", "gge"],
}
gge_df.loc["FBA (O2=30)"] = {
    "Glucose Only": fba_data.loc["Glucose Only(O2 = 30)_fba", "gge"],
    "Acetate Only": fba_data.loc["Acetate Only(O2 = 30)_fba", "gge"],
    "Glucose Heavy Mix": fba_data.loc["Glucose Heavy Mix(O2 = 30)_fba", "gge"],
    "Acetate Heavy Mix": fba_data.loc["Acetate Heavy Mix(O2 = 30)_fba", "gge"],
}
gge_df.loc["FBA (O2=1000)"] = {
    "Glucose Only": fba_data.loc["Glucose Only(O2 = 1000)_fba", "gge"],
    "Acetate Only": fba_data.loc["Acetate Only(O2 = 1000)_fba", "gge"],
    "Glucose Heavy Mix": fba_data.loc["Glucose Heavy Mix(O2 = 1000)_fba", "gge"],
    "Acetate Heavy Mix": fba_data.loc["Acetate Heavy Mix(O2 = 1000)_fba", "gge"],
}

# Plot the predicted vs experimental
# Transpose the DataFrame to make rows into columns for easier plotting
gge_df_transposed = gge_df.T

# Create a scatter plot of the two rows for each of the conditions
plt.figure(figsize=(8, 8))
plt.scatter(gge_df_transposed["Experimental"],
            gge_df_transposed["FBA (O2=5)"],
            label="Model v2 (O2=5)")
plt.scatter(gge_df_transposed["Experimental"],
            gge_df_transposed["FBA (O2=10)"],
            label="Model v2 (O2=10)")
plt.scatter(gge_df_transposed["Experimental"],
            gge_df_transposed["FBA (O2=20)"],
            label="Model v2 (O2=20)")
plt.scatter(gge_df_transposed["Experimental"],
            gge_df_transposed["FBA (O2=30)"],
            label="Model v2 (O2=30)"
            )
# Not plotting the O2=1000 data because it is an exact overlap of O2=30

# Save what the bounds are for the axes
# Get the current axis
ax = plt.gca()
# Get the x-axis and y-axis limits
x_limits = ax.get_xlim()
y_limits = ax.get_ylim()

# # Add a line of best fit
# # Calculate the coefficients for the line of best fit
# m, b = np.polyfit(gge_df_transposed["Experimental"], gge_df_transposed["FBA"], 1)
# # Create the line of best fit
# x_fit = np.array([0, 1])
# y_fit = m * x_fit + b
# # Plot the line of best fit
# plt.plot(x_fit, y_fit, color="blue", label=None)

# Add a 1:1 line for reference
x = [0, 1]
y = [0, 1]
plt.plot(x, y, color="red", linestyle="--", label="1:1 Line")

# Reset the limits to be what they were before
# (the automatic settings from the scatter plots without the 1:1 line)
ax.set_xlim(x_limits)
ax.set_ylim(y_limits)

# Add labels and title
plt.xlabel("Experimental")
plt.ylabel("FBA")
plt.title("Scatter Plot: Experimental vs FBA")
plt.legend()

# Save the plot
plt.savefig(os.path.join(FILE_DIR, "exp_vs_fba.png"), dpi=300)
