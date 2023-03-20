import seaborn as sns
import matplotlib.pyplot as plt
import os
import pickle

# Set a folder for the plots
# Assuming you are running from the root of the repository
output_folder = 'ecoli_full/c_sources/single/plots'

# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the results
with open('ecoli_full/c_sources/single/results.pkl', 'rb') as f:
    results = pickle.load(f)

########################################################################
# Carbon Fates vs Carbon Source
########################################################################
data = results[['respiration', 'exudation', 'biomass']]
# Plot the stacked bar plot
g = data.plot(kind='bar', stacked=True, color=['red', 'skyblue', 'green'])
# Set the x label
g.set_xlabel('Carbon Import Reaction')
# Turn the x labels to be 90 degrees
g.set_xticklabels(g.get_xticklabels(), rotation=90) # TODO: Change to the metnaolite name rather than the reaction name
# Set the y label
g.set_ylabel('Carbon Molecules (mmol/ [gDW h])')
# Title the plot based on the ATPM value
g.set_title('Carbon Fates')
# Save the plot
plt.savefig(os.path.join(output_folder, 'c_fates.png'))