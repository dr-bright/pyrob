from .mathops import rotate_image

import pathlib
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import scipy



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
    return cv.filter2D(map, cv.CV_32F, kernel) > 0.2


def extend_angle(map, robot_shape, layers=8):
    """
    
    Args:
        map: array[height, width]
        robot_shape: (width: int, height: int)  -- in pixels
        step_deg: int                           -- rotation step in degrees
    Returns:
        emap: array[angle, height, width]
    """
    robot_shape = np.array(robot_shape[::-1])
    tail = (map.shape - robot_shape) % 2
    margin = (map.shape - robot_shape) // 2
    robot = np.ones(robot_shape)
    robot = np.pad(robot, ((margin[0], margin[0] + tail[0])
                            , (margin[1], margin[1] + tail[1])
                          ))
    emap = []
    print(map.shape, robot.shape)
    for angle in np.arange(0, np.pi, np.pi / layers):
        rob = rotate_image(robot, angle)
        layer = cv.filter2D(map, cv.CV_32F, rob) > 0.3
        emap.append(layer)
    return np.stack(emap, axis=0)

if __name__ == '__main__':
    from .lidar import *
    
    path = pathlib.Path('..','..','data', 'examp2.txt')

    odom, lidar = read_txt(str(path))
    dpu = 100
    robot_size = (0.38, 0.58)
    robot_shape = (np.array(robot_size) * dpu).round().astype(int)
    
    ptc = stupid_slam(odom, lidar)
    map = render_ptc(ptc, dpu, ksize=5, msize=7)
    emap = extend_angle(map, robot_shape)
    
    
    plt.imshow(map); plt.show()
    for layer in emap:
        plt.imshow(layer); plt.show()
    pass
    
    