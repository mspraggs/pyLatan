import os
import warnings

import h5py
import numpy as np


warnings.simplefilter('always')

def _extract_samples(group, num_samples):
    """Loop through samples in group and build the associated numpy array"""

    centre = group["data_C"].value
    ret = np.zeros((num_samples + 1,) + centre.shape[::-1],
                   dtype=centre.dtype)
    ret[-1] = centre.reshape(centre.shape[::-1])

    for i in range(num_samples):
        key = "data_C" if i == -1 else "data_S_{}".format(i)
        data = group[key].value
        ret[i] = data.reshape(data.shape[::-1])

    return ret

def _common_hdf5_loading(filename):
    """Common code for loading group and file from HDF5 file"""

    if not os.path.exists(filename):
        raise IOError("No such file: {}".format(filename))

    f = h5py.File(filename)
    outer_groupname = f.keys()[0]
    outer_group = f[outer_groupname]
    num_samples = outer_group.attrs['nSample'][0]
    datatype = outer_group.attrs['type'][0]

    return outer_group, num_samples, datatype


def load_hdf5_legacy(filename):
    """Read v3.0 hdf5 samples from file and return them as a numpy ndarray.

    Args:
      filename (str): Path to the hdf5 file to open.

    Returns:
      numpy.ndarray: First dimension is length num_samples + 1.

      The first num_samples slices are the various bootstrap samples, the last
      slice is the central value.
    """

    warnings.warn("LatAnalyze 3.0 file formats are no longer supported. "
                  "Please convert your sample file if possible.",
                  DeprecationWarning)

    outer_group, num_samples, datatype = _common_hdf5_loading(filename)
    return _extract_samples(outer_group, num_samples)


def load_hdf5(filename):
    """Load hdf5 data from file and return it as a numpy ndarray.

    Args:
      filename (str): Path to the hdf5 file to open.

    Returns:
      numpy.ndarray: The samples or other data stored in the given file.

      For sample data, the first num_samples slices are the various bootstrap
      samples, the last slice is the central value.
    """
    if not os.path.exists(filename):
        raise IOError("No such file: {}".format(filename))

    outer_group, num_samples, datatype = _common_hdf5_loading(filename)

    if datatype not in [1, 2, 3]:
        raise IOError("Unknown datatype information. Try loading with "
                      "load_hdf5_legacy, or convert your input file.")

    if datatype == 1:
        return outer_group["data"][()]

    elif datatype == 2:
        return _extract_samples(outer_group, num_samples)

    elif datatype == 3:
        return np.roll(outer_group["data"][()], -1)
