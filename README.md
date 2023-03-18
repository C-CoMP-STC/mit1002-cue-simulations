# CUE Simulations

This repository holds the files needed to run FBA simulations and 
calculate/visualize the CUE.

## How to Use the Conda Environment
This repository includes an environment file so that you can re-create
the environment in which all this code was run.

To build and use the environment, make sure Conda is installed and run
```
conda env create --prefix ./env --file environment.yml
conda activate ./env
```

## Organisms
The simulations are grouped by organism:
* `ecoli_core` is the core model that comes with the COBRApy package. It
is a subset of the genome-scale metabolic reconstruction iAF1260 (uses
BiGG notation or reactions/metabolites).
* `ecoli_full` is the genome-scale reconstruction of *E. coli* that
comes with the COBRApy package. It is a reconstruction of iJO1366 (uses
BiGG notation or reactions/metabolites).
* `mit1002_core` is the core model that originally came from Edirisinghe
et al. (2016), and is now being manually curated (uses KBase notation
for reactions/metabolites).
* `mit1002_full` is the genome-scale reconstruction of *A. macleodii*
MIT1002 that was drafted using CarveMe and is now being manually
curated.

