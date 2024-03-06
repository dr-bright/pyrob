from misc import *
from mapp import *
from graph import *
import builtins

def voronoi(map_, mass_min=50, show=None):
    flag = False
    if show is True:
        _, show = plt.subplots()
        flag = True
    marked = mark_map(map_)
    obs = obstacles(marked, mass_min, True)
    masses = obs[2]
    obs = obs[:2].transpose()
    shape = np.array(map_.shape[::-1])
    corners =  np.indices((2,2)).transpose([2,1,0]).reshape(-1, 2) * shape * 4
    corners -= shape * 3 // 2
    obs = np.concatenate([obs, corners], axis=0)
    v = scipy.spatial.Voronoi(obs)
    g = PathGraph()
    g.vertices = [*map(lambda v: tuple(v[::-1]), v.vertices.tolist())]
    g.update(map(tuple, filter(lambda edge: -1 not in edge, v.ridge_vertices)))
    if show:
        show.clear()
        show.imshow(map_)
        g.render2D(show)
        show.scatter(*obs.transpose())
        show.set_xlim(0, map_.shape[1])
        show.set_ylim(1, map_.shape[0])
        if flag:
            plt.show()
    return g

if __name__ == '__main__':
    from lidar import *
    odom, lidar = read_txt('..\..\data\examp2.txt')
    pts = stupid_slam(odom, lidar)
    map_ = render_ptc(pts, 100)
    g = voronoi(map_, show=True)
    
    
    