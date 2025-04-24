# This script is for setting up, running, and saving the results from a
# COMETS simulation
# The simulation is for the Alteromonas macleodii MIT1002 core model,
# in a well-mixed environment with glucose and oxygen

import cometspy as c
import cobra
import pickle
import os

# Set the output directory (where the results.pkl file will be saved)
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Create empty 1x1 layout
test_tube = c.layout()

# Set glucose os 0.002, everything else as 1000
# I chose 0.002 because that is equivalent to what Zac used in the lab
# He used 12 mmol/L carbon, and I am modeling 1 mL of media, so 12 mmol/L
# * (0.1L/100 mL) = 0.012 mmol/mL carbon. And glucose has 6 carbons, so
# 0.012 mmol/mL / 6 carbons = 0.002 mmol/mL glucose
test_tube.set_specific_metabolite('cpd00027_e0', 0.002)  # D-Glucose_e0, in mmol

# Add a limiting amount of oxygen- not sure the exact amount I should use
test_tube.set_specific_metabolite('cpd00007_e0', 2)  # O2_e0

# Add the of the nutrients I found in the find_minimal_media notebook
test_tube.set_specific_metabolite('cpd00058_e0', 1000)  # Cu2+_e0
test_tube.set_specific_metabolite('cpd00971_e0', 1000)  # Na+_e0
test_tube.set_specific_metabolite('cpd00063_e0', 1000)  # Ca2+_e0
test_tube.set_specific_metabolite('cpd00048_e0', 1000)  # Sulfate_e0
test_tube.set_specific_metabolite('cpd10516_e0', 1000)  # fe3_e0
test_tube.set_specific_metabolite('cpd00254_e0', 1000)  # Mg_e0
test_tube.set_specific_metabolite('cpd00009_e0', 1000)  # Phosphate_e0
test_tube.set_specific_metabolite('cpd00205_e0', 1000)  # K+_e0
test_tube.set_specific_metabolite('cpd00013_e0', 1000)  # NH3_e0
test_tube.set_specific_metabolite('cpd00099_e0', 1000)  # Cl-_e0
test_tube.set_specific_metabolite('cpd00030_e0', 1000)  # Mn2+_e0
test_tube.set_specific_metabolite('cpd00075_e0', 1000)  # Nitrite_e0
test_tube.set_specific_metabolite('cpd00001_e0', 1000)  # H2O_e0
test_tube.set_specific_metabolite('cpd00635_e0', 1000)  # Cbl_e0
test_tube.set_specific_metabolite('cpd00034_e0', 1000)  # Zn2+_e0
test_tube.set_specific_metabolite('cpd00149_e0', 1000)  # Co2+_e0

# Load in the ALT model using COBRApy
alt_cobra = cobra.io.read_sbml_model("../../GEM-repos/GEM-mit1002/model.xml")

# use the loaded model to build a comets model
alt = c.model(alt_cobra)

# Convert the objective style so that the model uses pFBA
alt.obj_style = 'MAX_OBJECTIVE_MIN_TOTAL'

# remove the bounds from glucose import (will be set dynamically by COMETS
alt.change_bounds('EX_cpd00027_e0', -1000, 1000)
alt.change_bounds('EX_cpd00029_e0', -1000, 1000)

# set the model's initial biomass
# Zac's plot only had OD, so I don't know what the initial biomass should be
alt.initial_pop = [0, 0, 5e-6]

# add it to the test_tube
test_tube.add_model(alt)

# Set the parameters that are different from the default
sim_params = c.params()

sim_params.set_param('defaultVmax', 18.5)
# Set a different Vmax for just the oxygen exchange reaction
alt.change_vmax('EX_cpd00007_e0', 10)
sim_params.set_param('defaultKm', 0.000015)
sim_params.set_param('maxCycles', 2500)  # To get a total of 25 hours
sim_params.set_param('timeStep', 0.01)  # In hours
sim_params.set_param('spaceWidth', 1)
sim_params.set_param('maxSpaceBiomass', 10)
sim_params.set_param('minSpaceBiomass', 1e-11)
sim_params.set_param('writeMediaLog', True)
sim_params.set_param('writeFluxLog', True)
sim_params.set_param('FluxLogRate', 1)
sim_params.set_param('MediaLogRate', 1)

# Create the experiment
experiment = c.comets(test_tube, sim_params)

# Run the simulation
experiment.run()

# Save the results
with open(os.path.join(OUT_DIR, 'results.pkl'), 'wb') as f:
    pickle.dump(experiment, f)
