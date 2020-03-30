"""Module containing viz utils"""
import numpy as np
import matplotlib.pyplot as plt


def make_mosaic(data):
    """Reshape data into a mosaic plot
    
    Parameters
    ---------
    data : array of shape (dim1, dim2, dim3)
        input volume

    Returns
    ------
    mosaic : array
        mosaic matrix that can be plotted with matshow
    """
    # add extra slices top and bottom to make it divisible by 6
    dim1, dim2, dim3 = data.shape
    empty_slice = np.zeros((dim1, dim2, 1))
    n_cols = 10
    n_rows = int(np.ceil(dim3/n_cols))
    n_extra_slices = n_cols*n_rows - dim3
    n_extra_slices_half = n_extra_slices // 2
    to_concat = [empty_slice] * n_extra_slices_half
    to_concat += [data]
    to_concat += [empty_slice] * n_extra_slices_half
    if n_extra_slices % 2 != 0:
        to_concat += [empty_slice]
    t = np.concatenate(to_concat, -1)
    assert t.shape[-1] == n_cols * n_rows
    # split into rows
    t = np.split(t, n_rows, -1)
    # make matrix with some magic
    t = np.vstack([tt.transpose(1, 0, 2).reshape(dim2, -1, order='F') for tt in t])
    # change order so that plots match standard mosaic order
    t = t[::-1, ::-1]
    return t


from mpl_toolkits.axes_grid1 import make_axes_locatable 


def plot_mosaic(mat, vmin=30, vmax=250, title=None):
    fig, ax = plt.subplots(1, 1, figsize=(18, 18))
    im = ax.matshow(mat, vmin=vmin, vmax=vmax, interpolation='nearest', cmap='inferno')
    if title:
        ax.text(0, 0, title, ha='left', va='top', fontsize=24, bbox=dict(facecolor='white', alpha=1))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="1%", pad=0.05)
    plt.colorbar(im, cax=cax)
    ax.axis('off')
    return fig
