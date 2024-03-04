from mathops import *

import cv2 as cv
import matplotlib.pyplot as plt


def detect_dpu(ptc):
    pass

def render_ptc(ptc, dpu, point_size=2, margin=50, thresh=150, ksize=5, msize=7):
    """
    
    ptc: array[2, points, ...]
    """
    ptc = ptc.reshape(2, -1)
    corner = ptc.min(axis=1)
    size = (ptc.max(axis=1) - corner)
    ptc = ptc - corner.reshape(-1, 1) + margin / dpu
    shape = (size.reshape(-1) * dpu + margin * 2).astype(int)[::-1]
    image = np.zeros((*shape.tolist(), 3), dtype=np.uint8)
    for i in range(ptc.shape[1]):
        pt = (ptc[:, i] * dpu).astype(int)
        cv.circle(image, pt, point_size, (255, 255, 255), -1)
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.blur(image, (ksize, ksize))
    image = ((image >= thresh) * 255).astype(np.uint8)
    image = cv.medianBlur(image, msize)
    return image


def mark_map(map):
    return scipy.ndimage.label(map)[0]


def obstacles(marked, mass_thresh=None, convex=None):
    """
    Args:
        marked - array[height, width]
    Returns:
        np.array[3, classes]
    """
    classes = marked.max()
    obs = []
    ids = np.indices(marked.shape)
    for cls in range(1, classes+1):
        mask = marked == cls
        pts = ids[:, mask]
        mass = pts.shape[1]
        row, col = (pts.sum(axis=1) / mass).round().astype(int)
        if mass_thresh and mass < mass_thresh:
            continue
        if convex and not mask[row, col]:
            continue
        obs.append((col, row, mass))
    return np.array(obs).astype(int).transpose()


def minkowski(map, shape):
    kernel = np.ones(shape)
    return cv.filter2D(map, cv.CV_32F, kernel) > 0


if __name__ == '__main__':
    from lidar import *
    
    odom, lidar = read_txt('../../data/examp5.txt')
    ptc = stupid_slam(odom, lidar)
    image = render_ptc(ptc, 100, ksize=5, msize=7)
    plt.imshow(image)
    plt.show()
    