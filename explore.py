import numpy as np
import gzip, pickle

#Solution file
path = "solution_20VOL.pcl.gz"

with gzip.open(path, "rb") as infile:
    data = pickle.loads(infile.read())

for sol in data:
    # print(sol[0])
    print(np.nanmax(sol[0]))
