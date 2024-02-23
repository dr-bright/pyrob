import numpy as np
import scipy
import re  # regular expressions
from .misc import read_file


# lidar data is np.array([[a, r], ...])
# lidar dataset record is like this: x, y, a; r, r, ...
# {angle: distance}

def read_txt(txt, literal=False, degrange=240):
    """
    
    text format: r"(x, y, a; d{681}\n)*"
    Args:
        txt: str|text|bytes|readable
        literal: bool
        degrange: int: degrees
    Return:
        odom:  array[3, records]
        lidar: array[2, points, records]
    """
    txt = read_file(txt, literal=literal, decode='ascii').strip()
    row0 = txt[:txt.index('\n')]
    row_size = row0.count(',') + row0.count(';') + 1
    pat = re.compile(r';|,|\n', re.M)
    data = np.fromiter((float(v.strip()) for v in pat.split(txt)), dtype=float)
    data = data.reshape(-1, row_size)
    odom = data[:, :3].transpose()  # 3, records
    lidar = data[:, 3:].transpose() # points, records
    angrange = degrange * np.pi / 180
    angles = np.linspace(angrange / 2, -angrange/2, lidar.shape[0])
    angles = np.tile(angles, [lidar.shape[1], 1]).transpose()
    lidar = np.stack([angles, lidar], axis=0)
    # v = lidar[1, :, :].std(axis=1) < 0.4
    lidar[1, (lidar[1] == 5.6) | (lidar[1] < 0.35)] = np.nan
    # lidar[1, v] = np.nan
    """
    lidar[1, (lidar[1] == 5.6) | (lidar[1] < 0)] = np.nan
    lidar[1, 22:44,   :] = np.nan
    lidar[1, 64:69,   :] = np.nan
    lidar[1, 646:668, :] = np.nan
    """
    return odom, lidar


def cart(pts_polar):
    """
    
    Args:
        pts_polar: array[2, points, records]
    Returns:
        pts_cart: array[2, points, records]
    """
    a, d = pts_polar
    x, y = d * np.cos(a), d * np.sin(a)
    pts_cart = np.stack([x, y], axis=0)
    return pts_cart


def polar(pts_cart):
    """
    
    Args:
        pts_polar: array[2, points, records]
    Returns:
        pts_cart: array[2, points, records]
    """
    x, y = pts_cart
    r = np.sqrt(x * x + y * y)
    a = np.arctan2(y, x)
    pts_polar = np.stack([a, r], axis=0)
    return pts_polar


def stupid_slam(odom, lidar, a0=0):
    """
    
    Args:
        odom: array[3, records]
        lidar: array[2, points, records]
    Returns:
        carts: array[2, points, records]
    """
    pts_polar = lidar.copy()
    pts_polar[0] += odom[2] + a0
    pts_cart = cart(pts_polar)
    pts_cart[0] += odom[0]
    pts_cart[1] += odom[1]
    return pts_cart


def obs_map(pts, cell_size=None, recurse=False):
    """
    
    Args:
        pts: array[point_size, point_count]
    Returns:
        cell_size: float
        obs_map: array[*point_size]
    """
    if cell_size is None:
        pass


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    odom, lidar = read_txt('..\data\examp2.txt')
    a0 = 0
    ptc = stupid(odom, lidar, a0)
    mp = ptc.reshape(2, -1)
    plt.scatter(*mp, 1, 'r')
    # plt.savefig('test.png')
    plt.show();
    """
    plt.scatter(*mp, 1, 'r');
    plt.plot(*odom[:2, :]);
    plt.show();
    #"""
    # i = 20; m = lidar[:, :, i].copy(); m[0] += odom[2][i]; m = cart(m);  plt.scatter(*m); plt.show()
    

# d = np.diff(lidar[1, :, :], axis=1).mean(axis=1)

