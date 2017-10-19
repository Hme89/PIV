import os
import openpiv.tools
import openpiv.process
import openpiv.scaling


def path(filename):
    "Smart file finder"
    return os.path.join("images/","{}.png".format(filename))


frame_a  = openpiv.tools.imread( path("001") )
frame_b  = openpiv.tools.imread( path("002") )

u, v, sig2noise = openpiv.process.extended_search_area_piv( frame_a, frame_b,
    window_size=24,
    overlap=12,
    dt=0.02,
    search_area_size=64,
    sig2noise_method='peak2peak'
    )
