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

# Load the class results
with open('ecoli_full/c_sources/c_source_class.pkl', 'rb') as f:
    class_results = pickle.load(f)

# Add the class to the results
# Add a column for the class to the results dataframe
results['class'] = None
# Loop through the class results and add the class to the results dataframe
for c_course, c_class in class_results.items():
    results.loc[results['c-source'] == c_course, 'class'] = c_class

########################################################################
# Plot a distribution of the CUEs by class
########################################################################
# Plot boxplots of the CUEs by class
fig, ax = plt.subplots()
results[['class', 'cue']].boxplot(by='class', ax = ax)
# Set the x label
plt.xlabel('Carbon Source Class')
# Rotate the x labels
plt.xticks(rotation=90)
# Set the y label
plt.ylabel('CUE')
# Title the plot
plt.title('CUE vs. Carbon Source Class')
fig.tight_layout()

# Save the plot
plt.savefig(os.path.join(output_folder, 'cue_by_class.png'))
# Clear the plot
plt.clf()

########################################################################
# Plot a distribution of the GGEs by class
########################################################################
# Plot boxplots of the CUEs by class
fig, ax = plt.subplots()
results[['class', 'gge']].boxplot(by='class', ax = ax)
# Set the x label
plt.xlabel('Carbon Source Class')
# Rotate the x labels
plt.xticks(rotation=90)
# Set the y label
plt.ylabel('GGE')
# Title the plot
plt.title('GGE vs. Carbon Source Class')
fig.tight_layout()

# Save the plot
plt.savefig(os.path.join(output_folder, 'gge_by_class.png'))
# Clear the plot
plt.clf()