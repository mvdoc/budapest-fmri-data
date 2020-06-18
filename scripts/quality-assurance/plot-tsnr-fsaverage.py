import matplotlib.pyplot as plt
import cortex
import numpy as np
from glob import glob

# Run this code to download fsaverage surface for pycortex, labeled by Mark Lescroart
cortex.utils.download_subject(subject_id='fsaverage', download_again=False)

# We are going to compute median tSNR across all runs.
# We already pre-computed it for each subject, so we just need to
# load those files and then compute the median across subjects.
median_tsnr_left = sorted(glob('../../outputs/datapaper/tsnr/sub-*/*median*hemi-L*npy'))
median_tsnr_right = sorted(glob('../../outputs/datapaper/tsnr/sub-*/*median*hemi-R*npy'))

assert len(median_tsnr_left) == 25
assert len(median_tsnr_right) == 25

median_tsnr_both = []
for left, right in zip(median_tsnr_left, median_tsnr_right):
    median_tsnr_both.append(np.hstack((np.load(left), np.load(right))))

median_tsnr_across_subjects = np.median(median_tsnr_both, 0)

# set medial wall values to nan
median_wall = median_tsnr_across_subjects == 0.
median_tsnr_across_subjects[median_wall] = np.nan

surface = cortex.Vertex(median_tsnr_across_subjects, 'fsaverage',
                        vmin=0, vmax=180, cmap='hot');

params = cortex.export.params_inflated_lateral_medial_ventral
windowsize = (1600*2, 900*2)
viewer_params = dict(
    labels_visible=[],
    overlays_visible=[]
)
fig = cortex.export.plot_panels(surface, windowsize=windowsize, viewer_params=viewer_params, **params)
fig.savefig('../../outputs/datapaper/tsnr/figures/group_inflated_median-tsnr-fsaverage-hotcmap.png',
            dpi=300)

fig = cortex.quickflat.make_figure(surface, with_rois=False, with_curvature=True, colorbar_location='right', height=2048)
fig.savefig('../../outputs/datapaper/tsnr/figures/group_flatmap_median-tsnr-fsaverage-hotcmap.png',
            dpi=300)
