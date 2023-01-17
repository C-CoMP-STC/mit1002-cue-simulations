import cometspy as c
import cobra
import pickle

# This script is for setting up, running, and saving the results from a
# COMETS simulation
# The simulation is for the CarveMe Alteromoas MIT 1002, in a well-mixed
# environment with glucose and oxygen in one simulation, and acetate and
# oxygen in another

# Want to pull a specifc version of the model from the repository
# But for now just save the model here too...
alt_cobra = cobra.io.read_sbml_model('alt_nutrients/model.xml')

########################################################################
# Glucose and Oxygen simulation
########################################################################
# Create empty 1x1 layout
test_tube = c.layout()

# Add 11mM glucose
test_tube.set_specific_metabolite('glc__D_e', 0.011)

# Add plenty of oxygen
test_tube.set_specific_metabolite('o2_e', 1000)

# Add the rest of nutrients unlimited (ammonia, phosphate, water and protons)
test_tube.set_specific_metabolite('nh4_e',1000);
test_tube.set_specific_metabolite('pi_e',1000);
test_tube.set_specific_metabolite('h2o_e',1000);
test_tube.set_specific_metabolite('h_e',1000);

# use the loaded model to build a comets model
alt = c.model(alt_cobra)

# Remove the bounds from glucose import (will be set dynamically by COMETS)
alt.change_bounds('EX_glc__D_e', -1000, 1000)
alt.change_bounds('EX_ac_e', -1000, 1000)

# Set the model's initial biomass
alt.initial_pop = [0, 0, 5e-6]

# Add it to the test_tube
test_tube.add_model(alt)

# Set the parameters that are different from the default
sim_params = c.params()

sim_params.set_param('defaultVmax', 18.5)
sim_params.set_param('defaultKm', 0.000015)
sim_params.set_param('maxCycles', 1)
sim_params.set_param('timeStep', 0.01)
sim_params.set_param('spaceWidth', 1)
sim_params.set_param('maxSpaceBiomass', 10)
sim_params.set_param('minSpaceBiomass', 1e-11)
sim_params.set_param('writeMediaLog', True)
sim_params.set_param('writeFluxLog', True)
sim_params.set_param('FluxLogRate', 1)

# Create the experiment
experiment_glucose = c.comets(test_tube, sim_params)

# Run the simulation
experiment_glucose.run()

########################################################################
# Acetate and Oxygen simulation
########################################################################
# Create empty 1x1 layout
test_tube = c.layout()

# Add 11mM glucose
test_tube.set_specific_metabolite('ac_e', 0.011)

# Add plenty of oxygen
test_tube.set_specific_metabolite('o2_e', 1000)

# Add the rest of nutrients unlimited (ammonia, phosphate, water and protons)
test_tube.set_specific_metabolite('nh4_e',1000);
test_tube.set_specific_metabolite('pi_e',1000);
test_tube.set_specific_metabolite('h2o_e',1000);
test_tube.set_specific_metabolite('h_e',1000);

# use the loaded model to build a comets model
alt = c.model(alt_cobra)

# Remove the bounds from glucose import (will be set dynamically by COMETS)
alt.change_bounds('EX_ac_e', -1000, 1000)

# Set the model's initial biomass
alt.initial_pop = [0, 0, 5e-6]

# Add it to the test_tube
test_tube.add_model(alt)

# Set the parameters that are different from the default
sim_params = c.params()

sim_params.set_param('defaultVmax', 18.5)
sim_params.set_param('defaultKm', 0.000015)
sim_params.set_param('maxCycles', 1)
sim_params.set_param('timeStep', 0.01)
sim_params.set_param('spaceWidth', 1)
sim_params.set_param('maxSpaceBiomass', 10)
sim_params.set_param('minSpaceBiomass', 1e-11)
sim_params.set_param('writeMediaLog', True)
sim_params.set_param('writeFluxLog', True)
sim_params.set_param('FluxLogRate', 1)

# Create the experiment
experiment_acetate = c.comets(test_tube, sim_params)

# Run the simulation
experiment_acetate.run()

########################################################################
# Save the results
########################################################################
with open('alt_nutrients/results.pkl', 'wb') as f:
    pickle.dump([experiment_glucose, experiment_acetate], f)
