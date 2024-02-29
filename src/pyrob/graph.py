import matplotlib.pyplot as plt

class Graph(set):
    """
    
    Атрибуты:
        self.edges = [ (id1, id2), ... ]
    """    
    def add_edge(self, id, *ids):
        for id2 in ids:
            edge = tuple(sorted((id, id2)))
            self.add(edge)
    
    def remove_edge(self, id, *ids, directed=False):
        for id2 in ids:
            self.discard((id1, id2))
            self.discard((id2, id1))
    
    def get_neighbors(self, id):
        neighbors = set()
        for edge in self:
            edge = list(edge)
            if id in edge:
                edge.remove(id)
                neighbors.add(edge.pop())
        return neighbors
    
    def remove_vertex(self, id):
        neighbors = self.get_neighbors(self, id)
        self.remove_edge(id, *neighbors)
        

class SpatialGraph(Graph):
    """
    
    Атрибуты:
        self.vertices = список координат вершин
    """
    def add_vertex(self, label, *ids):
        if not hasattr(self, 'vertices'):
            self.vertices = []
        id = len(self.vertices)
        self.vertices.append(label)
        self.add_edge(id, *ids)
        return id
    
    def render2D(self, ax, show=None):
        if ax is None:
            fig, ax = plt.subplots()
            if show is None:
                show = True
        ax.scatter(*zip(self.vertices))
        xs, ys = [], []
        for edge in self.edges:
            pair = map(self.vertices.__getitem__, edge)
            ax.plot(*zip(*pair))
        show and plt.show()


class WeightedGraph(Graph):
    def set_weight(self, id1, id2=None, *, w):
        if not hasattr(self, 'weights'):
            self.weights = {}
        idx = id1
        if id2 is not None:
            idx = tuple(sorted((id1, id2)))
        if w is None:
            return self.weights.pop(idx, None)
        else:
            self.weights[idx] = w
    
    def get_weight(self, id1, id2=None):
        idx = id1
        if id2 is not None:
            idx = tuple(sorted((id1, id2)))
        return self.weights.get(idx)
    
    