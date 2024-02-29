import matplotlib.pyplot as plt

class Graph(set):
    """
    
    Атрибуты:
        self.edges = [ (id1, id2), ... ]
    """
    
    def make_directed(self):
        self.intersection_update(map(tuple, map(sorted, self)))
    
    def add_edge(self, id1, id2, directed=False):
        edge = tuple(sorted((id1, id2)
        if not directed:
            edge = tuple(sorted(edge))
        self.edges.add(edge)
    
    def remove_edge(self, id1, id2, *ids):
        self.edges.discard((id1, id2))
        if self.directed:
            self.edges.discard((id2, id1))
        if ids
    
    def remove_vertex(self, id):
        remove = set(filter(lambda x: id in x, self.edges))
        self.edges -= remove
        return remove

class SpatialGraph(Graph):
    def add_vertex(self, label, *ids):
        if not hasattr(self, 'vertices'):
            self.vertices = []
        id = len(self.vertices)
        self.vertices.append(label)
        self.add_edge(id, *ids)
        return id
    
    def render2D(self, ax):
        if ax is None:
            fig, ax = plt.subplots()
        ax.scatter(*zip(self.vertices))
        xs, ys = [], []
        for edge in self.edges:
            pair = map(self.vertices.__getitem__, edge)
            ax.plot(*zip(*pair))
        return ax
    