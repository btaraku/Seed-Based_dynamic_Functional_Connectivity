import numpy as np
import scipy


def np_pearson_corr(x, y):
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
	data_ts_znorm = scipy.stats.zscore(data_ts,axis=0)
	seed_ts_znorm = scipy.stats.zscore(seed_ts,axis=0)

	if seed_ts.size != data_ts.shape[0]:
		print("seed and data timepoints do not match")
		print(seed_ts.size)
		print(data_ts.shape[0])

	# Sliding window parameters
	n_tps = seed_ts.size
	n_pts = data_ts.shape[1]
	n_window = int((n_tps - w_size)/w_step + 1);
	start = 0
	end = w_size
	
	if wHamm:
		print("Using hamming window")
		window = np.hamming(w_size)
	else:
		print("Using rectangular window")
		window = np.ones(w_size)
	data_window = np.tile(window, (n_pts,1)).T
	seed_window = window

	# Output matrix of sliding windows
	SW_data = np.zeros((n_window, n_pts))
	
	for w in range(n_window):
		
		print("Calculating window "+str(w))
		w_data_ts = data_ts_znorm[start:end]
		w_data_ts = np.multiply(w_data_ts, data_window) 	
	
		w_seed_ts = seed_ts_znorm[start:end]
		w_seed_ts = np.multiply(w_seed_ts, seed_window)

		w_corr = np_pearson_corr(w_seed_ts, w_data_ts)

		# Fishers r to z transformation using inverse hyperbolic tangent function
		w_zcorr = np.arctanh(w_corr)
		
		SW_data[w] = w_zcorr

		start=start+1
		end=end+1
	
	# Compute Standard Deviation across Windows
	dFCv_zcorr = np.std(SW_data, axis=0, ddof=1)
	
	return dFCv_zcorr
	

def gen_SBC_dFCv(data_path, seed_path, out_file, w_size, w_step, wHamm=True, transpose=True):
	
	# Read timeseries data from data and seed
	data_ts = np.loadtxt(open(data_path, "rb"), delimiter=",")
	seed_ts = np.loadtxt(open(seed_path, "rb"))

	# transpose data if converted from cifti file
	if transpose:
		data_ts = data_ts.T
	
	dFCv_map = SBC_dFCv_map(data_ts, seed_ts, w_size, w_step, wHamm)

	np.savetxt(out_file, dFCv_map)


