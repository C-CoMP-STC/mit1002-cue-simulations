import cometspy as c
import cobra
import pickle

# This script is for setting up, running, and saving the results from a
# COMETS simulation
# The simulation is for the E. coli core model, in a well-mixed
# environment with glucose and oxygen

# Create empty 3x3 layout
grid_size = 3
layout = c.layout()
layout.grid = [grid_size,grid_size]

# Add 11mM glucose
layout.set_specific_metabolite('glc__D_e', 0.011)

# Add plenty of oxygen
layout.set_specific_metabolite('o2_e', 1000)

# Add the rest of nutrients unlimited (ammonia, phosphate, water and protons)
layout.set_specific_metabolite('nh4_e',1000);
layout.set_specific_metabolite('pi_e',1000);
layout.set_specific_metabolite('h2o_e',1000);
layout.set_specific_metabolite('h_e',1000);

# create the model using CobraPy functionality
e_coli_cobra = cobra.io.load_model('textbook')

# use the loaded model to build a comets model
e_coli = c.model(e_coli_cobra)

# remove the bounds from glucose import (will be set dynamically by COMETS)
e_coli.change_bounds('EX_glc__D_e', -1000, 1000)
e_coli.change_bounds('EX_ac_e', -1000, 1000)

# set the model's initial biomass
e_coli.initial_pop = [0, 0, 5e-6]

# add it to the layout
layout.add_model(e_coli)

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
experiment = c.comets(layout, sim_params)

# Run the simulation
experiment.run()

# Save the results
with open('spatial_ecoli_core/results.pkl', 'wb') as f:
    pickle.dump(experiment, f)

