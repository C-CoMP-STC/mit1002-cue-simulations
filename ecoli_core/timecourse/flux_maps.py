# Wanted to make Escher maps for the fluxes at different time points,
# but I can't install Escher on the base conda environment

# Flow now just look at the fluxes at a couple time points

from cobra.io import load_model
import pickle

import sys
sys.path.insert(0, 'cue_utils')
from utils import atomExchangeMetabolite

# Load the results
with open('well_mixed_ecoli_core/results.pkl', 'rb') as f:
    experiment = pickle.load(f)

# Load the E. coli model (Needed to get the exchange reactions)
e_coli_cobra = load_model('textbook')

# Get the exchange reactions for the E coli core model
c_ex_rxns = atomExchangeMetabolite(e_coli_cobra)

# Get the fluxes from the experiment
fluxes = experiment.fluxes_by_species['e_coli_core'].copy()

# Get the fluxes at the first time point
row = fluxes[fluxes.cycle == 1]
glucose_fluxes = {r: float(row[r]) * -c for r, c in c_ex_rxns.items()}
print("Fluxes on Glucose (cycle 1)")
print(glucose_fluxes)

# Get fluxes where GGE is going up during the diauxuc shift
# It's really jus tone point where GGE is going up
row = fluxes[fluxes.cycle == 444]
transition_fluxes = {r: float(row[r]) * -c for r, c in c_ex_rxns.items()}
print("Fluxes on Transition (cycle 444)")
print(transition_fluxes)

# Get the fluxes at the last time point
row = fluxes[fluxes.cycle == 500]
acetate_fluxes = {r: float(row[r]) * -c for r, c in c_ex_rxns.items()}
print("Fluxes on Acetate (cycle 500)")
print(acetate_fluxes)
