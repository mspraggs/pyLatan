import os

import h5py
import numpy as np


def read_hdf5_sample(filename):
    """Read LatAnalyze3 HDF5 sample file"""
    i = -1
    if not os.path.exists(filename):
        raise IOError("No such file: {}".format(filename))
    f = h5py.File(filename)
    outer_groupname = f.keys()[0]
    outer_group = f[outer_groupname]
    num_samples = outer_group.attrs['nSample'][0]

    while i < num_samples:
        key = "data_C" if i < 0 else 'data_S_{}'.format(i)
        ret = outer_group[key].value
        yield ret.reshape(ret.shape[::-1])
        i += 1

def read_hdf5_samples(filename):
    """Read hdf5 samples from file, returning centre and samples"""
    data = list(read_hdf5_sample(filename))
    return data[0], data[1:]

def read_hdf5_to_numpy(filename):
    """Read hdf5 samples from file and return them as ndarray"""
    if not os.path.exists(filename):
        raise IOError("No such file: {}".format(filename))
    f = h5py.File(filename)
    outer_groupname = f.keys()[0]
    outer_group = f[outer_groupname]
    num_samples = outer_group.attrs['nSample'][0]

    centre = outer_group["data_C"].value

    ret = np.zeros((num_samples + 1,) + centre.shape[::-1],
                   dtype=centre.dtype)
    ret[-1] = centre.reshape(centre.shape[::-1])
    
    for i in range(num_samples):
        key = "data_C" if i == -1 else "data_S_{}".format(i)
        data = outer_group[key].value
        ret[i] = data.reshape(data.shape[::-1])

    return ret

