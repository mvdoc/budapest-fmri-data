#!/usr/bin/env python
# coding: utf-8
import numpy as np
import cortex
import os
from glob import glob

data_dir = os.path.abspath('../../outputs/fmriprep')


def get_subjects():
    fns = sorted(glob(os.path.join(data_dir, 'sub-*/')))
    fns = [fn.split('/')[-2] for fn in fns]
    return fns

subjects = get_subjects()

data = np.load('../../outputs/datapaper/isc/isc-correlations-all-subjects-fsaverage.npy')
data_median = np.median(data, 0)
# surfaces = dict()
surface = cortex.Vertex(data_median, 'fsaverage', cmap='hot', vmin=0, vmax=0.5)
# for subject, dt in zip(subjects, data):
#     surfaces[subject] = cortex.Vertex(dt, 'fsaverage', cmap='inferno', vmin=0, vmax=0.5)

params = cortex.export.params_inflated_lateral_medial_ventral
windowsize = (1600*2, 900*2)
viewer_params = dict(
    labels_visible=[],
    overlays_visible=[]
)
fig = cortex.export.plot_panels(surface, windowsize=windowsize, viewer_params=viewer_params, **params)
fig.savefig('../../outputs/datapaper/isc/median-isc-fsaverage-hotcmap.png',
            dpi=300)

fig = cortex.quickflat.make_figure(surface, with_rois=False, colorbar_location='right', height=2048)
fig.savefig('../../outputs/datapaper/isc/flatmap_median-isc-fsaverage-hotcmap.png',
            dpi=300)
