import os
import pickle

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(FILE_DIR, "results")
PLOTS_DIR = os.path.join(FILE_DIR, "plots")

# Create the results and plots directories if they do not exist
if not os.path.exists(PLOTS_DIR):
    os.makedirs(PLOTS_DIR)

# For every pickle file in the results directory
for filename in os.listdir(RESULTS_DIR):
    if filename.endswith(".pkl"):
        # Load the COMETS results
        with open(os.path.join(RESULTS_DIR, filename), "rb") as f:
            experiment = pickle.load(f)

        # Take "_results.pkl" off the end of the filename to get the experiment name
        c_source_name = filename.split("_results.pkl")[0]

        # Plot the results
        ax = experiment.total_biomass.plot(x="cycle")
        ax.set_ylabel("Biomass (g)")
        ax.set_title(f"MIT1002 Growth on {c_source_name}")
        ax.figure.savefig(os.path.join(PLOTS_DIR, f"{c_source_name}_biomass.png"))
