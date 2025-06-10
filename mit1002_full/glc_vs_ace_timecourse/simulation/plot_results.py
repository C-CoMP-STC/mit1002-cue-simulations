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

        # Find the first cycle with the maximum biomass
        max_biomass = experiment.total_biomass["iHS4156"].max()
        final_cycle = experiment.total_biomass.loc[
            experiment.total_biomass["iHS4156"] == max_biomass, "cycle"
        ].values[0]

        # Plot the results
        ax = experiment.total_biomass.plot(x="cycle")
        ax.set_ylabel("Biomass (g)")
        ax.set_title(f"MIT1002 Growth on {c_source_name}")
        ax.figure.savefig(os.path.join(PLOTS_DIR, f"{c_source_name}_biomass.png"))

        # Cut off the x-axis to only show up to the final cycle
        ax.set_xlim(0, final_cycle)
        # Add the final cycle as text on the plot
        ax.text(
            final_cycle,
            max_biomass,
            f"Final cycle: {final_cycle}",
            horizontalalignment="right",
            verticalalignment="bottom",
        )
        ax.figure.savefig(
            os.path.join(PLOTS_DIR, f"{c_source_name}_biomass_cutoff.png")
        )

        # Change the y-axis to be in log scale
        ax.set_yscale("log")
        ax.figure.savefig(os.path.join(PLOTS_DIR, f"{c_source_name}_biomass_log.png"))

        # Plot the biomass reaction flux
        ax = experiment.fluxes_by_species["iHS4156"].plot(
            x="cycle", y="bio1_biomass", title=f"Biomass Flux on {c_source_name}"
        )
        ax.set_ylabel("Flux (mmol/gDW/h)")
        ax.figure.savefig(os.path.join(PLOTS_DIR, f"{c_source_name}_growth_rate.png"))

        # Cut off the x-axis to only show up to the final cycle
        ax.set_xlim(0, final_cycle)
        # Add the final cycle as text on the plot
        ax.text(
            final_cycle,
            experiment.fluxes_by_species["iHS4156"]
            .loc[
                experiment.fluxes_by_species["iHS4156"]["cycle"] == final_cycle,
                "bio1_biomass",
            ]
            .values[0],
            f"Final cycle: {final_cycle}",
            horizontalalignment="right",
            verticalalignment="bottom",
        )
        ax.figure.savefig(
            os.path.join(PLOTS_DIR, f"{c_source_name}_growth_rate_cutoff.png")
        )
