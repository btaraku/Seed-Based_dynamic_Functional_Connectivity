# Seed-Based_dynamic_Functional_Connectivity

Requires Python >= 3.6, NumPy, SciPy

Used to compute dynamic Functional Connectivty variability maps (dFCv), given preprocessed fMRI timeseries data and a seed timeseries. 

Works directly on CIFTI data from the Human Connectome Project (HCP)(https://www.humanconnectome.org/software/workbench-command/-cifti-help), 
which is done by first converting the fMRI timeseries to text, and running a sliding-windows analysis in Python. After running the sliding-windows
analysis, which produces a series of windowed Functional Connectivty (FC) maps using the Pearson Correlation Coefficient, the sample standard 
deviation is calculated across all FC maps to produce dFCv maps. dFCv maps are converted back to CIFTI space using static FC maps as CIFTI template,
calculated using HCP workbench.

Python code can also be run using any fMRI file type that can be converted to text.
