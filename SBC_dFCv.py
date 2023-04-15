import os
import sys
import numpy as np
import scipy


def np_pearson_corr(x, y):
	# Fast computation for Pearson Correlation Coefficient
	# Credit to:
	# https://cancerdatascience.org/blog/posts/pearson-correlation/
	xv = x - x.mean(axis=0)
	yv = y - y.mean(axis=0)
	xvss = (xv * xv).sum(axis=0)
	yvss = (yv * yv).sum(axis=0)
	result = np.matmul(xv.transpose(), yv) / np.sqrt(np.outer(xvss, yvss))
	# bound the values to -1 to 1 in the event of precision issues
	return np.maximum(np.minimum(result, 1.0), -1.0)


def SBC_dFCv_map(data_ts, seed_ts, w_size, w_step, wHamm):

	# Data expected to be in time (rows) by brain vertex/voxel (cols)

	# Znormalize data
	# Must be done if hamming window is used
	data_ts_znorm = scipy.stats.zscore(data_ts,axis=0)
	seed_ts_znorm = scipy.stats.zscore(seed_ts,axis=0)

	# Exit function if Seed timepoints do not match whole brain data timepoints
	if seed_ts.size != data_ts.shape[0]:
		print("seed and data timepoints do not match")
		print(seed_ts.size)
		print(data_ts.shape[0])
		return None

	# Sliding window parameters:
	#
	# number of timepoints in data
	n_tps = seed_ts.size
	# number of spatial data points in data (i.e. number of voxels or number of CIFTI greyordinates)
	n_pts = data_ts.shape[1]
	# number sliding windows to be computed
	n_window = int((n_tps - w_size)/w_step + 1);
	# window starting timepoint
	start = 0
	# window ending timepoint
	end = w_size
	
	# Create a window using a window function
	if wHamm:
		print("Using hamming window")
		window = np.hamming(w_size)
	else:
		print("Using rectangular window")
		window = np.ones(w_size)
	# Create matrix of windows for windowing of all data points
	data_window = np.tile(window, (n_pts,1)).T
	seed_window = window

	# Output matrix of sliding windows
	SW_data = np.zeros((n_window, n_pts))
	
	for w in range(n_window):
		
		print("Calculating window "+str(w))
		# Window whole brain data
		w_data_ts = data_ts_znorm[start:end]
		w_data_ts = np.multiply(w_data_ts, data_window) 	
	
		# Window seed data
		w_seed_ts = seed_ts_znorm[start:end]
		w_seed_ts = np.multiply(w_seed_ts, seed_window)

		# Compute correlation between seed and whole brain windowed timeseries
		w_corr = np_pearson_corr(w_seed_ts, w_data_ts)

		# Fishers r to z transformation using inverse hyperbolic tangent function
		w_zcorr = np.arctanh(w_corr)
		
		# Store result in sliding windows matrix
		SW_data[w] = w_zcorr

		# Increment window boundaries by window step size
		start=start+w_step
		end=end+w_step
	
	# Compute Standard Deviation across Windows
	dFCv_zcorr = np.std(SW_data, axis=0, ddof=1)
	
	return dFCv_zcorr
	

def gen_SBC_dFCv(data_path, seed_path, out_file, w_size, w_step, wHamm, transpose):
	
	# Read timeseries data from data and seed
	data_ts = np.loadtxt(open(data_path, "rb"), delimiter=",")
	seed_ts = np.loadtxt(open(seed_path, "rb"))

	# transpose data if converted from cifti file
	if transpose:
		data_ts = data_ts.T
	
	dFCv_map = SBC_dFCv_map(data_ts, seed_ts, w_size, w_step, wHamm)

	np.savetxt(out_file, dFCv_map)


# Retrieve arguments
data_path = sys.argv[1]
seed_path = sys.argv[2]
out_file = sys.argv[3]
w_size = int(sys.argv[4])
w_step = int(sys.argv[5])
w_type = sys.argv[6]
doT = sys.argv[7]

if w_type == "Hamm":
	print("Using Hamming Window")
	wHamm = True
elif w_type == "Rect":
	print("Using Rectangular window")
	wHamm = False
else:
	print("Uknown or unsupported window type: "w_type)
	print("Using Rectangular window")
	wHamm = False

if doT == "true":
	transpose=True
else:
	transpose=False

gen_SBC_dFCv(data_path, seed_path, out_file, w_size, w_step, wHamm, transpose)
