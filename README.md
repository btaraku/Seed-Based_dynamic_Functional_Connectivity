# Seed-Based_dynamic_Functional_Connectivity

Requires Python >= 3.6, NumPy, SciPy

Used to compute dynamic Functional Connectivty variability maps (dFCv), given fMRI timeseries data and a seed timeseries. Works directly on CIFTI data
from the Human Connectome Project (HCP)(https://www.humanconnectome.org/software/workbench-command/-cifti-help), by first converting the fMRI
timeseries to text, and running a sliding-window analysis in Python. Python code can be run using any fMRI file type that can be converted to text.
