import numpy as np
import scipy
import cv2 as cv


def convolve(a, b):
    out_shape = np.array((a.shape, b.shape)).max(0)  # shape = both inputs bounding
    fa = np.fft.rfftn(a, out_shape)                  # padded with 0 if necessary
    fb = np.fft.rfftn(b, out_shape)
    return np.fft.irfftn(fa * fb)

def imfilter(image, filter_kernel, recenter=True):
    image = np.array(image)
    filter_kernel = np.array(filter_kernel)
    if len(image.shape) - len(filter_kernel.shape) == 1:
        return np.stack([
            imfilter(image[:, :, i], filter_kernel)
            for i in range(image.shape[-1])
        ], axis=len(image.shape)-1)
    filter_kernel = filter_kernel[::-1, ::-1]
    out = convolve(image, filter_kernel).real
    if recenter:
        shape = np.array(filter_kernel.shape)
        out = np.roll(out, -(shape // 2), axis=[*range(len(shape))])
    return out

def rotate_image(image, radians):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    mtx = cv.getRotationMatrix2D(image_center, radians / np.pi * 180, 1.0)
    rsp = cv.warpAffine(image, mtx, image.shape[1::-1], flags=cv.INTER_LINEAR)
    return rsp

# cv.medianBlur