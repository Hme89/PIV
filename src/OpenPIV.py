import os
import openpiv.tools
import openpiv.process
import openpiv.scaling
import openpiv.validation
import openpiv.filters

import numpy as np
import matplotlib.pyplot as plt

import plotly as ply
import plotly.figure_factory as ff

def read_image(filename):
    "Smart file finder"
    path = os.path.join("images/","{}.png".format(filename))
    return openpiv.tools.imread(path).astype(np.int32)

def plot_mpl(x,y,u,v,sub):
    plt.subplot(sub)
    plt.quiver(x,y,u,v)

def plot_ply(x,y,u,v,sub):
    fig = ff.create_quiver(x,y,u,v,sub)
    ply.offline.plot(fig, filename="images/plot1.html")

def field(frame_a, frame_b, window_size, overlap, dt, search_area_size, sig2noise_method):
    frame_a  = read_image(frame_a)
    frame_b  = read_image(frame_b)

    print("Shape A: ",frame_a.shape)
    print("Shape B: ",frame_b.shape)

    assert frame_a.shape == frame_b.shape

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

    assert len(set( [i.shape for i in [x,y,u,v]] )) == 1

    return x, y, u, v, sig2noise


def mask(u, v, sig2noise, threshold=1.3):
    u, v, mask = openpiv.validation.sig2noise_val( u, v, sig2noise, threshold=threshold)
    return u, v, mask

def replace_outliers(u, v, method="localmean", kernel_size=2):
    u, v = openpiv.filters.replace_outliers( u, v, method=method, kernel_size=kernel_size)
    return u, v

def plot_show():
    plt.show()
