import cobra
import numpy as np
import matplotlib
import seaborn as sns
import pandas as pd
import os

from gem2cue import utils as gem2cue


OUT_DIR = os.path.dirname(os.path.realpath(__file__))


def main():
    # Load in the model
    model_path = '../../GEM-repos/mit1002-model/model.xml'
    model = cobra.io.read_sbml_model(model_path)

    # Get the exchange reactions
    # Since they don't change with the maintenance, we can just get them once
    c_ex_rxns = gem2cue.get_c_ex_rxns(model)

    # Get the ID for the biomass reaction
    # Since it doesn't change with the maintenance, we can just set it once
    biomass_rxn = 'bio1_biomass'

    # Set the medium so that glucose is the only carbon source and oxygen
    # is constrained to give reasonable growth rates
    # TODO: Use an uptake rate based on the NMR data
    glc_medium = {'EX_cpd00027_e0': 10,  # D-Glucose_e0
                  # Not sure what value to use for oxygen
                  'EX_cpd00007_e0': 1000,  # O2_e0
                  # Remaining minimal media components
                  'EX_cpd00058_e0': 1000,  # Cu2+_e0
                  'EX_cpd00971_e0': 1000,  # Na+_e0
                  'EX_cpd00063_e0': 1000,  # Ca2+_e0
                  'EX_cpd00048_e0': 1000,  # Sulfate_e0
                  'EX_cpd10516_e0': 1000,  # fe3_e0
                  'EX_cpd00254_e0': 1000,  # Mg_e0
                  'EX_cpd00009_e0': 1000,  # Phosphate_e0
                  'EX_cpd00205_e0': 1000,  # K+_e0
                  'EX_cpd00013_e0': 1000,  # NH3_e0
                  'EX_cpd00099_e0': 1000,  # Cl-_e0
                  'EX_cpd00030_e0': 1000,  # Mn2+_e0
                  'EX_cpd00075_e0': 1000,  # Nitrite_e0
                  'EX_cpd00001_e0': 1000,  # H2O_e0
                  'EX_cpd00635_e0': 1000,  # Cbl_e0
                  'EX_cpd00034_e0': 1000,  # Zn2+_e0
                  'EX_cpd00149_e0': 1000,  # Co2+_e0
                  }
    model.medium = glc_medium

    # Optimize and calculate CUE for a range of maintenance values
    # Save the maintenance values, biomass, and CUE to a dictionary in a list
    data = []
    for vm in np.linspace(0, 20, 5):
        # Update maintainance flux
        model.reactions.ATPM.lower_bound = vm

        # TODO: Run model and calculate CUE
        solution = model.optimize()
        u_fluxes, ex_fluxes, biomass_flux = gem2cue.get_c_ex_rxn_fluxes(model,
                                                                        solution,
                                                                        c_ex_rxns,
                                                                        biomass_rxn,
                                                                        'COBRApy')
        cue = gem2cue.calculate_cue(u_fluxes, ex_fluxes, co2_ex_rxn="EX_cpd00011_e0")

        # Save
        d = {'vm': vm,
             'biomass': solution.objective_value,
             'atpm_flux': solution.fluxes.ATPM,
             'cue': cue}
        data.append(d)

    # Convert the results to a pandas dataframe
    df = pd.DataFrame(data)

    # Make a custom color map for plotting
    # Goes from Light blue to Dark blue
    cmap2 = CustomCmap([0.5686, 0.8314, 0.8627], [0, 0.2588, 0.388])

    # Plot the results
    g = sns.relplot(x='vm', y='cue', data=df, kind='line', marker='o',
                    height=3, palette=cmap2)
    g.set_axis_labels("ATPM Flux (mmol / [gDW h])", "CUE")

    # Save the figure
    g.savefig(os.path.join(OUT_DIR, 'cue_vs_atpm.png'), dpi=300)


# Make a custom color map
def CustomCmap(from_rgb, to_rgb):

    # from color r,g,b
    r1, g1, b1 = from_rgb

    # to color r,g,b
    r2, g2, b2 = to_rgb

    cdict = {'red': ((0, r1, r1),
                     (1, r2, r2)),
             'green': ((0, g1, g1),
                       (1, g2, g2)),
             'blue': ((0, b1, b1),
                      (1, b2, b2))}

    cmap = matplotlib.colors.LinearSegmentedColormap('custom_cmap', cdict)
    return cmap


if __name__ == "__main__":
    main()
