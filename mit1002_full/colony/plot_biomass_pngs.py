import matplotlib.pyplot as plt
from matplotlib import cm
import os
import pickle

# Set the output directory (where the results.pkl file will be saved)
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

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
png_output_folder = os.path.join(output_folder, 'biomass_by_cycle')
if not os.path.exists(png_output_folder):
    os.makedirs(png_output_folder)

# Get the list of cycles
cycle_list = set(experiment.biomass['cycle'].tolist())

# Get the maximum biomass in a single grid cell
max_biomass = experiment.biomass['biomass'].max()

# Make a color map
# Want 0 to be black, and for biomass to be neon green
cmap = cm.get_cmap('Greens')

# For every cycle, generate and save an image of the biomass
for cycle in cycle_list:
    # Make a numpy array with the biomass of each cell at a specified cycle
    im = experiment.get_biomass_image('', cycle)
    # Plot
    fig, ax = plt.subplots(figsize=(3.1, 3.1))
    plt.imshow(im, cmap=cmap)
    # Style
    plt.axis('off')
    plt.title('Cycle {}'.format(cycle))
    # Set the colorbar limits
    plt.clim(0, max_biomass)
    # Show colorbar
    plt.colorbar()
    # Save
    plt.savefig(os.path.join(png_output_folder,
                             'biomass_{}.png'.format(cycle)))
