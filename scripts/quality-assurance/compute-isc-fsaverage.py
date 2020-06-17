#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
from glob import glob
import numpy as np
import nibabel as nib
import os
import pandas as pd
import scipy.linalg as la

from budapestcode.utils import clean_data

# Process is
# 1. Load runs
# 2. Clean up signal
# 3. zscore runs
# 4. stack
# 5. compute isc

data_dir = os.path.abspath('../../outputs/fmriprep')


def load_gifti(fn):
    data = nib.load(fn)
    data = np.vstack([d.data for d in data.darrays])
    return data


def get_subjects():
    fns = sorted(glob(os.path.join(data_dir, 'sub-*/')))
    fns = [fn.split('/')[-2] for fn in fns]
    return fns


def load_data(subject):
    print(f"Loading data for subject {subject}")
    datadir = f"{data_dir}/{subject}/func"
    data = []
    for irun in range(1, 6):
        data_ = []
        for hemi in ['L', 'R']:
            print(f"  run{irun:d}, hemi-{hemi}")
            fn = f"{subject}_task-movie_run-{irun:d}_space-fsaverage_hemi-{hemi}_bold.func.gii"
            data_.append(load_gifti(os.path.join(datadir, fn)))
        data.append(np.hstack(data_))
    return data


def load_confounds(subject):
    datadir = f"{data_dir}/{subject}/func"
    confounds = []
    confounds_fn = sorted(glob(f'../../outputs/fmriprep/{subject}/func/*tsv'))
    for conf in confounds_fn:
        print(conf.split('/')[-1])
        confounds.append(pd.read_csv(conf, sep='\t'))
    return confounds


def zscore(array):
    array -= array.mean(0)
    array /= (array.std(0) + 1e-8)
    return array


subjects = get_subjects()
print(len(subjects))

data = []
for subject in subjects:
    data_subject = load_data(subject)
    confounds = load_confounds(subject)
    data_subject = np.vstack(
        [zscore(clean_data(dt, conf)) 
         for dt, conf in zip(data_subject, confounds)]
    )
    data.append(data_subject)


def fast_mean(list_of_arrays):
    mean = np.zeros_like(list_of_arrays[0])
    for array in list_of_arrays:
        mean += array
    mean /= len(list_of_arrays)
    return mean


correlations = []
n_subjects = len(subjects)
n_samples = data[0].shape[0]

for isubject, subject in enumerate(subjects):
    mask_group = np.ones(n_subjects, dtype=bool)
    mask_group[isubject] = False
    mask_group = np.where(mask_group)[0]
    print(f"{subject}: {isubject}, group: {mask_group}")
    data_subject = data[isubject].copy()
    data_group = fast_mean([data[i] for i in mask_group])
    # compute columnwise correlation
    corr = (zscore(data_subject) * zscore(data_group)).sum(0) / n_samples
    correlations.append(corr)

correlations = np.array(correlations)

DIROUT = '../../outputs/datapaper/isc'
os.makedirs(DIROUT, exist_ok=True)
np.save(f'{DIROUT}/isc-correlations-all-subjects-fsaverage.npy', correlations)

