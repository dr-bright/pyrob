from .mathops import *
import cv2

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


def median_filter(image, ksize=3):
    image = np.array(image)
    return cv2.medianBlur(image, ksize)
    
