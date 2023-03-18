import seaborn as sns
import matplotlib.pyplot as plt
import os
import pickle

# Set a folder for the plots
# Assuming you are running from the root of the repository
output_folder = 'ecoli_full_model/basic_fba/plots'

# Check if the folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the results
with open('ecoli_full_model/basic_fba/results.pkl', 'rb') as f:
    results = pickle.load(f)

# Get the dataframes
nitrogen_results = results[0]
carbon_results = results[1]
vm_results = results[2]

########################################################################
# CUE vs Nitrogen and ATPM (Steady Glucose)
########################################################################
g = sns.relplot(x='ammonia', y='cue', hue='vm', data=nitrogen_results, 
                kind='line', marker='o', height=3)

# Save the plot
plt.savefig(os.path.join(output_folder, 'cue_ammonia_vm.png'))

########################################################################
# CUE vs Glucose and ATPM (Steady Nitrogen)
########################################################################
g = sns.relplot(x='glc', y='cue', hue='vm', data=carbon_results, kind='line',
                marker='o', height=3)

# Save the plot
plt.savefig(os.path.join(output_folder, 'cue_glc_vm.png'))

########################################################################
# CUE vs ATPM (Steady Carbon and Nitrogen)
########################################################################
g = sns.relplot(x='vm', y='cue', data=vm_results, kind='line', marker='o',
                height=3)

# Save the plot
plt.savefig(os.path.join(output_folder, 'cue_vm.png'))