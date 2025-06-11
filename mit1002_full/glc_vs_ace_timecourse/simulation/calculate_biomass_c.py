import os
import pickle

import cobra
import cometspy as c

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# TODO: Should I pull a specific version of the model? From the remote? Can I checkout a local tag?
MODEL_DIR = "/Users/helenscott/Documents/PhD/Segre-lab/GEM-repos/GEM-mit1002"

biomass_id = "bio1_biomass"  # Biomass


def update_dict(d, new_items):
    """Update a dictionary with new items."""
    for key, value in new_items.items():
        if key in d:
            d[key] += value
        else:
            d[key] = value


# Load the model using COBRApy
model = cobra.io.read_sbml_model(os.path.join(MODEL_DIR, "model.xml"))

# Get the biomass reaction object
bio_rxn_obj = model.reactions.get_by_id(biomass_id)

# Make a new metabolite/coefficient dictionary for the biomass reaction with
# "unlumped" components
unlumped_metabolites = {}
for metabolite, coeff in bio_rxn_obj.metabolites.items():
    # If the metabolite is a lumped component, skip it
    if metabolite.id in ["cpd11461_c0", "cpd11463_c0", "cpd11462_c0"]:
        # Find the reactions that produces the lumped metabolite
        # Find the reaction in the model that makes the lumped metabolite
        synth_rxn = [r for r in model.reactions if metabolite in r.products]
        # Throw an error if there is not exactly one reaction that makes the lumped metabolite
        if len(synth_rxn) != 1:
            raise ValueError(
                "There should be exactly one reaction that makes the lumped metabolite"
            )
        # Get the reaction
        synth_rxn = synth_rxn[0]
        # Loop trhough all of the metabolites in the reaction
        for subcomponent, sub_coeff in synth_rxn.metabolites.items():
            # If the metabolite is not a lumped component, add it to the list of biomass compounds
            if subcomponent.id not in ["cpd11461_c0", "cpd11463_c0", "cpd11462_c0"]:
                # Add the metabolite and coefficient to the dictionary
                update_dict(
                    unlumped_metabolites,
                    {subcomponent: sub_coeff * abs(coeff)},
                )
    # Otherwise, add the metabolite and coefficient to the dictionary
    else:
        update_dict(unlumped_metabolites, {metabolite: coeff})

total_c_atom = 0
total_weight = 0
# Loop through all of the biomass components
for component, s_coeff in unlumped_metabolites.items():
    # If the component does not contain carbon, skip it
    if "C" not in component.elements.keys():
        continue
    # Get the number of carbon atoms in the component
    n_c_atoms = component.elements["C"]
    # Multiply the number of carbon atoms by the stoichiometric coefficient
    component_c_atoms = n_c_atoms * s_coeff
    # Add the flux to the total c_atom_flux
    total_c_atom += component_c_atoms
    # Add the weight of the component to the total biomass weight
    total_weight += component.formula_weight * s_coeff

# Calculate the mmol of carbon per g of biomass
mmol_c_per_g_biomass = total_c_atom / total_weight * 6.022e20

# Save the mmol_c_per_g_biomass to a pickle file
with open(os.path.join(FILE_DIR, "mmol_c_per_g_biomass.pkl"), "wb") as f:
    pickle.dump(mmol_c_per_g_biomass, f)
