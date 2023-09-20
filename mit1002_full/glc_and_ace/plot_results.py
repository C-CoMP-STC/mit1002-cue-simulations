import pickle
import cobra
import os
import matplotlib.pyplot as plt

# Set the output directory (where the results.pkl file will be saved)
OUT_DIR = os.path.dirname(os.path.realpath(__file__))

# Set the path to the model file
MODEL_DIR = '../../GEM-repos/mit1002-model'

# Set a folder for the plots
OUTPUT_FOLDER = os.path.join(OUT_DIR, 'plots')


def main():
    # Check if the output folder exists, if not, create it
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Load the results from the COBRA simulations
    with open(os.path.join(OUT_DIR, 'results.pkl'), 'rb') as f:
        cobra_results = pickle.load(f)

    glc_only_fba = cobra_results[0]
    glc_only_pfba = cobra_results[1]
    ace_only_fba = cobra_results[2]
    ace_only_pfba = cobra_results[3]
    mix_fba = cobra_results[4]
    mix_pfba = cobra_results[5]

    # Load in the ALT model using COBRApy
    model = cobra.io.read_sbml_model(os.path.join(MODEL_DIR, 'model.xml'))

    ########################################################################
    # Barchart of all reactions that consume glucose or acetate
    ########################################################################
    plot_glc_and_ace_fluxes(model,
                            glc_only_fba.fluxes,
                            'Glucose Only')
    plot_glc_and_ace_fluxes(model,
                            ace_only_fba.fluxes,
                            'Acetate Only')
    plot_glc_and_ace_fluxes(model,
                            mix_fba.fluxes,
                            'Mixed Media (Glucose and Acetate)')


def plot_glc_and_ace_fluxes(model: cobra.Model, solution_fluxes: dict,
                            plot_title: str):
    """Plot all the fluxes involving gluocse and acetate as a bar chart"""
    rxns_of_interest = ['EX_cpd00027_e0']
    # Get the reactions that consume glucose
    glc_met = model.metabolites.cpd00027_c0
    glc_rxns = [reaction for reaction in model.reactions if glc_met in reaction.metabolites]
    for rxn in glc_rxns:
        rxns_of_interest.append(rxn.id)
    # Get the reactions that consume acetate
    rxns_of_interest.append('EX_cpd00029_e0')
    ace_met = model.metabolites.cpd00029_c0
    ace_rxns = [reaction for reaction in model.reactions if ace_met in reaction.metabolites]
    for rxn in ace_rxns:
        rxns_of_interest.append(rxn.id)
    # Plot the results
    # Filter the results dictionary to only include the reactions of interest
    fluxes_of_interest = {k: v for k, v in solution_fluxes.items() if k in rxns_of_interest}

    # Update the dict to have the whole reaction name, not just the ID
    fluxes_to_plot = {}
    for id in fluxes_of_interest.keys():
        rxn_name = model.reactions.get_by_id(id).name
        fluxes_to_plot[id + ' (' + rxn_name + ')'] = fluxes_of_interest[id]

    # Barchart
    # Increase the figure size
    plt.figure(figsize=(10, 15))  # Make figure large enough for reaction names
    plt.bar(range(len(fluxes_to_plot)),
            list(fluxes_to_plot.values()),
            align='center')
    plt.xticks(range(len(fluxes_to_plot)),
            list(fluxes_to_plot.keys()))
    # Turn the x-axis labels sideways
    plt.xticks(rotation=90)
    # Add a title
    plt.title('Glucose and Acetate Fluxes for FBA on ' + plot_title)
    # Tight layout so that the captions don't run off the page
    plt.tight_layout()

    # Save the plot
    plot_name = 'glc_and_ace_fluxes_' + plot_title.replace(" ", "_").lower() + '.png'
    plt.savefig(os.path.join(OUTPUT_FOLDER, plot_name))


if __name__ == '__main__':
    main()
