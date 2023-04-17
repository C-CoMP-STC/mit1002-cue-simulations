% run_cobra_and_cafba
%
% This script loads the E. coli model and runs FBA (from the COBRA toolbox)
% and caFBA (from supplementary code from Mori, 2016) for growth on glucose
% alone, acetate alone, and a mix of the two.
%

%% Load the model
% Downloaded this from the BiGG website
model = readCbModel('Ec_iJR904_flux1.xml');

% Get the indices of useful reactions
glcIdx = find(strcmp(model.rxns,'EX_glc_e_'));
o2Idx = find(strcmp(model.rxns,'EX_o2_e_'));
acIdx = find(strcmp(model.rxns, 'EX_ac_e_'));
respIdx = find(strcmp(model.rxns, 'EX_co2_e_'));

% Allow unlimited oxygen uptake
model.lb(o2Idx) = -1000;

%% FBA: Glucose
% Can check all constraints with:
% printConstraints(model, -1000, 1000)

% Limit glucose uptake
model.lb(glcIdx) = -10;

% Perform FBA with maximization of the biomass reaction as the objective
glcSolution = optimizeCbModel(model,'max');

% Visually inspect the fluxes
% fluxData = glcSolution.v;
% nonZeroFlag = 1;
% printFluxVector(model, fluxData, nonZeroFlag)

% Print key reaction fluxes
disp(['EX_glc__D_e: ', int2str(glcSolution.v(glcIdx))])
disp(['EX_ac_e: ', int2str(glcSolution.v(acIdx))])
disp(['EX_co2_e: ', int2str(glcSolution.v(respIdx))])

%% FBA: Acetate
% Set the glucose to 0
model.lb(glcIdx) = 0;

% Set the acetate to 30 (more than glucose because it has 2 carbons)
model.lb(acIdx) = -30;

% Perform FBA with maximization of the biomass reaction as the objective
acSolution = optimizeCbModel(model,'max');

% Print key reaction fluxes
disp(['EX_glc__D_e: ', int2str(acSolution.v(glcIdx))])
disp(['EX_ac_e: ', int2str(acSolution.v(acIdx))])
disp(['EX_co2_e: ', int2str(acSolution.v(respIdx))])

%% FBA: Mix
% Set the glucose to 5
model.lb(glcIdx) = -5;

% Set the acetate to 15
model.lb(acIdx) = - 15;

% Perform FBA with maximization of the biomass reaction as the objective
mixSolution = optimizeCbModel(model,'max');

% Print key reaction fluxes
disp(['EX_glc__D_e: ', int2str(mixSolution.v(glcIdx))])
disp(['EX_ac_e: ', int2str(mixSolution.v(acIdx))])
disp(['EX_co2_e: ', int2str(mixSolution.v(respIdx))])

%% caFBA: Mix
% Remove default bounds for glucose, oxygen, and acetate
model.lb(glcIdx)= -1000;
model.ub(glcIdx) = 1000;
model.lb(acIdx) = -1000;
model.ub(acIdx) = 1000;
model.lb(o2Idx) = -1000;
model.ub(o2Idx) = 1000;

% Knocking out the GLCDe flux
% I don't know what reaction this is supposed to be
% glcd_r=find(strcmp(model.rxns,'GLCDe'));
% model.lb(glcd_r)=0;
% model.ub(glcd_r)=0;

% Add protein groups to model
model=addProteinGroupsToModel(model); % FIXME: Include acetate?

% We now set the offsets for the different groups.
model.protGroup(1).phi0 = 0;
model.protGroup(2).phi0 = 0;
model.protGroup(3).phi0 = 0.066;
model.protGroup(4).phi0 = 0.45;

% Now we have to set the weights for the different groups.
% (note that the function creates the field model.weights if needed)
model=setWeights(model,1,0);
model=setWeights(model,2,0.00083);
model=setWeights(model,3,0.169);
model=setWeights(model,4,0);

% Run caFBA
caFbaSolution = CAFBA_OptimizeCbModel_glpk(model);

% Print key reaction fluxes
disp(['EX_glc__D_e: ', int2str(caFbaSolution.x(glcIdx))])
disp(['EX_ac_e: ', int2str(caFbaSolution.x(acIdx))])
disp(['EX_co2_e: ', int2str(caFbaSolution.x(respIdx))])


%% Save the results