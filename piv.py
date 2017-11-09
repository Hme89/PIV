#!bin/python
from src import OpenPIV as piv
import numpy as np
import os
import pickle

path = "/run/user/1000/gvfs/sftp:host=casey,user=sftp/PIV/9_november/Kamera_test_1_20k_fps_25%/Bilder_til_henrik/C001H001S0001/"

# Initial field settings
scaling_factor = 8000
window_size = 48
overlap = 24
dt = 19e-6

# search_area_size = int(window_size*1.3)
# search_area_size = window_size
search_area_size = 128
sig2noise_method ='peak2peak'

# Mask settings
threshold = 1.3

# Replace outliers settings
method='localmean'
kernel_size = 1

# Cut starting from x0, ending at x1: [[x0,x1],...]
cut = [[0,-1],[0,-1]]

# Cutoff params
cutoff = None

files = [ f for f in os.listdir(path) if "C001" not in f]
files.sort()

solutions = []
for i in range(0, len(files) - 1, 2):
    sol = []
    a = files[i]
    b = files[i + 1]
    print("\nMatching files {} and {}...".format(files[i],files[i+1]) )

    # piv.cutoff(u,v, cutoff)

    x,y,u,v,sig2n,a,b = piv.field(path, a, b, cut, window_size, overlap, dt,
        search_area_size, sig2noise_method, cutoff=cutoff)
    piv.imshow(a)
    piv.plot_save("img_{:0>2}".format(i))
    # piv.plot_show()
    # piv.imshow(a,141)search_area_size = window_size

    # piv.plot_mpl(x,y,u,v,142)
    piv.plot_mpl(x,y,u,v,131)

    u, v, mask = piv.mask( u, v, sig2n, threshold )
    # piv.plot_mpl(x,y,u,v,143)
    piv.plot_mpl(x,y,u,v,132)

    u, v = piv.replace_outliers( u, v, method, kernel_size)
    # piv.plot_mpl(x,y,u,v,144)
    piv.plot_mpl(x,y,u,v,133)


    x,y,u,v = piv.scale(x,y,u,v,scaling_factor)

    solutions.append([u,v,x,y,a,b])

    # piv.plot_mpl(x,y,u,v,111)
    piv.plot_save(i)
    # piv.plot_show()

with open('data.pcl', 'wb') as f:
    pickle.dump(solutions, f, pickle.HIGHEST_PROTOCOL)

for sol in solutions:
    a = (sol[0]**2 + sol[1]**2)**0.5
    print("max:",np.nanmax(a))
