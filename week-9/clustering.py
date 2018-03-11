###############################
#  PROGRAMMING ASSIGNMENT #8  #
###############################

# In this programming problem and the next you'll code up the clustering algorithm from lecture for computing a
# max-spacing k-clustering.


def read_edges(file):
    f = open(file, mode='r')
    data = f.readlines()
    f.close()

    lines = data[1:]

    edges = []

    for line in lines:
        # Parse raw lines
        u, v, cost = line.split()

        # Convert to integers
        u = int(u)
        v = int(v)
        cost = int(cost)

        edges.append((u, v, cost))

    return edges


def get_vertices(edges, aslist=False):
    # Initialize vertex set
    V = set()

    for e in edges:
        u, v = e[0:2]
        V = V.union({u, v})

    if aslist:
        return list(V)
    else:
        return V


# UnionFind data structure
class UnionFind:
    def __init__(self, N):
        self.clusters = {key: key for key in range(1, N + 1)}

    def find(self, p):
        return self.clusters[p]

    def union(self, p, q):
        pid = self.find(p)
        qid = self.find(q)

        for z in self.clusters:
            if self.find(z) == qid:
                self.clusters[z] = pid

    def n_clusters(self):
        return len(set(self.clusters.values()))


# Kruskal's MST Algorithm
def kruskalMST(edges):
    # Sort edges in ascending order by cost
    sorted_edges = sorted(edges, key=lambda x: x[2])

    T = set()
    UF = UnionFind(N=len(sorted_edges))

    for i, e in enumerate(sorted_edges):
        u, v = e[0:2]

        if UF.find(u) != UF.find(v):
            UF.union(u, v)
            T = T.union({e})

    mst_cost = sum([e[2] for e in T])

    return T, mst_cost


# Use Kruskal's Algorithm to find maximum-spacing k-clustering
def cluster(edges, k):
    # Sort edges in ascending order by cost
    sorted_edges = sorted(edges, key=lambda x: x[2])
    vertices = get_vertices(edges)

    T = set()
    UF = UnionFind(N=len(vertices))

    for i, e in enumerate(sorted_edges):
        u, v = e[0:2]

        if UF.find(u) != UF.find(v):
            UF.union(u, v)
            T = T.union({e})

        if UF.n_clusters() == k:
            break

    # Edges crossing between clusters
    crossing_edges = [e for e in edges if UF.find(e[0]) != UF.find(e[1])]

    spacing = min([e[2] for e in crossing_edges])

    return UF.clusters, spacing


# PROBLEM #1
# This file describes a distance function (equivalently, a complete graph with edge costs). It has the following format:
#
#       [number_of_nodes]
#
#       [edge 1 node 1] [edge 1 node 2] [edge 1 cost]
#
#       [edge 2 node 1] [edge 2 node 2] [edge 2 cost]
#
#       ...
#
# There is one edge (i,j) for each choice of 1≤i<j≤n, where n is the number of nodes.
#
# For example, the third line of the file is "1 3 5250", indicating that the distance between nodes 1 and 3
# (equivalently, the cost of the edge (1,3) is 5250. You can assume that distances are positive, but you should NOT
# assume that they are distinct.

# Your task in this problem is to run the clustering algorithm from lecture on this data set, where the target number
# k of clusters is set to 4. What is the maximum spacing of a 4-clustering?

# ADVICE: If you're not getting the correct answer, try debugging your algorithm using some small test cases. And
# then post them to the discussion forum!


################
#  TEST CASES  #
################

# TEST CASE #1
# Read in test edges
test_edges1 = read_edges('week-9/test1.txt')

# Run single-link clustering algorithm
clusters_test1, spacing_test1 = cluster(test_edges1, k=4)

# The spacing is 7
#   CHECK: CORRECT!
print(spacing_test1)

# TEST CASE #2
# Read in test edges
test_edges2 = read_edges('week-9/test2.txt')

# Run single-link clustering algorithm
clusters_test2, spacing_test2 = cluster(test_edges2, k=4)

# The spacing is 2
#   CHECK: CORRECT!
print(spacing_test2)

#########################
#  HOMEWORK PROBLEM #1  #
#########################

# Read in edge list
edges = read_edges('week-9/clustering1.txt')

clusters, spacing = cluster(edges, k=4)

# The spacing of the maximum-distance 4-clustering is 106
#   CHECK: CORRECT!
print(spacing)


#########################
#  HOMEWORK PROBLEM #2  #
#########################

# In this question your task is again to run the clustering algorithm from lecture, but on a MUCH bigger graph. So big,
# in fact, that the distances (i.e., edge costs) are only defined implicitly, rather than being provided as an explicit
# list.
#
# The data set is is in the file clustering_big.txt.
#
# The format is:
#
#       [# of nodes] [# of bits for each node's label]
#
#       [first bit of node 1] ... [last bit of node 1]
#
#       [first bit of node 2] ... [last bit of node 2]
#
#       ...
#
# For example, the third line of the file "0 1 1 0 0 1 1 0 0 1 0 1 1 1 1 1 1 0 1 0 1 1 0 1" denotes the 24 bits
# associated with node #2.
#
# The distance between two nodes u and v in this problem is defined as the Hamming distance --- the number of
# differing bits --- between the two nodes' labels. For example, the Hamming distance between the 24-bit label of
# node #2 above and the label "0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1 0 1 0 0 1 0 1" is 3 (since they differ in the 3rd,
# 7th, and 21st bits).
#
# The question is: what is the largest value of k such that there is a k-clustering with spacing at least 3? That is,
# how many clusters are needed to ensure that no pair of nodes with all but 2 bits in common get split into different
# clusters?
#
# NOTE: The graph implicitly defined by the data file is so big that you probably can't write it out explicitly, let
# alone sort the edges by cost. So you will have to be a little creative to complete this part of the question. For
# example, is there some way you can identify the smallest distances without explicitly looking at every pair of nodes?

import datetime
import copy


def read_big_file(path):
    f = open(path, mode='r')
    data = f.readlines()
    f.close()

    lines = []

    for line in data[1:]:
        line = [int(n) for n in line.split()]
        lines.append(line)

    return lines


# UnionFind data structure
class HammingUnionFind:
    def __init__(self, codes):
        self.codes = {binary_list_to_decimal(c): c for c in codes}
        self.clusters = {key: key for key in self.codes.keys()}
        self.neighbors = {key: self.find_neighbors(key) for key in self.codes.keys()}

    def find(self, p):
        return self.clusters[p]

    def distance(self, i, j):
        dist = 0

        line_i = self.codes[i]
        line_j = self.codes[j]

        for k in range(len(line_i)):
            if line_i[k] != line_j[k]:
                dist += 1

        return dist

    def union(self, p, q):
        pid = self.find(p)
        qid = self.find(q)

        neighbors_of_p = self.neighbors[p]
        # neighbors_of_p = self.clusters

        for np in neighbors_of_p:
            try:
                z = self.clusters[np]
            except KeyError:
                continue

            if self.find(z) == qid:
                self.clusters[z] = pid

    def find_neighbors(self, p):
        code_p = self.codes[p]

        neighbors_one = []
        neighbors_two = []

        N = len(code_p)

        # Find all neighbors of distance one
        for i in range(N):
            swap_one = copy.copy(code_p)

            if code_p[i] == 1:
                swap_one[i] = 0
            else:
                swap_one[i] = 1

            neighbors_one.append(binary_list_to_decimal(swap_one))

        # Find all neighbors of distance two
        for i in range(N):
            for j in range(i+1, N):
                if j != i:
                    swap_two = copy.copy(code_p)

                    if code_p[i] == 1:
                        swap_two[i] = 0
                    else:
                        swap_two[i] = 1

                    if code_p[j] == 1:
                        swap_two[j] = 0
                    else:
                        swap_two[j] = 1

                    neighbors_two.append(binary_list_to_decimal(swap_two))

        neighbors = neighbors_one + neighbors_two

        return neighbors

    def n_clusters(self):
        # Counts up number of unique parents
        # return len(set(self.clusters.values()))

        # Need to count up number of unique roots
        num = 0

        for key in self.clusters:
            if key == self.clusters[key]:
                num += 1

        return num


def binary_list_to_decimal(x):
    n = len(x)

    b = 0

    for i in range(n):
        b += x[n - i - 1]*2**i

    return b


################
#  TEST CASES  #
################

# TEST #1: Use file test_big3.txt
lines = read_big_file('week-9/test_big3.txt')

decimals = list(map(binary_list_to_decimal, lines))

hammingUF = HammingUnionFind(codes=lines)

for i, p in enumerate(decimals):
    neighbors_of_p = hammingUF.neighbors[p]

    for q in neighbors_of_p:
        try:
            d_pq = hammingUF.distance(p, q)
        except KeyError:
            continue

        if 1 <= d_pq <= 2:
            hammingUF.union(p, q)

# The minimum k required is 1
#   CHECK: CORRECT!
print(hammingUF.n_clusters())


# TEST #2: Use the file test_big22.txt
lines = read_big_file('week-9/test_big22.txt')

decimals = list(map(binary_list_to_decimal, lines))

hammingUF = HammingUnionFind(codes=lines)

for i, p in enumerate(decimals):
    neighbors_of_p = hammingUF.neighbors[p]

    for q in neighbors_of_p:
        try:
            d_pq = hammingUF.distance(p, q)
        except KeyError:
            continue

        if 0 <= d_pq <= 2:
            hammingUF.union(p, q)

# The minimum k required is 4
#   CHECK: INCORRECT
print(hammingUF.n_clusters())


# TEST #3: Use file test_big24.txt
lines = read_big_file('week-9/test_big24.txt')

decimals = list(map(binary_list_to_decimal, lines))

hammingUF = HammingUnionFind(codes=lines)

for i, p in enumerate(decimals):
    neighbors_of_p = hammingUF.neighbors[p]

    for q in neighbors_of_p:
        try:
            d_pq = hammingUF.distance(p, q)
        except KeyError:
            continue

        if 1 <= d_pq <= 2:
            hammingUF.union(p, q)

# The minimum k required is 7
#   CHECK: CORRECT!
print(hammingUF.n_clusters())


######################
#  HOMEWORK PROBLEM  #
######################

# Run on homework problem #2 file clustering_big.txt
lines = read_big_file('week-9/clustering_big.txt')

decimals = list(map(binary_list_to_decimal, lines))

hammingUF = HammingUnionFind(codes=lines)

for i, p in enumerate(decimals):
    neighbors_of_p = hammingUF.neighbors(p)

    for q in neighbors_of_p:
        try:
            d_pq = hammingUF.distance(p, q)
        except KeyError:
            continue

        if - <= d_pq <= 2:
            hammingUF.union(p, q)

    if i % 100 == 0:
        print(i, datetime.datetime.now())

print(hammingUF.n_clusters())