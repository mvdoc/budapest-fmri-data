"""Module containing viz utils"""
import numpy as np


def make_mosaic(data):
    """Reshape data into a mosaic plot
    
    Parameters
    ---------
    data : array of shape (dim1, dim2, 58)
        input volume (it assumes that it has 58 slices)

    Returns
    ------
    mosaic : array of shape (6 * dim1, 10 * dim2)
        mosaic matrix that can be plotted with matshow
    """
    # add an extra slice top and bottom
    dim1, dim2, dim3 = t.shape
    empty_slice = np.zeros((dim1, dim2, 1))
    t = np.concatenate((empty_slice, t, empty_slice), -1)
    # split into 6 rows
    t = np.split(t, 6, -1)
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
