###########################
#  WEEK 4: SHORTEST PATH  #
###########################

# This is my own attempt to compute the shortest path between two vertices of a graph using Breadth-First Search (
# BFS). I will use an adjacency list representation of a graph.

# NOTE: This is NOT Dijkstra's Algorithm, but it's sort of a precursor to it (from what I gathered reading Wikipedia)
# We will do Dijkstra's Algorithm in week 5 of the course

import itertools
import random

# Adjacency list representation of a graph I just came up with
adj_list = {
    1: [2, 5],
    2: [1, 3],
    3: [2, 4, 10],
    4: [3, 5, 6, 7],
    5: [1, 4],
    6: [4, 7, 8, 10],
    7: [4, 6, 8, 9],
    8: [6, 9],
    9: [7, 8],
    10: [3, 6]
}

# Another adjacency list representation of a random graph I create
# NOTE: This graph is NOT connected!
adj_list2 = {
    1: [5],
    2: [4, 6, 7],
    3: [5, 9],
    4: [2],
    5: [3, 9],
    6: [2, 7],
    7: [2, 8],
    8: [7, 10],
    9: [3, 5],
    10: [8]
}


class Queue:
    def __init__(self):
        self.queue_list = []

    def enqueue(self, item):
        # Enqueue item to the front of the queue list
        self.queue_list = [item] + self.queue_list

    def dequeue(self):
        # Dequeue the "oldest" item from the back of the list (FIFO)
        if len(self.queue_list) > 0:
            # First-In First-Out (FIFO), remove first element added to queue (which is at the END of the list!)
            out = self.queue_list[-1]

            # Remove element from list
            self.queue_list = self.queue_list[:-1]

            return out
        else:
            return None

    def __repr__(self):
        # The __repr__ method determines what is printed to the console when you just "type" the Queue object
        return str(self.queue_list)

    def isEmpty(self):
        # Check if Queue is
        return len(self.queue_list) == 0


class UndirectedGraph:
    def __init__(self, adjacency_list):
        self.adj_list = adjacency_list
        self.explored = {key: False for key in self.adj_list.keys()}

    def __getitem__(self, item):
        return self.adj_list[item]

    def __repr__(self):
        return str(self.adj_list)

    def exploreVertex(self, vertex):
        # Mark vertex as explored
        self.explored[vertex] = True

    def isExplored(self, vertex):
        # Check if vertex has been explored
        return self.explored[vertex]

    def vertices(self):
        # Get vertex set V of graph G = (V, E)
        return self.adj_list


def generate_random_graph(n, m):
    # Generates a Graph object with n vertices and m edges

    # Have n vertices labeled 1, 2, ... , n
    vertices = list(range(1, n+1))

    # Now randomly create m edges
    # NOTE: No self-loops or parallel edges for now
    all_edges = [e for e in itertools.combinations(iterable=vertices, r=2)]

    edges = random.sample(population=all_edges, k=m)

    # List of "doubled" edges (i.e. now have (v, u) for every (u, v) in edges)
    edges_double = edges + [(e[1], e[0]) for e in edges]

    # Turn these into an adjacency list
    adj_list = {}

    for v in vertices:
        adjlist[v] = [e[1] for e in edges_double if e[0] == v]

    # Generate an UndirectedGraph object from the the adjacency list
    graph = UndirectedGraph(adjacency_list=adj_list)

    return graph


def shortest_path(graph, s, v):
    # Calculates the shortest path between vertices s and v in UndirectedGraph graph

    # Mark s as explored
    graph.exploreVertex(s)

    # Initialize distances for each vertex u to infinity if u != s and 0 if u = s
    dist = {key: float('inf') for key in graph.vertices()}
    dist[s] = 0

    # Create a Queue
    q = Queue()

    # Enqueue s as the first item in q
    q.enqueue(item=s)

    while not q.isEmpty():
        # Pop the front element of the queue
        t = q.dequeue()

        neighbors = graph[t]
        print(t, graph[t])

        for w in neighbors:
            if not graph.isExplored(vertex=w):
                # If w is not yet explored, mark is as explored and add it to the queue
                graph.exploreVertex(vertex=w)

                q.enqueue(item=w)

                # Update the distance
                dist[w] = dist[t] + 1

    return dist[v]

g = UndirectedGraph(adj_list2)
shortest_path(g, 10, 2)