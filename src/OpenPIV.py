import sys, os
import openpiv.tools
import openpiv.process
import openpiv.scaling
import openpiv.validation
import openpiv.filters

import numpy as np
import matplotlib.pyplot as plt

import plotly as ply
import plotly.figure_factory as ff

def read_array(path, filename):
    filepath = os.path.join(path, filename,)
    return np.fromfile(filepath, dtype=np.int16).reshape(1024,1024).astype(np.int32)

def cut_array(a, cut):
    x0 = cut[0][0]; x1 = cut[0][1]
    y0 = cut[1][0]; y1 = cut[1][1]
    return a[x0:x1, y0:y1]

def imshow(img, sub=111):
    plt.subplot(sub)
    plt.imshow(img, cmap="binary_r")

def plot_mpl(x,y,u,v,sub):
    plt.subplot(sub)
    plt.quiver(x,y,u,v)


def plot_ply(x,y,u,v,sub):
    fig = ff.create_quiver(x,y,u,v,sub)
    ply.offline.plot(fig, filename="images/plot1.html")


def field(path, a, b, cut, window_size, overlap, dt, search_area_size, sig2noise_method, cutoff=None):

    frame_a  = cut_array(read_array(path, a), cut)
    frame_b  = cut_array(read_array(path, b), cut)

    # frame_a  = openpiv.tools.imread( '/home/hme/Sandbox/exp1_001_a.bmp' ).astype(np.int32)
    # frame_b  = openpiv.tools.imread( '/home/hme/Sandbox/exp1_001_b.bmp' ).astype(np.int32)

    assert frame_a.shape == frame_b.shape
    print("Shape of frames: ",frame_a.shape)

    u, v, sig2noise = openpiv.process.extended_search_area_piv( frame_a, frame_b,
        window_size=window_size,
        overlap=overlap,
        dt=dt,
        search_area_size=search_area_size,
        sig2noise_method=sig2noise_method
        )

    x, y = openpiv.process.get_coordinates(
        image_size=frame_a.shape,
        window_size=window_size,
        overlap=overlap
        )

    if cutoff:
        cutoff(u, v, cutoff)

    assert len(set( [i.shape for i in [x,y,u,v]] )) == 1

    return x, y, u, v, sig2noise, frame_a, frame_b


def mask(u, v, sig2noise, threshold=1.3):
    u, v, mask = openpiv.validation.sig2noise_val( u, v, sig2noise, threshold=threshold)
    return u, v, mask

def replace_outliers(u, v, method="localmean", kernel_size=2):
    u, v = openpiv.filters.replace_outliers( u, v, method=method, kernel_size=kernel_size)
    return u, v

def scale(x, y, u, v, scaling_factor):
    return openpiv.scaling.uniform(x,y,u,v,scaling_factor = scaling_factor)

def cutoff(u, v, cut):
    n = 0
    assert u.shape == v.shape
    shp = u.shape
    for i in range(shp[0]):
        for j in range(shp[1]):
            if (u[i,j]**2 + v[i,j]**2)**0.5 > cut:
                u[i,j] = 0
                v[i,j] = 0
                n += 1
    print("{} values over {} cut from solution arrays...".format(n, cut) )


def plot_show():
    plt.show()

def plot_save(fname="img", format="pdf"):
    plt.savefig("images/{:0>3}.pdf".format(fname))
    plt.clf()
