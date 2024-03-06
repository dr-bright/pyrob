import cv2 as cv
import numpy as np
import itertools
from .graph import PathGraph


def sparse_map(map_, stride):
    """
    
    Args:
        stride: int | tuple[int, int]
    """
    if isinstance(stride, int):
        stride = (stride, stride)
    s = [0] * len(map_.shape)
    for i in range(len(map_.shape)):
        s[i] = np.s_[:: stride[i]]
    return map_[tuple(s)]


def iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def every_cell(shape, index=None):
    """Iterates over nd indices
    
    Args:
        start: int | tuple[int, ...]
        stop: int | tuple[int, ...]
        step: int | tuple[int, ...]
    """
    if index is None:
        index = slice(None)
    if not iterable(index):
        index = len(shape) * [index]
    ranges = [range(*s.indices(shape[i])) for i, s in enumerate(index)]
    return itertools.product(*ranges)


def celldec(map_, mask=None, loops=None, stride=None):
    """
    
    Args:
        map: ndarray
        mask: ndarray with same nd
        loops: None | bool | list[bool] of len(map_.shape)
        stride: None | int | list[int]  of len(map_.shape)
    """
    if mask is None:
        mask = np.zeros((3,) * len(map_.shape))
        for cell in every_cell(mask.shape):
            vec = np.array(cell) - 1
            if sum(abs(vec)) == 1:
                mask[cell] = 1
    if loops is None:
        loops = [False] * len(map_.shape)
    elif not iterable(loops):
        loops = [loops] * len(map_.shape)
    if stride is not None:
        map_ = sparse_map(map_, stride)
    else:
        stride = [1] * len(map_.shape)
    stride = np.array(stride)
    loops = np.array(loops)
    shape = np.array(map_.shape)
    graph = PathGraph()
    center = np.array(mask.shape) // 2
    for node in every_cell(map_.shape):
        if map_[node]:    continue
        id = graph.add_vertex(tuple(node * stride))
        for neighbor in every_cell(mask.shape):
            if not mask[neighbor]:  continue
            cell = neighbor - center + node
            if all(cell == node):   continue
            idx = tuple(cell)
            problems = (cell < 0) | (cell >= shape)
            problems = problems & ~loops
            if any(problems):       continue
            cell = cell.clip(0, shape - 1)
            if map_[idx]:           continue
            graph.add_vertex(tuple(cell * stride), id)
    return graph
    """
    
    Args:
        stride: int | list[int] - step size
    """

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from .lidar import read_txt, stupid_slam
    from .mapp import render_ptc, extend_angle
    
    odom, lidar = read_txt('../data/examp5.txt')
    dpu = 100
    robot_size = (0.38, 0.58)
    robot_shape = (np.array(robot_size) * dpu).round().astype(int)
    pts = stupid_slam(odom, lidar)
    map_ = render_ptc(pts, 100)
    emap = extend_angle(map_, robot_shape, 4)
    
    gs = []
    for i in range(4):
        manuevers = np.array([
            [i == 1, i == 0, i == 3], 
            [i == 2,    0,   i == 2], 
            [i == 3, i == 0, i == 1], 
        ])
        g = celldec(emap[i], manuevers, stride=30)
        gs.append(g)
        g.render2D(show=False).imshow(emap[i])
        plt.show()
    