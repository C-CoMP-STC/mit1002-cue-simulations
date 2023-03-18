import cobra
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle

# Import my own CUE functions
# I want the CUE functions to eventually be their own package, but for
# now I'm just importing them from a different folder in the same
# repository
import sys
sys.path.insert(0, 'cue_utils')
from utils import (
                   atomExchangeMetabolite,
                   calculate_cue,
                   calculate_gge,
                   extract_c_fates)

# Set a folder for the plots
# Assuming you are running from the root of the repository
output_folder = 'alt_nutrients/plots'

# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the results
with open('alt_nutrients/results.pkl', 'rb') as f:
    experiments = pickle.load(f)

# Load the model and get the exchange reactions
model = cobra.io.read_sbml_model('alt_nutrients/model.xml')
c_ex_rxns = atomExchangeMetabolite(model, ex_nomenclature={'C_e'})

# Plot bar charts of the C fates for each experiment
respiration = []
exudation = []
other = []
for experiment in experiments:
    fluxes = experiment.fluxes_by_species['Alteromonas_macleodii_MIT1002']
    cycle_resp, cycle_ex, cycle_other = extract_c_fates(fluxes, c_ex_rxns, resp_rxn = 'EX_co2_e')
    respiration.append(cycle_resp)
    exudation.append(cycle_ex)
    other.append(cycle_other)

# Because the others are tiny and one negative numeber, just make it 0s
other = [0]*len(other)

# Make labels for the x axis
labels = ["Glucose", "Acetate"]

fig, ax = plt.subplots()
ax.bar(labels, other, label='Biomass')
ax.bar(labels, exudation, bottom=other, label='Exudation')
ax.bar(labels, respiration, bottom=np.array(other)+np.array(exudation), label='Respiration')
plt.ylabel('Propotion of Uptaken Carbon')
plt.xlabel('Sole Carbon Source')
plt.title('Carbon Fates on Each Carbon Source')
plt.legend()

plt.savefig(os.path.join(output_folder, 'c_fates_per_c_source.png'))