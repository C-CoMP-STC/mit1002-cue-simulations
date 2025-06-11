import os
import pickle

import pandas as pd

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(FILE_DIR, "results")

model_id = "iHS4156"  # Model ID for the COMETS model
biomass_id = "bio1_biomass"  # Biomass reaction ID in the model
co2_id = "cpd00011_e0"  # CO2 (extracellular) metabolite ID in the model

# Numbers to convert g of biomass to mmol of carbon
biomass_c_by_weight = 0.5  # Biomass is 50% carbon by weight
c_weight = 12.01  # g/mol


def main():
    # Make a dictionary to hold the BGE results
    bge_results = {}

    # For every pickle file in the results directory
    for filename in os.listdir(RESULTS_DIR):
        if filename.endswith("pfba_results.pkl"):
            # Load the COMETS results
            with open(os.path.join(RESULTS_DIR, filename), "rb") as f:
                experiment = pickle.load(f)

            # Take "_results.pkl" off the end of the filename to get the experiment name
            c_source_name = filename.split("_results.pkl")[0]

            # Find the cycles where the glucose exchange flux in negative
            glucose_exchange_flux = experiment.fluxes_by_species[model_id][
                "EX_cpd00027_e0"
            ]
            glucose_cycles = glucose_exchange_flux[glucose_exchange_flux < 0].index

            # Find the cycles where the acetate exchange flux is negative
            acetate_exchange_flux = experiment.fluxes_by_species[model_id][
                "EX_cpd00029_e0"
            ]
            acetate_cycles = acetate_exchange_flux[acetate_exchange_flux < 0].index

            # Calculate the BGE for glucose and acetate
            if glucose_cycles.any():
                bge_glucose = bge_across_cycle(experiment, glucose_cycles)
            else:
                bge_glucose = None
            if acetate_cycles.any():
                bge_acetate = bge_across_cycle(experiment, acetate_cycles)
            else:
                bge_acetate = None
            # Store the BGE results
            bge_results[c_source_name] = {
                "bge_glucose": bge_glucose,
                "bge_acetate": bge_acetate,
            }

    # Convert the BGE results to a DataFrame
    bge_df = (
        pd.DataFrame.from_dict(bge_results, orient="index")
        .reset_index()
        .rename(columns={"index": "c_source"})
    )
    # Save the BGE results to a CSV file
    bge_df.to_csv(os.path.join(RESULTS_DIR, "bge_results.csv"), index=False)


def bge_across_cycle(experiment, cycles):
    """Calculate the BGE across a set of cycles."""
    # Get the starting biomass in grams
    starting_biomass_g = experiment.total_biomass.loc[cycles[0]][model_id]
    # Convert to mmol of carbon
    starting_biomass_mmol = starting_biomass_g * biomass_c_by_weight / c_weight * 1000

    # Get the ending biomass in grams
    ending_biomass_g = experiment.total_biomass.loc[cycles[-1]][model_id]
    # Convert to mmol of carbon
    ending_biomass_mmol = ending_biomass_g * biomass_c_by_weight / c_weight * 1000

    # Get the starting CO2
    co2_df = experiment.media[
        (experiment.media["metabolite"] == co2_id)
        & (experiment.media["cycle"] == cycles[0])
    ]
    if co2_df.empty:
        starting_co2 = 0
    else:
        starting_co2 = co2_df["conc_mmol"].values[0]

    # Get the ending CO2
    co2_df = experiment.media[
        (experiment.media["metabolite"] == co2_id)
        & (experiment.media["cycle"] == cycles[-1])
    ]
    if co2_df.empty:
        ending_co2 = 0
    else:
        ending_co2 = co2_df["conc_mmol"].values[0]

    # Calculate the deltas
    delta_biomass = ending_biomass_mmol - starting_biomass_mmol
    delta_co2 = ending_co2 - starting_co2

    # Calculate the BGE
    bge = delta_biomass / (delta_biomass + delta_co2)
    return bge


if __name__ == "__main__":
    main()
