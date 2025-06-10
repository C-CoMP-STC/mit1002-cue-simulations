import os
import pickle

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(FILE_DIR, "results")
PLOTS_DIR = os.path.join(FILE_DIR, "plots")

n_sigfigs = 6  # Number of digits to round the growth rate to

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

        # Round the growth rate to n_sigfigs
        growth_rate_per_cycle = experiment.fluxes_by_species["iHS4156"][
            "bio1_biomass"
        ].round(n_sigfigs)

        # Find the most common growth rate that is not zero
        growth_rate_per_cycle = growth_rate_per_cycle[growth_rate_per_cycle != 0]
        most_common_growth_rate = growth_rate_per_cycle.value_counts().idxmax()

        # Find all cycles with the most common growth rate
        phase_cycles = growth_rate_per_cycle[
            growth_rate_per_cycle == most_common_growth_rate
        ].index

        # Plot the biomass over time
        ax = experiment.total_biomass.plot(x="cycle")

        # Shade the regions of growth in the phase cycles
        for cycle in phase_cycles:
            ax.axvspan(cycle - 0.5, cycle + 0.5, color="green", alpha=0.3)

        # Style the plot
        ax.set_ylabel("Biomass (g)")
        ax.set_title(f"MIT1002 Growth on {c_source_name}")
        ax.figure.savefig(os.path.join(PLOTS_DIR, f"{c_source_name}_biomass.png"))

        # Save the list of phase cycles to a pickle file
        with open(
            os.path.join(RESULTS_DIR, f"{c_source_name}_phase_cycles.pkl"), "wb"
        ) as f:
            pickle.dump(phase_cycles, f)
