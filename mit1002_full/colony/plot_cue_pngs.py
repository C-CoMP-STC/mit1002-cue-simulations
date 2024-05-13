import matplotlib.pyplot as plt
import os
import pickle
import numpy as np
import cobra

# Import my own CUE functions
from gem2cue import (
    utils,  # Import the working version (works with the med4-hot1a3 conda env)
)

# Set the output directory (where the results.pkl file will be saved)
OUT_DIR = os.path.dirname(os.path.realpath(__file__))


# Main function for running the script
def main():
    # Set a folder for the plots
    # Assuming you are running from the root of the repository
    output_folder = os.path.join(OUT_DIR, 'plots')

    # Check if the folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the results
    with open(os.path.join(OUT_DIR, 'results.pkl'), 'rb') as f:
        experiment = pickle.load(f)

    # Make a folder for all of the individual plots that will go into the gif
    png_output_folder = os.path.join(output_folder, 'cue_by_cycle')
    if not os.path.exists(png_output_folder):
        os.makedirs(png_output_folder)

    # Load the model
    cobra_model = cobra.io.read_sbml_model("../../GEM-repos/mit1002-model/model.xml")

    # Get the exchange reactions for the E coli core model
    # Because this isn't dependent on the fluxes, I can do it out of the loop
    c_ex_rxns = utils.get_c_ex_rxns(cobra_model)

    # Get the list of cycles
    cycle_list = experiment.fluxes_by_species['']['cycle'].tolist()

    # For every cycle, generate and save an image of the biomass
    for cycle in cycle_list:
        # Make a numpy array with the biomass of each cell at a specified cycle
        im = get_cue_image(experiment, cycle, c_ex_rxns, species='')
        # Plot
        fig, ax = plt.subplots(figsize=(3.1, 3.1))
        plt.imshow(im)
        # Style
        plt.axis('off')
        plt.title('Cycle {}'.format(cycle))
        # Set the colorbar limits
        plt.clim(0, 1)
        # Show colorbar
        plt.colorbar()
        # Save
        plt.savefig(os.path.join(png_output_folder,
                                 'cue_{}.png'.format(cycle)))


def get_cue_image(experiment,
                  cycle: int,
                  c_ex_rxns: dict,
                  species: str = 'e_coli_core') -> np.array:
    """
    Get the image of the CUE at a specified cycle.

    Parameters
    ----------
    experiment: c.comets
        The experiment object.
    c_ex_rxns: dict
        The carbon exchange reactions for the model of interest
    cycle: int
        The cycle number.
    species: str
        The model ID for the species of interest.

    Returns
    -------
    np.array
        The image of the CUE.
    """
    # Get the fluxes for the species of interest
    fluxes = experiment.fluxes_by_species[species].copy()
    # Get the fluxes at a specified cycle
    fluxes = fluxes[fluxes['cycle'] == cycle]

    # Make a numpy array to hold the results
    im = np.zeros((experiment.layout.grid[0], experiment.layout.grid[1]))

    # Loop through all of the grid cells and calculate the CUE
    for index, row in fluxes.iterrows():
        uptake_fluxes, excretion_fluxes = utils.comets_atom_fluxes(row,
                                                                   c_ex_rxns)
        im[int(row['x']-1),
           int(row['y']-1)] = utils.calculate_cue(uptake_fluxes,
                                                  excretion_fluxes)
    # Return the numpy array
    return im


if __name__ == '__main__':
    main()
