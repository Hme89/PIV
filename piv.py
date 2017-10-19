from src import OpenPIV as piv

# name of frames saved in images-folder
frame_a = "56"
frame_b = "58"

# Initial field settings
window_size = 24
overlap = 12
dt = 0.02
search_area_size = 64
sig2noise_method ='peak2peak'

# Mask settings
threshold = 1.3

# Replace outliers settings
method='localmean'
kernel_size=2


x,y,u,v,sig2n = piv.field(frame_a, frame_b, window_size, overlap, dt, search_area_size, sig2noise_method)
piv.plot_mpl(x,y,u,v,131)

u, v, mask = piv.mask( u, v, sig2n, threshold  )
piv.plot_mpl(x,y,u,v,132)

u, v = piv.replace_outliers( u, v, method, kernel_size)
piv.plot_mpl(x,y,u,v,133)

piv.plot_show()
