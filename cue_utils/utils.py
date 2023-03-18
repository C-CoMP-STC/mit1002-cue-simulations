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
    # FIXME: This is where the issue is
    # compartment for CarveMe models is C_e
    # Compartment for BiGG models is e
    ex_atoms = {r.id: m.elements[atom] for m in model.metabolites for r in m.reactions if atom in m.elements if r.compartments == ex_nomenclature}

    return ex_atoms


def calculate_cue(row, c_ex_rxns, resp_rxn = 'EX_co2_e'):
    # TODO: Document this function
    # Get the exchange fluxes for the current cycle
    c_ex_fluxes = [float(row[r]) * -c for r, c in c_ex_rxns.items()]
    # Calculate the CUE for the current cycle and add it to the cue array
    uptake = sum([flux for flux in c_ex_fluxes if flux > 0])
    respiration = row[resp_rxn]
    if uptake == 0:
        cue = None
    else:
        cue = 1 - respiration/uptake
    
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


def extract_c_fates(row, c_ex_rxns, resp_rxn = 'EX_co2_e', norm = True):
    # TODO: Document this function
    # Get the exchange fluxes for the current cycle
    c_ex_fluxes = {r: float(row[r]) * -c for r, c in c_ex_rxns.items()}
    # Use the exchange fluxes to calculate uptake, resp, and exudation
    uptake = sum([flux for rxn, flux in c_ex_fluxes.items() if flux > 0])
    respiration = abs(c_ex_fluxes[resp_rxn])
    exudation = abs(sum([flux for rxn, flux in c_ex_fluxes.items()
                         if flux < 0 and rxn != resp_rxn]))
    # Calculate the biomass as everything that is not uptake or respiration
    biomass = uptake - respiration - exudation
    # Normalize everything to the uptake or not
    if norm == True:
        if uptake == 0:
            exudation_norm = 0
            respiration_norm = 0
            biomass_norm = 0
        else:
            respiration_norm = respiration/uptake
            exudation_norm = exudation/uptake
            biomass_norm = biomass/uptake
        return [respiration_norm, exudation_norm, biomass_norm]
    else:
        return [respiration, exudation, biomass]
    