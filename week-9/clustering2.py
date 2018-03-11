
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


def read_big_file(path):
    f = open(path, mode='r')
    data = f.readlines()
    f.close()

    lines = []

    for line in data[1:]:
        line = [int(n) for n in line.split()]
        lines.append(line)

    return lines


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


n = int(1e+10)

l = [(1, 1, 1) for i in range(n)]

