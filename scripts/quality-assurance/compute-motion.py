#!/usr/bin/env python
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from glob import glob


def load_add_idx(sub_fns, sub_idx):
    dfs = []
    for i, fn in enumerate(sub_fns):
        df = pd.read_csv(fn, sep='\t', skiprows=[1])
        df['subject'] = sub_idx
        df['run'] = i+1
        dfs.append(df)
    return dfs


def extract_columns(dfs):
    keep_columns = [
    'framewise_displacement',
    'rot_x', 'rot_y', 'rot_z',
    'trans_x', 'trans_y', 'trans_z'
    ,'subject', 'run']
    
    dfs = [df[keep_columns] for df in dfs]
    return pd.concat(dfs)


def all_sub_cols(fns, subjects):
    all_df = []
    median_fd = []
    for s in subjects:
        sub_files = [fn for fn in fns if s in fn]
        dfs = load_add_idx(sub_files, s)
        dfs_cols = extract_columns(dfs)
        all_df.append(dfs_cols)
        
    return all_df


def plot_one_sub(df, sids, col, outdir):
    
    for sid in sids:
        print("Plotting {0} for {1}".format(col, sid))
        sub_df = df[df.subject == sid]
        to_plot = [sub_df[sub_df.run == r][col].values for r in range(1,6)]
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        pos =[1, 2, 3, 4, 5]
        parts = ax.violinplot(to_plot, positions=pos, showmedians=True);
        for pc in parts['bodies']:
            pc.set_facecolor('gray')
            pc.set_edgecolor('black')
            pc.set_alpha(0.5)

        for p in ['cbars', 'cmins', 'cmaxes', 'cmedians']:
            parts[p].set_edgecolor('black')

        ax.set_xticks(pos)
        ax.set_xticklabels(['run-{}'.format(r) for r in range(1,6)], fontsize=12, ha='right')
        ax.set_ylabel('{0} for {1}'.format(col, sid), fontsize=12)
        plt.tight_layout()
        
        
        outfile = os.path.join(outdir, '{0}_{1}-violinplot.png'.format(sid, col))
        print("saving...")
        fig.savefig(outfile, dpi=300, bbox_inches='tight')



def plot_all_sub_med(df, sids, col, outdir):
    fig, ax = plt.subplots(1, 1, figsize=(18, 6))
    pos = np.arange(len(sids))

    parts = ax.violinplot(df, positions=pos, showmedians=True);
    for pc in parts['bodies']:
        pc.set_facecolor('gray')
        pc.set_edgecolor('black')
        pc.set_alpha(0.5)

    for p in ['cbars', 'cmins', 'cmaxes', 'cmedians']:
        parts[p].set_edgecolor('black')

    ax.set_xticks(pos)
    ax.set_xticklabels(sids, fontsize=16, rotation=45, ha='right')
    if col == 'framewise_displacement':
        ylabel = 'Framewise Displacement [mm]'
        ax.axhline(0.5, color='lightgray', linestyle='dashed', zorder=0)
    else:
        ylabel = col
    ax.set_ylabel(ylabel, fontsize=16)
    sns.despine()
    plt.tight_layout()
    outfile = os.path.join(outdir, 'group_median-{}.png'.format(col))
    print("saving...")
    fig.savefig(outfile, dpi=300, bbox_inches='tight')
    


def main():
    indir = '../../outputs/fmriprep'
    outdir = '../../outputs/datapaper/motion/figures'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    fns = sorted(glob(f'{indir}/*/func/*tsv'))
    subjects = [path.split('/')[-1].split('_')[0] for path in fns]
    subjects = sorted(list(set(subjects)))
    dfs = all_sub_cols(fns, subjects)
    
    for col in ['framewise_displacement', 'rot_x', 'rot_y', 'rot_z']:
        print("Working on {}".format(col))
        df_plot = [df[col].values for df in dfs]
        print("Plotting {} for the group".format(col))
        plot_all_sub_med(df_plot, subjects, col, outdir)
        # print("Now plotting {} for each subject".format(col))
        # plot_one_sub(pd.concat(dfs), subjects, col, outdir)
        

if __name__ == '__main__':
    main()
