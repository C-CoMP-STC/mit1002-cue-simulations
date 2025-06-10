import os
import pickle

import cobra
import cometspy as c

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(FILE_DIR, "results")
# TODO: Should I pull a specific version of the model? From the remote? Can I checkout a local tag?
MODEL_DIR = "/Users/helenscott/Documents/PhD/Segre-lab/GEM-repos/GEM-mit1002"

# Create the output directory if it does not exist
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

# Load in the ALT model using COBRApy
alt_cobra = cobra.io.read_sbml_model(os.path.join(MODEL_DIR, "model.xml"))

# Define the different experimental set-ups, giving each a filename friendly
# name, and define the carbon sources and their concentrations
carbon_sources = {
    "glucose": {"cpd00027_e0": 0.012},
    "acetate": {"cpd00029_e0": 0.012},
    "4glucose_8acetate": {"cpd00027_e0": 0.004, "cpd00029_e0": 0.008},
    "8glucose_4acetate": {"cpd00027_e0": 0.008, "cpd00029_e0": 0.004},
}

# Define shared nutrients and their concentrations
# TODO: Instead use the the defined media, can't use the current definition,
# becuase I need concentrations, not bounds
shared_nutrients = {
    "cpd00007_e0": 2,  # O2_e0
    "cpd00058_e0": 1000,  # Cu2+_e0
    "cpd00971_e0": 1000,  # Na+_e0
    "cpd00063_e0": 1000,  # Ca2+_e0
    "cpd00048_e0": 1000,  # Sulfate_e0
    "cpd10516_e0": 1000,  # fe3_e0
    "cpd00254_e0": 1000,  # Mg_e0
    "cpd00009_e0": 1000,  # Phosphate_e0
    "cpd00205_e0": 1000,  # K+_e0
    "cpd00013_e0": 1000,  # NH3_e0
    "cpd00099_e0": 1000,  # Cl-_e0
    "cpd00030_e0": 1000,  # Mn2+_e0
    "cpd00075_e0": 1000,  # Nitrite_e0
    "cpd00001_e0": 1000,  # H2O_e0
    "cpd00635_e0": 1000,  # Cbl_e0
    "cpd00034_e0": 1000,  # Zn2+_e0
    "cpd00149_e0": 1000,  # Co2+_e0
}

# Loop through objective optimization styles (FBA and pFBA)
for fba_type, objective_exp in {
    "fba": "MAXIMIZE_OBJECTIVE_FLUX",
    "pfba": "MAX_OBJECTIVE_MIN_TOTAL",
}.items():

    # Loop through each carbon source
    for exp_name, carbon_concentrations in carbon_sources.items():
        # Create empty 1x1 layout
        test_tube = c.layout()

        # Set the carbon source concentrations for this experiment
        for carbon_source, concentration in carbon_concentrations.items():
            test_tube.set_specific_metabolite(carbon_source, concentration)

        # Set shared nutrients
        for nutrient, value in shared_nutrients.items():
            test_tube.set_specific_metabolite(nutrient, value)

        # Use the loaded model to build a COMETS model
        alt = c.model(alt_cobra)

        # Convert the objective style so that the model uses pFBA
        alt.obj_style = objective_exp

        # Remove the bounds from carbon source imports (set dynamically by COMETS)
        # TODO: Find a way to set all of the bounds programmatically
        alt.change_bounds("EX_cpd00027_e0", -1000, 1000)
        alt.change_bounds("EX_cpd00029_e0", -1000, 1000)
        alt.change_bounds("EX_cpd00058_e0", -1000, 1000)  # Cu2+_e0
        alt.change_bounds("EX_cpd00007_e0", -1000, 1000)  # O2_e0
        alt.change_bounds("EX_cpd00971_e0", -1000, 1000)  # Na+_e0
        alt.change_bounds("EX_cpd00063_e0", -1000, 1000)  # Ca2+_e0
        alt.change_bounds("EX_cpd00048_e0", -1000, 1000)  # Sulfate_e0
        alt.change_bounds("EX_cpd10516_e0", -1000, 1000)  # fe3_e0
        alt.change_bounds("EX_cpd00254_e0", -1000, 1000)  # Mg_e0
        alt.change_bounds("EX_cpd00009_e0", -1000, 1000)  # Phosphate_e0
        alt.change_bounds("EX_cpd00205_e0", -1000, 1000)  # K+_e0
        alt.change_bounds("EX_cpd00013_e0", -1000, 1000)  # NH3_e0
        alt.change_bounds("EX_cpd00099_e0", -1000, 1000)  # Cl-_e0
        alt.change_bounds("EX_cpd00030_e0", -1000, 1000)  # Mn2+_e0
        alt.change_bounds("EX_cpd00075_e0", -1000, 1000)  # Nitrite_e0
        alt.change_bounds("EX_cpd00001_e0", -1000, 1000)  # H2O_e0
        alt.change_bounds("EX_cpd00034_e0", -1000, 1000)  # Zn2+_e0
        alt.change_bounds("EX_cpd00149_e0", -1000, 1000)  # Co2+_e0

        # Set the model's initial biomass
        alt.initial_pop = [0, 0, 5e-6]

        # Add the model to the test_tube
        test_tube.add_model(alt)

        # Set the parameters that are different from the default
        sim_params = c.params()
        sim_params.set_param("defaultVmax", 18.5)
        sim_params.set_param("defaultKm", 0.000015)
        sim_params.set_param("maxCycles", 2100)  # To get a total of 21 hours
        sim_params.set_param("timeStep", 0.01)  # In hours
        sim_params.set_param("spaceWidth", 1)
        sim_params.set_param("maxSpaceBiomass", 10)
        sim_params.set_param("minSpaceBiomass", 1e-11)
        sim_params.set_param("writeMediaLog", True)
        sim_params.set_param("writeFluxLog", True)
        sim_params.set_param("FluxLogRate", 1)

        # Create the experiment
        experiment = c.comets(test_tube, sim_params)

        # Run the simulation
        experiment.run()

        # Save the results
        result_filename = f"{exp_name}_{fba_type}_results.pkl"
        with open(os.path.join(OUT_DIR, result_filename), "wb") as f:
            pickle.dump(experiment, f)
