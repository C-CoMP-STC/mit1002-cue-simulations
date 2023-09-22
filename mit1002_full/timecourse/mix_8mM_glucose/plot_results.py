import cobra
import matplotlib.pyplot as plt
import os
import pickle
import pandas as pd

# Add the root folder to the python path so that I can import helpers.py
# TODO: Find a a way to do this that doens't use sys
import sys
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.realpath(__file__))))))
import helpers

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

# Find the cycle where biomass stops increasing
stationary_cycle = experiment.total_biomass.loc[
    experiment.total_biomass[''].idxmax()]['cycle']
max_cycle = stationary_cycle + 25

# Read in the model file
# Assuming you are running from the root of the repository
model_path = '../../GEM-repos/mit1002-model/model.xml'
alt_cobra = cobra.io.read_sbml_model(model_path)

# Get the ID of the biomass reaction
# TODO: Just get this from the model objective
biomass_rxn = 'bio1_biomass'

# Plot the biomass
helpers.plot_biomass(experiment, max_cycle, output_folder)

# Plot the fluxes
helpers.plot_fluxes(experiment, max_cycle, output_folder)

# Plot concentrations of metabolites in the media
helpers.plot_media(alt_cobra, experiment, max_cycle, output_folder)

# Plot all of the due definitions on one graph
helpers.plot_cue(alt_cobra, experiment, biomass_rxn, max_cycle, output_folder)

# Plot the carbon fates
# There's an error somewhere in this function
# helpers.plot_c_fates(alt_cobra, experiment, biomass_rxn, max_cycle, output_folder)
