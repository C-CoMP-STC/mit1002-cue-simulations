import pickle
import os

# Path to results
# Assuming you are running from the root of the repository
output_folder = 'ecoli_full/c_sources/'

# Load the dictionary from find_c_classes
with open(os.path.join(output_folder, 'c_source_brite_list.pkl'), 'rb') as f:
    results = pickle.load(f)

# Make a new empty dictionary
results_clean = {}

# Loop through every entry in the old, messy dictionary
for key in results.keys():
    # Extract the list of strings from the BRITE hierarchy
    brite_words = results[key]
    # Determine what the class is based on what strings are in the value
    # and add it to the clean dictionary
    if 'Nucleic' in brite_words:
        results_clean[key] = 'Nucleic Acid'
    elif 'Amino' in brite_words:
        results_clean[key] = 'Amino Acid'
    elif 'Lipids' in brite_words:
        results_clean[key] = 'Lipid'
    elif 'Organic' in brite_words:
        results_clean[key] = 'Organic Acid'
    elif 'Monosaccharides' in brite_words:
        results_clean[key] = 'Monosaccharide'
    elif 'Oligosaccharides' in brite_words:
        results_clean[key] = 'Oligosaccharide'
    elif 'Vitamins' in brite_words:
        results_clean[key] = 'Vitamin'
    elif 'Dipeptides' in brite_words:
        results_clean[key] = 'Dipeptide'
    elif 'Glycosides' in brite_words:
        results_clean[key] = 'Glycoside'
    elif 'Amines' in brite_words:
        results_clean[key] = 'Amines'
    else:
        results_clean[key] = 'Unsure'

# Save results
with open(os.path.join(output_folder, 'c_source_class.pkl'), 'wb') as f:
    pickle.dump(results_clean, f)