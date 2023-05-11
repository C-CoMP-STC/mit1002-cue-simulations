def atomExchangeMetabolite(model, atom = 'C', ex_nomenclature = {'e'}):
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
    