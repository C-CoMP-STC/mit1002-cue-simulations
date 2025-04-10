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
    "Heavy Glucose Mix": [0.71],
    "Heavy Acetate Mix": [0.62],
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
gge_df.loc["FBA"] = {
    "Glucose Only": fba_data.loc["glc_medium_real_o2_fba", "gge"],
    "Acetate Only": fba_data.loc["ace_medium_real_o2_fba", "gge"],
    "Heavy Glucose Mix": fba_data.loc["glc_heavy_mix_medium_real_o2_fba", "gge"],
    "Heavy Acetate Mix": fba_data.loc["ace_heavy_mix_medium_real_o2_fba", "gge"],
}

# Plot the predicted vs experimental
# Transpose the DataFrame to make rows into columns for easier plotting
gge_df_transposed = gge_df.T

# Create a scatter plot of the two rows
plt.scatter(gge_df_transposed["Experimental"], gge_df_transposed["FBA"], label="Experimental vs FBA")

# Add a line of best fit
# Calculate the coefficients for the line of best fit
m, b = np.polyfit(gge_df_transposed["Experimental"], gge_df_transposed["FBA"], 1)
# Create the line of best fit
x_fit = np.array([0, 1])
y_fit = m * x_fit + b
# Plot the line of best fit
plt.plot(x_fit, y_fit, color="blue", label="Line of Best Fit")

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
plt.savefig(os.path.join(FILE_DIR, "exp_vs_fba.png"), dpi=300)
