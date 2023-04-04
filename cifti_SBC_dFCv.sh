#!/bin/bash

### Inputs ###
# datadir: directory where resting-state fMRI timeseries can be found
# filename: name of fMRI file to be analyzed
# seed_ts: location of where seed timeseries data can be found
# 	Expects to find seed timeseries in both .txt and .sdseries.nii
# outdir: location of where outputs are saved
# fc_outname: name of static FC map to be saved
# dfcv_outname: name of dFCv map to be saved
# Wsize: window size in TRs
# Wstep: window step size parameter in TRs
# Wtype: type of window function: Currently only supports 2 options:
# 	Rectangular window: "Rect"
# 	Hamming window: "Hamm"

datadir=$1
filename=$2
seed_ts=$3
outdir=$4
fc_outname=$5
dfcv_outname=$6
Wsize=$7
Wstep=$8
Wtype=$9

# Run standard correlation to get static FC maps
echo "Running cifti cross correlation"
wb_command -cifti-cross-correlation ${datadir}${filename}.dtseries.nii ${seed_ts}.sdseries.nii ${outdir}${fc_outname}.dscalar.nii -fisher-z

# Convert cifti to text
echo "converting cifti to csv"
rm ${outdir}${filename}.csv
wb_command -cifti-convert -to-text ${datadir}${filename}.dtseries.nii ${outdir}${filename}.csv -col-delim ","

# Run dFCv python script
echo "running sliding-window analysis in python"
python SBC_dFCv.py ${outdir}${filename}.csv ${seed_ts}.txt ${outdir}${dfcv_outname}.txt $Wsize $Wstep $Wtype "true"

# Convert text file back to cifti space using FC map as reference
echo "converting back to cifti space"
wb_command -cifti-convert -from-text ${outdir}${dfcv_outname}.txt ${outdir}${fc_outname}.dscalar.nii ${outdir}${dfcv_outname}.dscalar.nii

