# SeedBased_dynamic_FC

Python function used to compute dynamic Functional Connectivty variability maps, given fMRI timeseries data and a seed timeseries. Is intented to work
on any imaging file type, and therefore requires the conversion of neuroimaging data to text, such that the fMRI timeseries data is read as a .csv and
the seed timeseries data is read as a .txt. Was initiallly developed to work directly on CIFTI data from the Human Connectome Project (HCP)
(https://www.humanconnectome.org/software/workbench-command/-cifti-help), which can be converted to a .csv using the HCP workbench software.
