#!/usr/bin/env python
import os
import sys

import matplotlib.pyplot as plt
import nibabel as nib
import nilearn.image as nimage
import numpy as np
import pandas as pd
import seaborn as sns
import scipy.linalg as la

from glob import glob

from budapestcode.utils import compute_tsnr
from budapestcode.viz import make_mosaic, plot_mosaic

if len(sys.argv) < 2:
    print(f"Usage: {os.path.basename(__file__)} subject_id")
    sys.exit(1)

subject = sys.argv[1]
if not subject.startswith('sub-'):
    subject = f'sub-{subject}'

HERE = os.path.dirname(__file__)

OUTPUT_DIR = os.path.abspath(os.path.join(HERE, '../../outputs'))
INDIR = f"{OUTPUT_DIR}/fmriprep"
OUTDIR = f"{OUTPUT_DIR}/datapaper/tsnr"

func_fns = sorted(glob(f'{INDIR}/{subject}/func/*space-fsaverage_hemi-*_bold.func.gii'))
conf_fns = sorted(glob(f'{INDIR}/{subject}/func/*tsv'))
conf_fns = sorted(conf_fns * 2)  # we have both L,R hemispheres

assert len(func_fns) == 10

# compute tSNR for every run
tsnr_runs = []
print("Computing tSNR")
for f, c in zip(func_fns, conf_fns):
    print(f"  {f.split('/')[-1]}")
    data = nib.load(f)
    data = np.vstack([d.data for d in data.darrays])
    conf = pd.read_csv(c, sep='\t')
    # mask data removing the medial wall
    mask_medial_wall = data.std(0) != 0.
    data = data[:, mask_medial_wall].T  # transpose because of compute_tsnr
    tsnr = compute_tsnr(data, conf)
    tsnr_ = np.zeros_like(mask_medial_wall, dtype=np.float)
    tsnr_[mask_medial_wall] = tsnr
    tsnr_runs.append(tsnr_)

# compute median tsnr
tsnr_median_l = np.median(tsnr_runs[::2], 0)
tsnr_median_r = np.median(tsnr_runs[1::2], 0)

# finally store the tSNR data so we can do group analyses
tsnr_tosave = tsnr_runs + [tsnr_median_l, tsnr_median_r]
run_types = [f'{i:02d}' for i in range(1, 6)] + ['median']
# make filenames
fnouts = []
for run_type in run_types:
    for hemi in ['L', 'R']:
        fnout = f'{subject}_task-movie_run-{run_type}_space-fsaverage_hemi-{hemi}_desc-tsnr.npy'
        fnouts.append(fnout)


OUTDIR = f"{OUTDIR}/{subject}"
os.makedirs(OUTDIR, exist_ok=True)

for fnout, t in zip(fnouts, tsnr_tosave):
    print(fnout)
    fnout = f"{OUTDIR}/{fnout}"
    np.save(fnout, t)
