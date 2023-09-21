import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

from gem2cue import utils as gem2cue


def plot_biomass(experiment, output_folder):
    """
    Plot the biomass over time for the given experiment.

    Parameters
    ----------
    experiment : c.comets
        The experiment to plot the biomass for.
    output_folder : str
        The path to the folder to save the plot to.
    """
    # Plot the biomass over time
    # Right now, can use total biomass because the simulation is only the E.
    # coli core model, but if I add other species, I will need to change
    ax = experiment.total_biomass.plot(x='cycle')
    ax.set_ylabel("Biomass (gr.)")

    # Convert the x ticks to hours by dividing by 100
    # TODO: Make this a variable
    ax.set_xticklabels([tick._x/100 for tick in ax.get_xticklabels()])
    ax.set_xlabel("Time (hours)")

    # Save the biomass plot
    plt.savefig(os.path.join(output_folder, 'biomass.png'))


def plot_fluxes(experiment, output_folder):
    """
    Plot the fluxes of certain reactions over time for the given experiment.
    Currently the reactions are hard coded to be the exchange reactions for
    oxygen, carbon dioxide, glucose, and acetate.

    Parameters
    ----------
    experiment : c.comets
        The experiment to plot the biomass for.
    output_folder : str
        The path to the folder to save the plot to.
    """
    # Plot the fluxes over time
    # The model doesn't have a name, it is just called ''
    ax = experiment.fluxes_by_species[''].plot(x="cycle",  # FIXME: Add an ID to the model file
                                            y=["EX_cpd00007_e0",  # EX_o2_e
                                                "EX_cpd00011_e0",  # EX_co2_e
                                                "EX_cpd00027_e0",  # Glucose
                                                "EX_cpd00029_e0"],  # Acetate
                                            kind="line")

    # Convert the x ticks to hours by dividing by 100
    ax.set_xticklabels([tick._x/100 for tick in ax.get_xticklabels()])
    ax.set_xlabel("Time (hours)")

    # Make a more human-friendly legend
    plt.legend(('O2 Exchange', 'CO2 Exchange', 'Glucose Exchange', 'Acetate Exchange'))

    # Save the biomass plot
    plt.savefig(os.path.join(output_folder, 'fluxes.png'))


def plot_media(model, experiment, output_folder):
    """
    Plot the media concentrations over time for the given experiment.

    Parameters
    ----------
    model : cobra.Model
        The model to get the metabolite names from.
    experiment : c.comets
        The experiment to plot the media for.
    output_folder : str
        The path to the folder to save the plot to.
    """
    # Plot the media concentrations over time
    media = experiment.media.copy()
    media = media[media.conc_mmol < 900]

    fig, ax = plt.subplots()
    for name, group in media.groupby('metabolite'):
        group.plot(x='cycle',
                   ax=ax,
                   y='conc_mmol',
                   label=model.metabolites.get_by_id(name).name)
    ax.set_ylabel("Concentration (mmol)")

    # Convert the x ticks to hours by dividing by 100
    ax.set_xticklabels([tick._x/100 for tick in ax.get_xticklabels()])
    ax.set_xlabel("Time (hours)")

    # Save the media plot with the default y lims
    plt.savefig(os.path.join(output_folder, 'media.png'))

    # Zoom in so I can see what the low metabolites are doing
    # FIXME: It still shows the legend of O2 which is confusing, maybe make
    # a new media df with a lower concentration threshold than 900
    ax.set_ylim(0, 0.022)  # Can only get this number by actually looking at it
    plt.savefig(os.path.join(output_folder, 'media-zoom-in.png'))


def plot_cue(model, experiment, biomass_rxn, output_folder,
             definitions=['cue', 'gge', 'bge', 'cumulative_cue']):
    """
    Plot the values for any of the CUE metrics over time for the given
    experiment.

    Parameters
    ----------
    model : cobra.Model
        The model to get the metabolite names from.
    experiment : c.comets
        The experiment to plot the media for.
    biomass_rxn : str
        The ID of the biomass reaction in the model.
    output_folder : str
        The path to the folder to save the plot to.
    definitions : list
        A list of the CUE metrics to plot. The options are 'cue', 'gge',
        'bge', and 'cumulative_cue'.
    """
    # Check that the definitions are valid
    valid_definitions = ['cue', 'gge', 'bge', 'cumulative_cue']
    for definition in definitions:
        if definition not in valid_definitions:
            raise ValueError(f"The definition {definition} is not valid. "
                             f"Valid definitions are {valid_definitions}")

    # Get the exchange reactions for the model
    # FIXME: I think I would rather do this in the comets_simulation script,
    # and save the exchange reactions with the results, but for now just do it
    # here
    c_ex_rxns = gem2cue.get_c_ex_rxns(model)

    # Get the fluxes for each exchange reaction for each cycle of the
    # experiment
    fluxes = experiment.fluxes_by_species[''].copy()
    # Create an empty array to hold the CUE for each cycle
    cue_list = []
    gge_list = []
    bge_list = []
    # Loop through each cycle and calculate the CUE and the GGE
    for index, row in fluxes.iterrows():
        u_fluxes, ex_fluxes, biomass_flux = gem2cue.get_c_ex_rxn_fluxes(model,
                                                                        row,
                                                                        c_ex_rxns,
                                                                        biomass_rxn,
                                                                        'COMETS')
        cue_list.append(gem2cue.calculate_cue(u_fluxes, ex_fluxes,
                                            co2_ex_rxn="EX_cpd00011_e0"))
        gge_list.append(gem2cue.calculate_gge(u_fluxes, ex_fluxes,
                                            co2_ex_rxn="EX_cpd00011_e0"))
        bge_list.append(gem2cue.calculate_bge(ex_fluxes, biomass_flux,
                                            co2_ex_rxn="EX_cpd00011_e0"))
    
    # Calculate the cumulative CUE
    media = experiment.media.copy()
    # Get the initial concentration of glucose
    glc_conc = media[media.metabolite == 'cpd00027_e0'].iloc[0].conc_mmol
    # Get the initial concentration of CO2
    co2_conc = media[media.metabolite == 'cpd00011_e0'].iloc[0].conc_mmol

    # Calculate the cumulative CUE for each cycle
    cumulative_cue = []
    for i in range(len(cue_list)):
        # Get the cumulative CO2
        # Filter the media dataframe to only include the current cycle and the
        # metabolite glucose, but if that cycle isn't in the media dataframe,
        # skip it
        if len(media[media.cycle == cycle_list[i]][media.metabolite == 'cpd00027_e0']) == 0:
            cumulative_cue.append(None)
            continue
        else:
            cumulative_glc = glc_conc - media[media.cycle == cycle_list[i]][media.metabolite == 'cpd00027_e0'].iloc[0].conc_mmol
        # Do the same for CO2
        if len(media[media.cycle == cycle_list[i]][media.metabolite == 'cpd00011_e0']) == 0:
            cumulative_cue.append(None)
            continue
        else:
            cumulative_co2 = media[media.cycle == cycle_list[i]][media.metabolite == 'cpd00011_e0'].iloc[0].conc_mmol - co2_conc

        # Calculate the cumulative CUE
        cumulative_cue.append(1 - cumulative_co2 / cumulative_glc)

    # Plot the specified values for each cycle
    cycle_list = experiment.fluxes_by_species['']['cycle'].tolist()
    fig, ax = plt.subplots()
    if 'cue' in definitions:
        plt.plot(cycle_list, cue_list, label="CUE")
    if 'gge' in definitions:
        plt.plot(cycle_list, gge_list, '--', label="GGE")
    if 'bge' in definitions:
        plt.plot(cycle_list, bge_list, ':', label="BGE")
    if 'cumulative_cue' in definitions:
        plt.plot(cycle_list, cumulative_cue, '-.', label="Cumulative CUE")

    ax.set_ylabel("Value")
    # ax.set_ylim(0, 1) # Would need to increase the upper limit so that the line is visible
    ax.set_xlim(0, max(cycle_list))
    ax.set_xticklabels([tick._x/100 for tick in ax.get_xticklabels()])
    ax.set_xlabel("Time (hours)")
    plt.legend()

    plt.savefig(os.path.join(output_folder, 'cue.png'))


def plot_c_fates(model, experiment, biomass_rxn, output_folder):
    """
    Plot the carbon fates over time for the given experiment.

    Parameters
    ----------
    model : cobra.Model
        The model to get the metabolite names from.
    experiment : c.comets
        The experiment to plot the carbon fates for.
    biomass_rxn : str
        The ID of the biomass reaction in the model.
    output_folder : str
        The path to the folder to save the plot to.
    """
    # Get the fluxes
    fluxes = experiment.fluxes_by_species[''].copy()
    unaccounted = []
    respiration = []
    exudation = []
    biomass = []
    for index, row in fluxes.iterrows():
        cycle_biomass = gem2cue.get_biomass_carbon(row, biomass_rxn, model, 'COMETS')
        uptake_fluxes, secretion_fluxes = gem2cue.get_c_ex_rxn_fluxes(row, c_ex_rxns,
                                                            'COMETS')
        cycle_uptake = gem2cue.get_c_uptake(uptake_fluxes)
        cycle_co2 = gem2cue.get_co2_secretion(secretion_fluxes, 'EX_cpd00011_e0')
        cycle_secretion = gem2cue.get_org_c_secretion(secretion_fluxes, 'EX_cpd00011_e0')

        unaccounted.append(cycle_uptake - (cycle_co2 + cycle_secretion + cycle_biomass))
        respiration.append(cycle_co2)
        exudation.append(cycle_secretion)
        biomass.append(cycle_biomass)

    # Plot 5: Plot bar chart of carbon fates for each cycle
    # width = 0.35
    cycle_list = experiment.fluxes_by_species['']['cycle'].tolist()
    fig, ax = plt.subplots()
    ax.bar(cycle_list, biomass, label='Biomass')
    ax.bar(cycle_list, exudation, bottom=biomass, label='Organic C')
    ax.bar(cycle_list, respiration, bottom=np.array(biomass)+np.array(exudation),
        label='CO2')
    ax.bar(cycle_list, unaccounted,
        bottom=np.array(biomass)+np.array(exudation)+np.array(respiration),
        label='Unaccounted')
    plt.ylabel('Carbon Atom Flux')
    ax.set_xticklabels([tick._x/100 for tick in ax.get_xticklabels()])
    ax.set_xlabel("Time (hours)")
    plt.title('Carbon Fates at Each Cycle')
    plt.legend()

    plt.savefig(os.path.join(output_folder, 'c_fates_per_cycle.png'))