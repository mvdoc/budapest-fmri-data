#!/usr/bin/env python
# coding: utf-8
import numpy as np
import cortex
import os
from glob import glob

data_dir = os.path.abspath('../outputs/fmriprep')


def get_subjects():
    fns = sorted(glob(os.path.join(data_dir, 'sub-*/')))
    fns = [fn.split('/')[-2] for fn in fns]
    return fns

subjects = get_subjects()

data = np.load('../outputs/datapaper/isc/isc-correlations-all-subjects.npy')
data_median = np.median(data, 0)
surfaces = dict()
surfaces['median'] = cortex.Vertex(data_median, 'fsaverage6', cmap='inferno', vmin=0, vmax=0.5)
for subject, dt in zip(subjects, data):
    surfaces[subject] = cortex.Vertex(dt, 'fsaverage6', cmap='inferno', vmin=0, vmax=0.5)

params = cortex.export.params_inflated_lateral_medial_ventral
windowsize = (1600*2, 900*2)
fig = cortex.export.plot_panels(surfaces['median'], windowsize=windowsize,
                                **params)
fig.savefig('../outputs/datapaper/isc/median-isc.png', dpi=300)
