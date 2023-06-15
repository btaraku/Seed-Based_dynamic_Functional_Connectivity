# Seed-Based_dynamic_Functional_Connectivity

Requires Python >= 3.6, NumPy, SciPy

Used to compute dynamic Functional Connectivty variability (dFCv) maps, given preprocessed fMRI timeseries data and a seed timeseries. dFCv is defined
as the standard deviation of windowed Seed-Based Functional Connectivty maps, calculated from a sliding-windows analysis.

dFCv used in fMRI research: https://onlinelibrary.wiley.com/doi/epdf/10.1002/hbm.23910

Reference for how Dynamic FC measures are calculated: https://web.conn-toolbox.org/fmri-methods/connectivity-measures/dynamic-connectivity

Expects preprocessed fMRI data from the HCP Minimal Preprocessing Pipeline and a seed timeseries

Works directly on CIFTI data from the Human Connectome Project (HCP)(https://www.humanconnectome.org/software/workbench-command/-cifti-help), 
which is done by first converting the fMRI timeseries to text, and running a sliding-windows analysis in Python. After running the sliding-windows
analysis, which produces a series of windowed Functional Connectivty (FC) maps using the Pearson Correlation Coefficient, the sample standard 
deviation is calculated across all FC maps to produce dFCv maps. dFCv maps are converted back to CIFTI space using static FC maps as CIFTI template,
calculated using HCP workbench.

Python code can also be run using any fMRI file type that can be converted to text.

Inspired by code from the DPABI toolbox https://rfmri.org/dpabi (Temporal Dynamics Analysis)
