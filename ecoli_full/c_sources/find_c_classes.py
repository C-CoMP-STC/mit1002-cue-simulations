import os
import cobra
from Bio.KEGG import REST
import pandas as pd
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
                   extract_c_fates_from_solution)

# Function to take the string result from KEGG and make a dictionary
def kegg_to_dict(result):
    # Make a dictionary to store the results
    res = {}

    # Loop through every line (makred by '\n')
    for line in result.split('\n'):
        # Split the line based on spaces, and remove the empty strings
        words = [x for x in line.split(' ') if x]

        # Skip lines that are empty or that have no letters
        # This was really from looking at it and failing, make the logic better
        if line == '' or ' ' not in line:
            continue
        # If the line starts with a string (i.e. not a space), then make
        # a new key based on the first word in the line, and add all the
        # other words to the value
        elif line[0].isalpha():
            res[words[0]] = words[1:]
        # If the line starts with a space, then add the words to the
        # value of the last key
        else:
            res[list(res.keys())[-1]].extend(words)

    return res


# Set a folder for the resulting CSV
# Assuming you are running from the root of the repository
output_folder = 'ecoli_full/c_sources/'

# Load the E. coli full model, using the built in model from COBRApy
model = cobra.io.load_model("iJO1366")

# Get the exchange reactions
c_ex_rxns = atomExchangeMetabolite(model)

########################################################################
# Loop through the carbon sources, use KEGG to find their class
########################################################################
# Make a dataframe to store the results
results = {}
# Loop through all the carbon sources
for c_ex_rxn in c_ex_rxns:
    # Get the KEGG ID for the metabolite
    if 'kegg.compound' in list(model.reactions.get_by_id(c_ex_rxn).metabolites)[0].annotation.keys():
        kegg_id = list(model.reactions.get_by_id(c_ex_rxn).metabolites)[0].annotation['kegg.compound']
    else:
        # If there is no KEGG ID, skip this metabolite
        continue
    # Search for the metabolite in KEGG
    kegg_res = REST.kegg_get(kegg_id).read()
    # Try to read the results, if there are no results, skip this metabolite
    if not kegg_res: # FIXME: This is not working, it is catching '\n' but not ''
        continue
    else:
        # Convert the kegg results to a dictionary
        kegg_dict = kegg_to_dict(kegg_res)
        # Check if the BRITE results are in the dictionary
        if 'BRITE' in kegg_dict.keys():
            results[c_ex_rxn] = kegg_dict['BRITE']
        else:
            continue

########################################################################
# Save the results
########################################################################
with open(os.path.join(output_folder, 'c_source_brite_list.pkl'), 'wb') as f:
    pickle.dump(results, f)

