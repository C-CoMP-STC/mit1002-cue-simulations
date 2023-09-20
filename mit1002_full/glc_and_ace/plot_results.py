import pickle
import cobra
import os

# Set the output directory (where the results.pkl file will be saved)
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Set a folder for the plots
# Assuming you are running from the root of the repository
output_folder = os.path.join(OUT_DIR, 'plots')

# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the results from the COBRA simulations
with open(os.path.join(OUT_DIR, 'results.pkl'), 'rb') as f:
    cobra_results = pickle.load(f)

# Load in the ALT model using COBRApy
alt_cobra = cobra.io.read_sbml_model("../../GEM-repos/mit1002-model/model.xml")

########################################################################
# Barchart of all reactions that consume glucose or acetate
########################################################################
# Get the reactions that consume glucose or acetate