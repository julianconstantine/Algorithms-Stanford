###############################
#  PROGRAMMING ASSIGNMENT #3  #
###############################

# KARGER'S MIN CUT ALGORITHM
# The file contains the adjacency list representation of a simple undirected graph. There are 200 vertices labeled 1
# to 200. The first column in the file represents the vertex label, and the particular row (other entries except the
# first column) tells all the vertices that the vertex is adjacent to. So for example, the 6th row looks like:
# "6 155 56	52 120 ...". This just means that the vertex with label 6 is adjacent to (i.e., shares an edge
# with) the vertices with labels 155, 56, 52, 120, ... , etc.

# Your task is to code up and run the randomized contraction algorithm for the min cut problem and use it on the above
# graph to compute the min cut. (HINT: Note that you'll have to figure out an implementation of edge contractions.
# Initially, you might want to do this naively, creating a new graph from the old every time there's an edge
# contraction. But you should also think about more efficient implementations.) (WARNING: As per the video lectures,
# please make sure to run the algorithm many times with different random seeds, and remember the smallest cut that you
# ever find.) Write your numeric answer in the space provided. So e.g., if your answer is 5, just type 5 in the space
# provided.

import numpy as np

import random


def read_adjacency_list(path):
    # Read the adjacency list from a specified file
    f = open(path, mode='r')
    data = f.readlines()

    adjacency_list = {}

    for row in data:
        row_data = [int(i) for i in row.split()]
        vertex = row_data[0]
        edges = row_data[1:]

        adjacency_list[vertex] = edges

    return adjacency_list


def create_edge_list(adjacency_list):
    # List of all edges stored as tuples
    edge_list = []

    for u in adj_list:
        edges = [(u, v) for v in adjacency_list[u]]

        edge_list += edges

    return edge_list


def choose_random_edge(adjacency_list):
    vertices = [v for v in adjacency_list]

    weights = np.array([len(adjacency_list[v]) for v in vertices])
    weights = weights/sum(weights)

    u = np.random.choice(a=vertices, size=1, p=weights)[0]

    v = random.sample(adjacency_list[u], 1)[0]

    return u, v


min_cut = [0]*1000

for i in range(1000):
    adj_list = read_adjacency_list(path='week-3/kargerMinCut.txt')

    # This will fail if we set merge_list = adj_list, because then they will both point to each other
    # We need to make a copy of the adjacency list that doesn't point to the same location in memory
    merge_list = read_adjacency_list(path='week-3/kargerMinCut.txt')

    while len(adj_list) > 2:
        u, v = choose_random_edge(adjacency_list=adj_list)

        # Merge vertices u and v
        adj_list[u] += adj_list[v]
        merge_list[u] += merge_list[v]

        # Delete vertex v
        adj_list.pop(v)
        merge_list.pop(v)

        # Find any edges pointing to v and flip them to point to
        for x in adj_list:
            adj_list[x] = [y if y != v else u for y in adj_list[x]]

        # Remove self loops
        adj_list[u] = [w for w in adj_list[u] if w != u and w in adj_list]

    a, b = adj_list.keys()

    min_cut[i] = len(adj_list[a])

    print(i)

# The smallest min cut in our series of experiments is 17
#   CHECK: CORRECT!
min(min_cut)




