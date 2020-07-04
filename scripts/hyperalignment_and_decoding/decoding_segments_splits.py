#!/usr/bin/env python3

## This script performs movie segment classification using 15 s segments,
## similar to Haxby et al. ([2011](https://doi.org/10.1016/j.neuron.2011.08.026))
## and Guntupalli et al. ([2016](https://doi.org/10.1093/cercor/bhw068),
## [2018](https://doi.org/10.1371/journal.pcbi.1006120)).
## Author GUO-Jiahui
## Cloned from: https://github.com/GUO-Jiahui/budapest_hyperalignment

import numpy as np
from scipy.spatial.distance import cdist
from joblib import Parallel, delayed, parallel_backend


def read_in_series(subj, lr, split):
    datadir = f'/datadir/split_{split}'
    if split == 1:
        runs = ['04', '05']
        if lr == 'l':
            dss = np.zeros([598+783, 9372])
        elif lr == 'r':
            dss = np.zeros([598+783, 9370])
        for run in runs:
            ds = np.load(f'{datadir}/{subj}_run-{run}_{lr}h.npy')
            ds = np.nan_to_num(ds)
            if run == '04':
                dss[0:598, :] = ds[15:-5, :]
            elif run == '05':
                dss[598:598+783, :] = ds[15:-5, :]
    elif split == 2:
        runs = ['01', '02', '03']
        if lr == 'l':
            dss = np.zeros([578+478+515, 9372])
        elif lr == 'r':
            dss = np.zeros([578+478+515, 9370])
        for run in runs:
            ds = np.load(f'{datadir}/{subj}_run-{run}_{lr}h.npy')
            ds = np.nan_to_num(ds)
            if run == '01':
                dss[0:578, :] = ds[15:-5, :]
            elif run == '02':
                dss[578:578+478, :] = ds[15:-5, :]
            elif run == '03':
                dss[578+478:578+478+515, :] = ds[15:-5, :]
    return dss

def smooth_data(subj, lr, window_size, split):
    dss = read_in_series(subj, lr, split)
    startpoints = range(len(dss) - window_size + 1)
    dss_smoothed = []
    for startpoint in startpoints:
        strs = range(startpoint, startpoint + window_size)
        dss_smoothed.append(dss[strs, :])
    dss_smoothed = np.array(dss_smoothed)
    return dss_smoothed

def wipe_out_offdiag(mtx, window_size, value=np.inf):
    for rw, _ in enumerate(mtx):
        mtx[rw, max(0, rw - window_size):rw] = value
        mtx[rw, (rw + 1):min(len(mtx), rw + window_size)] = value
    return mtx

def searchlight_classification(dsss, subj, subj_order, lr, window_size, split):
    ds_self = dsss[subj_order, :, :, :]
    ds_temp = np.delete(dsss, subj_order, axis=0)
    ds_others = np.mean(ds_temp, axis=0)
    sls = np.load(f'/sls_dir/fsaverage_{lr}h_10mm.npy')
    ans = np.arange(ds_self.shape[0])
    accs = []
    for sl in sls:
        ds_sf = ds_self[:, :, sl]
        ds_ots = ds_others[:, :, sl]
        ds_sf_rp = ds_sf.reshape(ds_sf.shape[:-2] + (-1,))
        ds_ots_rp = ds_ots.reshape(ds_ots.shape[:-2] + (-1,))
        mtx = cdist(ds_sf_rp, ds_ots_rp, 'correlation')
        mtx_wpt = wipe_out_offdiag(mtx, window_size)
        corrt = np.argmin(mtx_wpt, axis=1)
        acc = (np.sum(corrt == ans))/(ds_self.shape[0])
        accs.append(acc)
    accs = np.array(accs)
    fn_out = f'/fn_out/split_{split}/{subj}_sl_acc_{lr}h.npy'
    np.save(fn_out, accs)

def run_searchlight_classsification(lr, split):
    ffile1 = f'/ffile1/subjects.npy'
    subjects = np.load(ffile1)
    window_size = 15
    jobs = []
    dsss = np.load(f'/fn_out/split_{split}/dsss_{lr}h.npy')
    for subj_order, subj in enumerate(subjects):
        jobs.append(delayed(searchlight_classification)(dsss, subj, subj_order, lr, window_size, split))

    with parallel_backend("loky", inner_max_num_threads=1):
        Parallel(n_jobs=n_jobs)(jobs) # Fill in the actual number of processes allocated

if __name__ == '__main__':
    ## Step 1
    ffile1 = f'/ffile1/subjects.npy'
    subjects = np.load(ffile1)
    window_size = 15
    splits = [1,2]

    for split in splits:
        for lr in 'lr':
            dsss = []
            for subj_order, subj in enumerate(subjects):
                print(subj)
                dss = smooth_data(subj, lr, window_size, split)
                dsss.append(dss)
            dsss = np.array(dsss)
            print(dsss.shape)
            fn_out = f'/fn_out/split_{split}/dsss_{lr}h.npy'
            np.save(fn_out, dsss)

    ## Step 2
    splits = [1,2]
    for split in splits:
        for lr in 'lr':
            run_searchlight_classsification(lr, split)
