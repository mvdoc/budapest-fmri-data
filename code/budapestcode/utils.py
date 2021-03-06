"""Module containing utils"""
from numpy.polynomial.legendre import Legendre
import numpy as np
import scipy.linalg as la


def compute_tsnr(data, confounds):
    """Compute tSNR on data by first regressing out the following nuisance
    regressors:

    - six motion parameters and their derivatives
    - global signal
    - framewise displacement
    - six aCompCor components
    - polynomial regressors up to second order

    Parameters
    ----------
    data : array of shape (dim1, dim2, dim3, n_volumes)
        EPI data
    confounds : pandas Dataframe
        dataframe containing confounds generated by fmriprepp
    
    Returns
    ------
    tsnr : array of shape (dim1, dim2, dim3)
        temporal SNR array
    """
    # reshape
    data = data.T
    orig_shape = data.shape
    data = data.reshape(orig_shape[0], -1)
    # store mean
    data_mean = data.mean(0)
    data_clean = clean_data(data, confounds)
    # compute std
    std = data_clean.std(0)
    std[std < 1e-8] = 1
    tsnr = data_mean / std
    # reshape to the original shape
    tsnr = tsnr.reshape(orig_shape[1:]).T
    return tsnr


def make_poly_regressors(n_samples, order=2):
    # mean
    X = np.ones((n_samples, 1))
    for d in range(order):
        poly = Legendre.basis(d + 1)
        poly_trend = poly(np.linspace(-1, 1, n_samples))
        X = np.hstack((X, poly_trend[:, None]))
    return X


def clean_data(data, confounds):
    """Clean data by regressing out the following nuisance regressors:

    - six motion parameters and their derivatives
    - global signal
    - framewise displacement
    - six aCompCor components
    - polynomial regressors up to second order

    Parameters
    ----------
    data : array of shape (n_volumes, n_features)
        flattened EPI data
    confounds : pandas Dataframe
        dataframe containing confounds generated by fmriprepp

    Returns
    -------
    data_clean : array of shape (n_volumes, n_features)
        denoised data
    """
    # make predictor matrix using confounds computed by fmriprep
    columns = [
        'global_signal',
        'framewise_displacement',
        'trans_x', 'trans_x_derivative1',
        'trans_y', 'trans_y_derivative1',
        'trans_z', 'trans_z_derivative1',
        'rot_x', 'rot_x_derivative1',
        'rot_y', 'rot_y_derivative1',
        'rot_z', 'rot_z_derivative1',
    ]
    # compcor
    n_comp_cor = 6
    columns += [f"a_comp_cor_{c:02d}" for c in range(n_comp_cor)]
    X = confounds[columns].values
    # remove nans
    X[np.isnan(X)] = 0.
    # add polynomial components
    n_samples = X.shape[0]
    X = np.hstack((X, make_poly_regressors(n_samples, order=2)))

    # time to clean up
    # center the data first and store the mean
    data_mean = data.mean(0)
    data = data - data_mean
    coef, _, _, _ = la.lstsq(X, data)
    # remove trends and add back mean of the data
    data_clean = data - X.dot(coef) + data_mean
    return data_clean
