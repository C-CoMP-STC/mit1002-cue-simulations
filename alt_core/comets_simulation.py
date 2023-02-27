import cometspy as c
import cobra
import pickle

# This script is for setting up, running, and saving the results from a
# COMETS simulation
# The simulation is for the Alteromonas macleodii MIT1002 core model,
# in a well-mixed environment with glucose and oxygen

# Create empty 1x1 layout
test_tube = c.layout()

# Set a rich media (copied from one of Ilija's notebooks)
test_tube.set_specific_metabolite('4abz_e',5.47e-8)
test_tube.set_specific_metabolite('btn_e',1.31e-8)
test_tube.set_specific_metabolite('ca2_e',1000)
test_tube.set_specific_metabolite('cl_e',1000)
test_tube.set_specific_metabolite('cobalt2_e',1000)
test_tube.set_specific_metabolite('cu2_e',1000)
test_tube.set_specific_metabolite('fe2_e',1000)
test_tube.set_specific_metabolite('fe3_e',1000) 
test_tube.set_specific_metabolite('fol_e',7.3e-9)
test_tube.set_specific_metabolite('glc__D_e',0.00075)
test_tube.set_specific_metabolite('k_e',1000)
test_tube.set_specific_metabolite('lac__D_e',0)
test_tube.set_specific_metabolite('lac__L_e',0)
test_tube.set_specific_metabolite('mg2_e',1000)
test_tube.set_specific_metabolite('mn2_e',1000)
test_tube.set_specific_metabolite('mobd_e',1000)
test_tube.set_specific_metabolite('na_e',1000)
#test_tube.set_specific_metabolite('nac_e',6.09e-8)
test_tube.set_specific_metabolite('nac_e',0.0002)
#test_tube.set_specific_metabolite('nh4_e',0.0007)
test_tube.set_specific_metabolite('nh4_e',0.00012)
test_tube.set_specific_metabolite('o2_e',1000)
test_tube.set_specific_metabolite('pi_e',0.000645)
#test_tube.set_specific_metabolite('pi_e',1000)
test_tube.set_specific_metabolite('pnto__R_e',3.4e-8)
#test_tube.set_specific_metabolite('pnto__R_e',0)
test_tube.set_specific_metabolite('pydxn_e',8.865e-9)
test_tube.set_specific_metabolite('ribflv_e',2e-8)
test_tube.set_specific_metabolite('sel_e',1000)
test_tube.set_specific_metabolite('so3_e',1000)
test_tube.set_specific_metabolite('so4_e',1000)
test_tube.set_specific_metabolite('zn2_e',1000)

# create the model using CobraPy functionality
alt_cobra = cobra.io.read_sbml_model("../../GEM-repos/mit1002-core-model/core_314275.5_GP.SBML/core_314275.5_GP.xml")

# Change the objective of the COBRA model
# Not sure if that will cary over to the COMETS model, but trying it
alt_cobra.objective = "bio1_biomass"

# use the loaded model to build a comets model
alt = c.model(alt_cobra)

# remove the bounds from glucose import (will be set dynamically by COMETS)
alt.change_bounds('EX_glc__D_e', -1000, 1000) # FIXME: Do I need to change the name to be the KBase ID?
alt.change_bounds('EX_ac_e', -1000, 1000)

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
with open('alt_core/results.pkl', 'wb') as f:
    pickle.dump(experiment, f)

