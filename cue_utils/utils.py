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