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

        # Find the cycles where the glucose exchange flux in negative
        glucose_exchange_flux = experiment.fluxes_by_species[model_id]["EX_cpd00027_e0"]
        glucose_cycles = glucose_exchange_flux[glucose_exchange_flux < 0].index

        # Find the cycles where the acetate exchange flux is negative
        acetate_exchange_flux = experiment.fluxes_by_species[model_id]["EX_cpd00029_e0"]
        acetate_cycles = acetate_exchange_flux[acetate_exchange_flux < 0].index

        # Plot the biomass over time
        ax = experiment.total_biomass.plot(x="cycle")
        # Shade in the cycles where glucose is being consumed
        for cycle in glucose_cycles:
            ax.axvspan(cycle - 0.5, cycle + 0.5, color="blue", alpha=0.1)
        # Shade in the cycles where acetate is being consumed
        for cycle in acetate_cycles:
            ax.axvspan(cycle - 0.5, cycle + 0.5, color="orange", alpha=0.1)
        # Style the plot
        ax.set_ylabel("Biomass (g)")
        ax.set_title(f"MIT1002 Growth on {c_source_name}")
        ax.figure.savefig(os.path.join(PLOTS_DIR, f"{c_source_name}_biomass.png"))

        # Plot the growth rate over time
        ax = experiment.fluxes_by_species[model_id].plot(x="cycle", y=biomass_id)
        # Shade in the cycles where glucose is being consumed
        for cycle in glucose_cycles:
            ax.axvspan(cycle - 0.5, cycle + 0.5, color="blue", alpha=0.1)
        # Shade in the cycles where acetate is being consumed
        for cycle in acetate_cycles:
            ax.axvspan(cycle - 0.5, cycle + 0.5, color="orange", alpha=0.1)
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
        ax.figure.savefig(
            os.path.join(PLOTS_DIR, f"{c_source_name}_exchange_fluxes.png")
        )
