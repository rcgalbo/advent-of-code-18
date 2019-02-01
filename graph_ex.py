from collections import defaultdict
from typing import List, Tuple
import heapq
import sys

from tmp import Cave

def adjacent(coord):
    '''return coord ( up, down, right, left )'''
    i, j = coord
    return ((i - 1, j),
            (i + 1, j),
            (i, j - 1),
            (i, j + 1))


class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxsize
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True
    
    def set_not_visited(self):
        self.visited = False

    def __lt__(self, other):
        return self.distance < other.distance

    def __repr__(self):
        return f'{self.id} adjacent: {[x.id for x in self.adjacent]}'


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

    def reset(self):
        for v in self:
            v.set_distance(sys.maxsize)
            v.set_not_visited()
            v.previous = None
    


    @staticmethod
    def build(empty):
        g = Graph()
        
        visited = []
        for c in empty:
            g.add_vertex(c)
            v = g.get_vertex(c)
            idc = [c.id for c in v.adjacent]
            for adj in adjacent(c):
                if adj in empty:
                    ad = g.get_vertex(adj)
                    if ad:
                        ida = ([a.id for a in ad.adjacent])
                        if adj not in idc and c not in ida:
                            g.add_edge(c, adj, cost=1)

        return g


def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return


def dijkstra(aGraph, start):
    '''compute the shortest from origin to all other points'''
    # Set the distance for the start node to zero
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(), v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        # for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
            #     print('updated : current = %s next = %s new_dist = %s'
            #           % (current.get_id(), next.get_id(), next.get_distance()))
            # else:
            #     print('not updated : current = %s next = %s new_dist = %s'
            #           % (current.get_id(), next.get_id(), next.get_distance()))

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(), v)
                           for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)


if __name__ == '__main__':

    ex = """#########
    #G..G..G#
    #.......#
    #.......#
    #G..E..G#
    #.......#
    #.......#
    #G..G..G#   
    #########"""

    c = Cave(ex)

    g = Graph.build(c.get_empty())

    print('Graph data:')
    for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print('( %s , %s, %3d)' % (vid, wid, v.get_weight(w)))

    dijkstra(g, g.get_vertex((2, 1)))

    target = g.get_vertex((2, 2))
    path = [target.get_id()]
    shortest(target, path)
    print('The shortest path : %s' % (path[::-1]))
