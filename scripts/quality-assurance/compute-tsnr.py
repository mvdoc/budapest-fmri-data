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

func_fns = sorted(glob(f'{INDIR}/{subject}/func/*space-T1w_desc-preproc_bold.nii.gz'))
conf_fns = sorted(glob(f'{INDIR}/{subject}/func/*tsv'))

# compute tSNR for every run
tsnr_runs = []
print("Computing tSNR")
for f, c in zip(func_fns, conf_fns):
    print(f"  {f.split('/')[-1]}")
    data = nib.load(f).get_fdata()
    conf = pd.read_csv(c, sep='\t')
    tsnr_runs.append(compute_tsnr(data, conf))

# make mosaics
mosaic_runs = [make_mosaic(t) for t in tsnr_runs]
# compute median tsnr
tsnr_median = np.median(tsnr_runs, 0)
mosaic_median_run = make_mosaic(tsnr_median)


IMGOUT = f'{OUTDIR}/figures/{subject}'
os.makedirs(IMGOUT, exist_ok=True)

# Save images
print("Saving images")
for i, mat in enumerate(mosaic_runs, 1):
    fig = plot_mosaic(mat, vmin=0, vmax=150, title=f'{subject}: run {i}');
    plt.tight_layout()
    fnout = f'{subject}_tsnr-mosaic_run-{i:02d}.png'
    print(fnout)
    fig.savefig(f'{IMGOUT}/{fnout}', dpi=150, bbox_inches='tight')
# median
fnout = f'{subject}_tsnr-mosaic_run-median.png'
print(fnout)
fig = plot_mosaic(mosaic_median_run, vmin=0, vmax=150, title=f'{subject}: median tSNR');
fig.savefig(f'{IMGOUT}/{fnout}', dpi=150, bbox_inches='tight')


# Now make violinplot
# first compute a conjuction brain mask
mask_fns = sorted(glob(f'{INDIR}/{subject}/func/*space-T1w_desc-brain_mask.nii.gz'))

# make a conjuction mask
brainmask = np.ones_like(tsnr_runs[0])
for mask_fn in mask_fns:
    bm = nib.load(mask_fn).get_fdata()
    brainmask *= bm
# plot it
mat_brainmask = make_mosaic(brainmask)
fig = plot_mosaic(mat_brainmask, vmin=0, vmax=1, title='Conjuction brainmask');
fnout = f'{subject}_brainmask-conjunction.png'
print(fnout)
fig.savefig(f'{IMGOUT}/{fnout}', dpi=150, bbox_inches='tight')

# mask the runs
tsnr_runs_masked = [t[brainmask.astype(bool)] for t in tsnr_runs]
# compute median
tsnr_median_masked = np.median(tsnr_runs_masked, 0)
tsnr_runs_masked.append(tsnr_median_masked)

# make a pretty plot please
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
pos =[0, 1, 2, 3, 4, 5.5]
parts = ax.violinplot(tsnr_runs_masked, positions=pos, showmedians=True);
for pc in parts['bodies']:
    pc.set_facecolor('gray')
    pc.set_edgecolor('black')
    pc.set_alpha(0.5)

for p in ['cbars', 'cmins', 'cmaxes', 'cmedians']:
    parts[p].set_edgecolor('black')

ax.set_xticks(pos)
ax.set_xticklabels([f"Run {i}" for i in range(1, 6)] + ['Median tSNR'], fontsize=12)
ax.set_ylabel('tSNR', fontsize=12)
ax.set_title(subject, fontsize=14)
sns.despine()
plt.tight_layout()

fnout = f'{subject}_tsnr-violinplot.png'
print(fnout)
fig.savefig(f'{IMGOUT}/{fnout}', dpi=150, bbox_inches='tight')

# finally store the tSNR data so we can do group analyses
tsnr_tosave = tsnr_runs + [tsnr_median]
run_types = [f'{i:02d}' for i in range(1, 6)] + ['median']

OUTDIR = f"{OUTDIR}/{subject}"
os.makedirs(OUTDIR, exist_ok=True)

for run, t in zip(run_types, tsnr_tosave):
    t_img = nimage.new_img_like(func_fns[0], t)
    fnout = f'{subject}_task-movie_run-{run}_space-T1w_desc-tsnr.nii.gz'
    print(fnout)
    fnout = f"{OUTDIR}/{fnout}"
    t_img.to_filename(fnout)
