import pandas as pd
import cobra

def get_c_ex_rxns(model, atom = 'C'):
    # TODO: Infer the ex_nomenclature rather than forcing the user to provide it
    """Get number of carbon atoms associated with each exchange reaction

    Args:
        model (cobra.core.Model): A file that has already been read in
        atom (string): String of atom of interest
        ex_nomenclature (set): Set of strings of the exchange nomenclature

    Returns:
        ex_atoms (dict): Dictionary with the IDs as the rxn names, and the
            values as the number of atoms associates
    """
    # This assumes that there is only ever one reactant in an exchange
    # reaction
    ex_atoms = {ex_rxn.id: ex_rxn.reactants[0].elements[atom] for 
                ex_rxn in model.exchanges
                if atom in ex_rxn.reactants[0].elements}

    return ex_atoms


def get_c_ex_rxn_fluxes(solution, c_ex_rxns, tool_used):
    """Use the list of dictionary of exchange reactions to make a
    two dictionaries of reactions and the number of carbon atoms
    exchanged (the flux times the number of carbon atoms in the
    metabolite). Makes one dictionary for uptake exchanges and another
    dictionary for secretion excahnges.

    Args:
    solution (pd.Series OR cobra.Solution): Results from FBA


    Returns:
    
    """
    # Check that the tool used matches with the expected type of the
    # solution object
    if tool_used.lower() != 'comets' and tool_used.lower() != 'cobrapy':
        raise ValueError('Function does not recognize the value supplied ' +
                         'for `tool_used`. Select from `COMETS` or `COBRApy`' +
                         ' (capitalization does not matter). You supplied ' +
                         tool_used + '.')
    if tool_used.lower() == 'comets' and not isinstance(solution, pd.Series):
        raise ValueError('Function was expecting results from a COMETS' +
                         'simulation as a pandas.Series object, but was ' +
                         'given the solution as a ' + type(solution) +
                         'object.')
    if tool_used.lower() == 'cobrapy' and not isinstance(solution, cobra.Solution):
        raise ValueError('Function was expecting results from a COBRApy' +
                         'simulation as a cobra.Solution object, but was ' +
                         'given the solution as a ' + type(solution) +
                         'object.')
    
    # Make a dictionary of all carbon atom fluxes (reaction flux * number of
    # carbon atoms). Have to access the fluxes differently if the results are
    # from COMETS or COBRApy.
    if tool_used.lower == 'comets':
        c_ex_fluxes = {rxn_id: float(solution[rxn_id]) * n_atoms
                       for rxn_id, n_atoms in c_ex_rxns.items()}
    if tool_used.lower == 'cobrapy':
        c_ex_fluxes = {rxn_id: solution.fluxes[rxn_id] * n_atoms
                       for rxn_id, n_atoms in c_ex_rxns.items()}
    
    # Set the signs for the uptake and secretion
    
    # Separate the uptake and secretion fluxes based on the sign
    uptake = {rxn_id: abs(atom_flux)
              for rxn_id, atom_flux in c_ex_fluxes.items()
              if atom_flux < 0}
    secretion = {rxn_id: abs(atom_flux)
                 for rxn_id, atom_flux in c_ex_fluxes.items()
                 if atom_flux > 0}

    return uptake, secretion

def get_co2_secretion(secretion_fluxes, co2_ex_rxn = 'EX_co2_e'):
    """Get the total number of carbon atoms lost from the cell as CO2

    Args:
    secretion_fluxes (dict): Dictionary of carbon secreting reactions
        with the reaction ID and the absolute value of the carbon atom
        flux
    co2_ex_rxn (str): Reaction ID for the CO2 exchange reaction.
        Defaults to the BiGG ID 'EX_co2_e'.

    Returns:
    co2_flux (float): Numeric value for the carbon atom flux for CO2
        secretion
    
    """
    co2_flux = secretion_fluxes[co2_ex_rxn]

    return co2_flux


def get_org_c_secretion(secretion_fluxes, co2_ex_rxn = 'EX_co2_e'):
    """Get the total number of carbon atoms lost from the cell as
    organic carbon

    Args:
    secretion_fluxes (dict): Dictionary of carbon secreting reactions
        with the reaction ID and the absolute value of the carbon atom
        flux
    co2_ex_rxn (str): Reaction ID for the CO2 exchange reaction.
        Defaults to the BiGG ID 'EX_co2_e'.

    Returns:
    org_c_secretion_flux (float): Numeric value for the carbon atom flux
        for all secretion reactions other than CO2.
    """
    org_c_secretion_flux = sum([c_atom_flux
                                for rxn, c_atom_flux in secretion_fluxes.items()
                                if rxn != co2_ex_rxn])

    return org_c_secretion_flux


def get_c_uptake(uptake_fluxes):
    """Get the total number of organic carbon atoms taken up. Would
    include CO2 if that is taken up.

    Args:
    secretion_fluxes (dict): Dictionary of carbon importing reactions
        with the reaction ID and the absolute value of the carbon atom
        flux

    Returns:
    uptake_flux (float): Numeric value for the total carbon atom flux
        for all import reactions
    """
    secretion_flux = sum([c_atom_flux
                          for rxn, c_atom_flux in uptake_fluxes.items()])

    return secretion_flux


def get_biomass_carbon():
    """Get the total number of carbon atoms used by the biomass reaction

    Args:
    

    Returns:
    
    """
    pass


def calculate_cue(row, c_ex_rxns, co2_ex_rxn = 'EX_co2_e'):
    # TODO: Document this function
    # Get the exchange fluxes for the current cycle
    c_ex_fluxes = [float(row[r]) * -c for r, c in c_ex_rxns.items()]
    # Calculate the CUE for the current cycle and add it to the cue array
    uptake = sum([flux for flux in c_ex_fluxes if flux > 0])
    co2_ex = row[co2_ex_rxn]
    if uptake == 0:
        cue = None
    else:
        cue = 1 - co2_ex/uptake
    
    return cue


def calculate_gge(row, c_ex_rxns):
    # TODO: Document this function
    # Get the exchange fluxes for the current cycle
    c_ex_fluxes = [float(row[r]) * -c for r, c in c_ex_rxns.items()]
    # Calculate the CUE for the current cycle and add it to the cue array
    uptake = sum([flux for flux in c_ex_fluxes if flux > 0])
    release = sum([flux for flux in c_ex_fluxes if flux < 0])
    if uptake == 0:
        gge = None
    else:
        gge = 1 + release/uptake
    
    return gge


def extract_c_fates(row, c_ex_rxns, co2_ex_rxn = 'EX_co2_e', norm = True):
    # TODO: Document this function
    # Get the exchange fluxes for the current cycle
    c_ex_fluxes = {r: float(row[r]) * -c for r, c in c_ex_rxns.items()}
    # Use the exchange fluxes to calculate uptake, resp, and exudation
    uptake = sum([flux for rxn, flux in c_ex_fluxes.items() if flux > 0])
    co2_ex = abs(c_ex_fluxes[co2_ex_rxn])
    exudation = abs(sum([flux for rxn, flux in c_ex_fluxes.items()
                         if flux < 0 and rxn != co2_ex_rxn]))
    # Calculate the biomass as everything that is not uptake or co2_ex
    biomass = uptake - co2_ex - exudation
    # Normalize everything to the uptake or not
    if norm == True:
        if uptake == 0:
            exudation_norm = 0
            co2_ex_norm = 0
            biomass_norm = 0
        else:
            co2_ex_norm = co2_ex/uptake
            exudation_norm = exudation/uptake
            biomass_norm = biomass/uptake
        return [co2_ex_norm, exudation_norm, biomass_norm]
    else:
        return [co2_ex, exudation, biomass]


def extract_c_fates_from_solution(solution, c_ex_rxns, co2_ex_rxn = 'EX_co2_e', norm = True):
    # TODO: Document this function
    # Get the exchange fluxes for the current cycle
    c_ex_fluxes = {r: solution.fluxes[r] * c for r, c in c_ex_rxns.items()}
    # Use the exchange fluxes to calculate uptake, resp, and exudation
    uptake = sum([flux for rxn, flux in c_ex_fluxes.items() if flux < 0
                  and rxn != co2_ex_rxn]) # Should I count the co2_ex_rxn here?
    if c_ex_fluxes[co2_ex_rxn] < 0:
        # If the co2 flux is negative than the model is taking up CO2???
        co2_ex = 0
    else:
        co2_ex = c_ex_fluxes[co2_ex_rxn]
    exudation = abs(sum([flux for rxn, flux in c_ex_fluxes.items()
                         if flux > 0 and rxn != co2_ex_rxn]))
    # Calculate the biomass as everything that is not uptake or co2 release
    biomass = abs(uptake) - co2_ex - exudation
    # Normalize everything to the uptake or not
    if norm == True:
        if uptake == 0:
            co2_release_norm = 0
            exudation_norm = 0
            biomass_norm = 0
        else:
            co2_release_norm = co2_ex/uptake
            exudation_norm = exudation/uptake
            biomass_norm = biomass/uptake
        return [co2_release_norm, exudation_norm, biomass_norm]
    else:
        return [abs(uptake), co2_ex, exudation, biomass]
    