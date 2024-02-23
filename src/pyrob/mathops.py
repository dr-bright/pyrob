import numpy as np
import scipy


def convolve(a, b):
    out_shape = np.array((a.shape, b.shape)).max(0)  # shape = both inputs bounding
    fa = np.fft.rfftn(a, out_shape)                  # padded with 0 if necessary
    fb = np.fft.rfftn(b, out_shape)
    return np.fft.irfftn(fa * fb)


def minkowski(ptcA, ptcB):
    pass
    