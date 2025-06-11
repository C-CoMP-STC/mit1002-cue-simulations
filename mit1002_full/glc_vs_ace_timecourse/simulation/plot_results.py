import os
import pickle

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(FILE_DIR, "results")
PLOTS_DIR = os.path.join(FILE_DIR, "plots")

model_id = "iHS4156"  # Model ID for the COMETS model
biomass_id = "bio1_biomass"  # Biomass reaction ID in the model

# Create the results and plots directories if they do not exist
if not os.path.exists(PLOTS_DIR):
    os.makedirs(PLOTS_DIR)

# For every pickle file in the results directory
for filename in os.listdir(RESULTS_DIR):
    if filename.endswith("pfba_results.pkl"):
        # Load the COMETS results
        with open(os.path.join(RESULTS_DIR, filename), "rb") as f:
            experiment = pickle.load(f)

        # Take "_results.pkl" off the end of the filename to get the experiment name
        c_source_name = filename.split("_results.pkl")[0]

        # Plot the biomass over time
        ax = experiment.total_biomass.plot(x="cycle")
        # Style the plot
        ax.set_ylabel("Biomass (g)")
        ax.set_title(f"MIT1002 Growth on {c_source_name}")
        ax.figure.savefig(os.path.join(PLOTS_DIR, f"{c_source_name}_biomass.png"))

        # Plot the growth rate over time
        ax = experiment.fluxes_by_species[model_id].plot(x="cycle", y=biomass_id)
        # Style the plot
        ax.set_ylabel("Growth Rate (1/h)")
        ax.set_title(f"MIT1002 Growth Rate on {c_source_name}")
        ax.figure.savefig(os.path.join(PLOTS_DIR, f"{c_source_name}_growth_rate.png"))

        # Plot the glucose and acetate exchange fluxes over time
        ax = experiment.fluxes_by_species[model_id].plot(
            x="cycle", y=["EX_cpd00027_e0", "EX_cpd00029_e0"]
        )
        # Style the plot
        ax.set_ylabel("Exchange Flux (mmol/gDW/h)")
        ax.set_title(f"MIT1002 Exchange Fluxes on {c_source_name}")
        ax.figure.savefig(os.path.join(PLOTS_DIR, f"{c_source_name}_exchange_fluxes.png"))
