import cometspy as c
import cobra
import pickle

# This script is for setting up, running, and saving the results from a
# COMETS simulation
# The simulation is for the Alteromonas macleodii MIT1002 core model,
# in a well-mixed environment with glucose and oxygen

# Create empty 1x1 layout
test_tube = c.layout()

# Set glucose os 0.011, everything else as 1000
test_tube.set_specific_metabolite('cpd00027_e0', 0.011) # D-Glucose_e0

# Add a limiting amount of oxygen- not sure the exact amount I should use
test_tube.set_specific_metabolite('cpd00007_e0', 20) # O2_e0

# Add the of the nutrients available from MBM as unlimited (phosphate, water and protons)
test_tube.set_specific_metabolite('cpd00009_e0',1000); # Phosphate_e0
test_tube.set_specific_metabolite('cpd00001_e0',1000); # H2O_e0
test_tube.set_specific_metabolite('cpd00067_e',1000); # H+_e0

# create the model using CobraPy functionality
alt_cobra = cobra.io.load_json_model("../../GEM-repos/mit1002-core-model/model.json")

# Change the objective of the COBRA model
# Not sure if that will cary over to the COMETS model, but trying it
alt_cobra.objective = "bio1_biomass"

# use the loaded model to build a comets model
alt = c.model(alt_cobra)

# remove the bounds from glucose import (will be set dynamically by COMETS)
alt.change_bounds('EX_cpd00027_e0', -1000, 1000)
alt.change_bounds('EX_cpd00029_e0', -1000, 1000)

# set the model's initial biomass
alt.initial_pop = [0, 0, 5e-6]

# add it to the test_tube
test_tube.add_model(alt)

# Set the parameters that are different from the default
sim_params = c.params()

sim_params.set_param('defaultVmax', 18.5)
sim_params.set_param('defaultKm', 0.000015)
sim_params.set_param('maxCycles', 600)
sim_params.set_param('timeStep', 0.01)
sim_params.set_param('spaceWidth', 1)
sim_params.set_param('maxSpaceBiomass', 10)
sim_params.set_param('minSpaceBiomass', 1e-11)
sim_params.set_param('writeMediaLog', True)
sim_params.set_param('writeFluxLog', True)
sim_params.set_param('FluxLogRate', 1)

# Create the experiment
experiment = c.comets(test_tube, sim_params)

# Run the simulation
experiment.run()

# Save the results
with open('mit1002_core/timecourse/results.pkl', 'wb') as f:
    pickle.dump(experiment, f)

