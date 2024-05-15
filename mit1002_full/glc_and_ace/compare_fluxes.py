import os
import pickle
import sys

import cobra
import pandas as pd
import plotly.graph_objects as go

# Import the plot styles (has global variables for colors)
sys.path.append(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)
from plot_styles import DARK_BLUE

# Set the output directory (where the results.pkl file will be saved)
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Set the path to the model file
MODEL_DIR = "../../GEM-repos/mit1002-model"

# Set a folder for the plots
OUTPUT_FOLDER = os.path.join(OUT_DIR, "plots")


def main():
    # Check if the output folder exists, if not, create it
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Load the results from the COBRA simulations
    with open(os.path.join(OUT_DIR, "results.pkl"), "rb") as f:
        cobra_results = pickle.load(f)

    glc_only_fba = cobra_results["glc_medium_real_o2_fba"]
    ace_only_fba = cobra_results["ace_medium_real_o2_fba"]
    glc_heavy_mix_fba = cobra_results["glc_heavy_mix_medium_real_o2_fba"]
    ace_heavy_mix_fba = cobra_results["ace_heavy_mix_medium_real_o2_fba"]

    # Load in the ALT model using COBRApy
    model = cobra.io.read_sbml_model(os.path.join(MODEL_DIR, "model.xml"))

    # Scatterplot comparing the fluxes on glucose only and acetate only
    plot_scatter_flux_comparison(
        model,
        glc_only_fba.fluxes + ace_only_fba.fluxes,
        glc_heavy_mix_fba.fluxes,
        "Glucose Only + Acetate Only",
        "8mM Glucose & 4mM Acetate Mixture",
    )
    plot_scatter_flux_comparison(
        model,
        glc_only_fba.fluxes + ace_only_fba.fluxes,
        ace_heavy_mix_fba.fluxes,
        "Glucose Only + Acetate Only",
        "4mM Glucose & 8mM Acetate Mixture",
    )

    # Scatterplot comparing the sum of the fluxes on glucose only and acetate
    # only with the fluxes on the two mixtures

    # Table of the reactions with the biggest differences in flux between the two solutions
    db = make_table_flux_comparison(
        model, glc_only_fba.fluxes, ace_only_fba.fluxes, "Glucose Only", "Acetate Only"
    )
    db.to_csv(os.path.join(OUTPUT_FOLDER, "glc_vs_ace_flux_comparison.csv"))


# Make a plotly plot that plots a scatterplot comparing the fluxes of two solutions,
# and shows the reaction information when hovering over the points
def plot_scatter_flux_comparison(
    model: cobra.Model,
    sol1_fluxes: dict,
    sol2_fluxes: dict,
    sol1_title: str,
    sol2_title: str,
):
    """Create a plotly scatter plot comparing the fluxes of two solutions

    Args:
    - model: cobra.Model object
    - sol1_fluxes: dict, fluxes of the first solution
    - sol2_fluxes: dict, fluxes of the second solution
    - sol1_title: str, title of the first solution
    - sol2_title: str, title of the second solution

    Returns:
    - None
    """
    # Get the reactions that are in both solutions
    shared_rxns = set(sol1_fluxes.keys()) & set(sol2_fluxes.keys())
    # Give a warning for reactions that are in one solution but not the other
    for rxn in set(sol1_fluxes.keys()) - shared_rxns:
        print(f"Reaction {rxn} is in {sol1_title} but not in {sol2_title}")

    # Create a scatter plot of the fluxes
    fig = go.Figure()
    for rxn in shared_rxns:
        # When hovering over a point, show the reaction ID, name, and reaction
        # from the model
        # Make all points large and the same color (blue, defined by a hex code)
        fig.add_trace(
            go.Scatter(
                x=[sol1_fluxes[rxn]],
                y=[sol2_fluxes[rxn]],
                mode="markers",
                name=rxn,
                marker=dict(size=10, color=DARK_BLUE),
                text=[f"{rxn}: {model.reactions.get_by_id(rxn).name}"],
            )
        )
    fig.update_layout(
        title=f"Fluxes of {sol1_title} vs {sol2_title}",
        xaxis_title=sol1_title,
        yaxis_title=sol2_title,
    )
    # Hide the legend
    fig.update_layout(showlegend=False)

    # Save the plot as a html file
    plot_file = os.path.join(
        OUTPUT_FOLDER,
        f'{sol1_title.replace(" ", "_").lower()}_vs_{sol2_title.replace(" ", "_").lower()}.html',
    )
    fig.write_html(plot_file)


def make_table_flux_comparison(
    model: cobra.Model,
    sol1_fluxes: dict,
    sol2_fluxes: dict,
    sol1_title: str,
    sol2_title: str,
):
    """Create a table of the reactions with the biggest differences in flux between two solutions

    Args:
    - model: cobra.Model object
    - sol1_fluxes: dict, fluxes of the first solution
    - sol2_fluxes: dict, fluxes of the second solution
    - sol1_title: str, title of the first solution
    - sol2_title: str, title of the second solution

    Returns:
    - DataFrame, table of the reactions with the biggest differences in flux
    """
    # Get the reactions that are in both solutions
    shared_rxns = set(sol1_fluxes.keys()) & set(sol2_fluxes.keys())
    # Calculate the difference in flux between the two solutions
    flux_diffs = {rxn: abs(sol1_fluxes[rxn] - sol2_fluxes[rxn]) for rxn in shared_rxns}
    # Sort the reactions by the difference in flux
    sorted_rxns = sorted(flux_diffs, key=flux_diffs.get, reverse=True)
    # Create a table of the reactions with their fluxes in each and the difference
    table_data = []
    for rxn in sorted_rxns:
        table_data.append(
            {
                "Reaction ID": rxn,
                "Reaction Name": model.reactions.get_by_id(rxn).name,
                f"Flux in {sol1_title}": sol1_fluxes[rxn],
                f"Flux in {sol2_title}": sol2_fluxes[rxn],
                "Difference in Flux": flux_diffs[rxn],
            }
        )
    return pd.DataFrame(table_data)


if __name__ == "__main__":
    main()
