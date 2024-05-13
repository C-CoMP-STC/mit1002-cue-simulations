# This script is for setting up, running, and saving the results from a
# COMETS simulation
# The simulation is for the MIT1002 model in a 9x9 grid with 11mM glucose
# as the only carbon source

import cometspy as c
import cobra
import pickle
import os

# Set the output directory (where the results.pkl file will be saved)
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Create empty 10x10 layout
grid_size = 9
layout = c.layout()
layout.grid = [grid_size, grid_size]

# Load in the ALT model using COBRApy
cobra_model = cobra.io.read_sbml_model("../../GEM-repos/mit1002-model/model.xml")

# use the loaded model to build a comets model
comets_model = c.model(cobra_model)

# remove the bounds from glucose import (will be set dynamically by COMETS)
comets_model.change_bounds('EX_cpd00027_e0', -1000, 1000)
comets_model.change_bounds('EX_cpd00029_e0', -1000, 1000)

# Set bounds on O2
comets_model.change_bounds('EX_cpd00007_e0', -20, 1000)

# set the model's initial biomass
# FIXME: I think this is overwriting, and only using the last!
comets_model.initial_pop = [4, 4, 5E-6]

# add it to the layout
layout.add_model(comets_model)

# Add 11mM glucose
layout.set_specific_metabolite('cpd00027_e0', 0.011)

# Add plenty of oxygen
# FIXME: Should this be lower? to get a realistic bound on O2 flux?
layout.set_specific_metabolite("cpd00007_e0", 20)  # O2_e0

# Add the rest of the nutrients unlimited
layout.set_specific_metabolite("cpd00058_e0", 1000)  # Cu2+_e0
layout.set_specific_metabolite("cpd00971_e0", 1000)  # Na+_e0
layout.set_specific_metabolite("cpd00063_e0", 1000)  # Ca2+_e0
layout.set_specific_metabolite("cpd00048_e0", 1000)  # Sulfate_e0
layout.set_specific_metabolite("cpd10516_e0", 1000)  # fe3_e0
layout.set_specific_metabolite("cpd00254_e0", 1000)  # Mg_e0
layout.set_specific_metabolite("cpd00009_e0", 1000)  # Phosphate_e0
layout.set_specific_metabolite("cpd00205_e0", 1000)  # K+_e0
layout.set_specific_metabolite("cpd00013_e0", 1000)  # NH3_e0
layout.set_specific_metabolite("cpd00099_e0", 1000)  # Cl-_e0
layout.set_specific_metabolite("cpd00030_e0", 1000)  # Mn2+_e0
layout.set_specific_metabolite("cpd00075_e0", 1000)  # Nitrite_e0
layout.set_specific_metabolite("cpd00001_e0", 1000)  # H2O_e0
layout.set_specific_metabolite("cpd00635_e0", 1000)  # Cbl_e0
layout.set_specific_metabolite("cpd00034_e0", 1000)  # Zn2+_e0
layout.set_specific_metabolite("cpd00149_e0", 1000)  # Co2+_e0


# Set the parameters that are different from the default
sim_params = c.params()
sim_params.set_param('biomassMotionStyle', 'ConvNonlin Diffusion 2D')
sim_params.set_param('numDiffPerStep', 1)
sim_params.set_param('growthDiffRate', 0)
sim_params.set_param('allowCellOverlap', True)
sim_params.set_param('toroidalWorld', False)
sim_params.set_param('defaultVmax', 10)
sim_params.set_param('defaultKm', 0.000015)
sim_params.set_param('maxCycles', 3000)
sim_params.set_param('timeStep', .1)
sim_params.set_param('spaceWidth', 0.01)
sim_params.set_param('maxSpaceBiomass', 10)
sim_params.set_param('minSpaceBiomass', 1e-9)
sim_params.set_param('writeMediaLog', True)
sim_params.set_param('writeFluxLog', True)
sim_params.set_param('writeBiomassLog', True)
sim_params.set_param('BiomassLogRate', 100)
sim_params.set_param('FluxLogRate', 100)

# Create the experiment
experiment = c.comets(layout, sim_params)

# Run the simulation
experiment.run()

# Save the results
with open(os.path.join(OUT_DIR, 'results.pkl'), 'wb') as f:
    pickle.dump(experiment, f)
