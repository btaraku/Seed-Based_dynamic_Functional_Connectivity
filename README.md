# SeedBased_dynamic_FC

A set Python functions used to compute dynamic Functional Connectivty variability maps, given fMRI timeseries data and a seed timeseries. Requires the 
conversion of data to text, such that the fMRI timeseries data is read as a .csv with columns as brain locations and row as timepoints, and the seed 
timeseries data is read as a .txt with a sinlge row of timepoints. This was initiallly developed to work directly on CIFTI data from the Human 
Connectome Project (HCP)(https://www.humanconnectome.org/software/workbench-command/-cifti-help), since this can be converted directly to a .csv and 
then back to CIFTI space using the HCP workbench software (https://www.humanconnectome.org/software/workbench-command/-cifti-convert).
