#!/usr/bin/env python2

## This script trains hyperalignment using one half of the movie,
## and applies the transformation matrix to the other half.
## Author: GUO-Jiahui
## Cloned from: https://github.com/GUO-Jiahui/budapest_hyperalignment

import os
from glob import glob
import numpy as np
from scipy.stats import zscore
from nibabel.freesurfer.io import read_geometry

from mvpa2.datasets.base import Dataset
from mvpa2.support.nibabel.surf import Surface
from mvpa2.misc.surfing.queryengine import SurfaceQueryEngine
from mvpa2.algorithms.searchlight_hyperalignment import SearchlightHyperalignment
from mvpa2.base import debug
from mvpa2.base.hdf5 import h5save, h5load


DATA_DIR = '/data_dir/preprocessed_20.1.1'
N_JOBS = n_jobs # Fill in the actual number of processes allocated

MASKS = [np.load('/data_dir/masks/fsaverage_{lr}h_mask.npy'
                 ''.format(lr=lr))
         for lr in 'lr']


def load_dss(lr, runs, subjects):
    mask = {'l': MASKS[0], 'r': MASKS[1]}[lr]
    node_indices = np.where(mask[:10242])[0]

    dss = []
    for subj in subjects:
        ds = []
        for run in runs:
            fn = '{DATA_DIR}/{subj}_run-{run:02d}_space-fsaverage_'\
                 'hemi-{LR}.func.npy'.format(DATA_DIR=DATA_DIR, subj=subj, run=run, LR=lr.upper())
            d = np.load(fn).astype(np.float)
            d = np.nan_to_num(zscore(d, axis=0))
            ds.append(d)
        ds = np.concatenate(ds, axis=0)
        ds = Dataset(ds)
        ds.fa['node_indices'] = node_indices.copy()
        dss.append(ds)
    return dss, node_indices


def load_surface(lr):
    all_coords = []
    for surf_type in ['white', 'pial']:
        coords, faces = read_geometry('/data_dir/freesurfer/'
                                      'subjects/fsaverage/surf/lh.{surf_type}'.format(surf_type=surf_type))
        all_coords.append(coords)
    coords = np.array(all_coords).astype(np.float).mean(axis=0)
    surf = Surface(coords, faces)
    return surf


def load_subj_d(subj, lr, run):
    fn = '{DATA_DIR}/{subj}_run-{run:02d}_space-fsaverage_'\
         'hemi-{LR}.func.npy'.format(DATA_DIR=DATA_DIR, subj=subj, run=run, LR=lr.upper())
    d = np.load(fn).astype(np.float)
    d = np.nan_to_num(zscore(d, axis=0))
    d = Dataset(d)
    return d


if __name__ == '__main__':

    splits = [1,2]
    radius = 15

    fns = glob('{DATA_DIR}/*.npy'.format(DATA_DIR=DATA_DIR))
    subjects = sorted(set([os.path.basename(fn).split('_')[0] for fn in fns]))
    assert len(subjects) == 25

    for lr in 'lr':
        surf = load_surface(lr)
        print(surf)

        for nst, split in enumerate(splits):
            if nst == 0:
                runs = [1,2,3]
            elif nst == 1:
                runs = [4,5]
            dss, node_indices = load_dss(lr, runs, subjects)
            for ds in dss:
                print(ds.shape)

            debug.active += ['SHPAL', 'SLC']
            ha = SearchlightHyperalignment(
                queryengine=SurfaceQueryEngine(surf, radius),
                nproc=N_JOBS,
                nblocks=128,
                compute_recon=False,
                featsel=1.0,
                mask_node_ids=node_indices,
                dtype='float64',
            )

            Ts = ha(dss)
            for T, subj in zip(Ts, subjects):
                out_fn = '/out_fn/split_{split}/{subj}_{lr}h_{radius}_{runs}.hdf5.gz'\
                         ''.format(split=split, subj=subj, lr=lr, radius=radius, runs='-'.join([str(_) for _ in runs]))
                h5save(out_fn, T, compression=9)


    for subj in subjects:
        for lr in 'lr':
            for nst, split in enumerate(splits):
                if nst == 0:
                    runs_1 = [1,2,3]
                    runs_2 = [4,5]
                elif nst == 1:
                    runs_1 = [4,5]
                    runs_2 = [1,2,3]
                h = h5load('/out_fn/split_{split}/{subj}_{lr}h_{radius}_{runs}.hdf5.gz'\
                         ''.format(split=split, subj=subj, lr=lr, radius=radius, runs='-'.join([str(_) for _ in runs_1])))
                for run in runs_2:
                    d = load_subj_d(subj, lr, run)
                    d_hyper = h.forward(d)
                    out_fn_hyper = '/out_fn_hyper/split_{split}_hdata/{subj}_run-{run}_{lr}h.npy'\
                             ''.format(split=split, subj=subj, lr=lr, run=run)
                    np.save(out_fn_hyper, d_hyper)
