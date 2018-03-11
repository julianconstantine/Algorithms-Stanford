###############################################
#  KRUSKAL'S MINIMUM SPANNING TREE ALGORITHM  #
###############################################

# Implement Kruskal's MST algorithm using the UnionFind data structure and compare with Prim's MST algorithm using the
# data from the last assignment


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


def get_vertices(edges):
    # Initialize vertex set
    V = set()

    for e in edges:
        u, v = e[0:2]
        V = V.union({u, v})

    return V


# Prim's MST Algorithm (from week #8 assignment)
def primMST(edges):
    V = get_vertices(edges=edges)

    s = edges[0][0]

    X = {s}
    T = set()

    while X != V:
        # Find edges (u, v) with u in X, v not in X (or u not in X, v in X; since this is an UNDIRECTED graph)
        crossing_edges = set([e for e in edges if e[0] in X and e[1] not in X or e[1] in X and e[0] not in X])

        if len(crossing_edges) > 0:
            # If there are crossing edges, find the cheapest one

            # Sort the edges by cost in ascending order and take the cheapest one
            cheapest_edge = sorted(crossing_edges, key=lambda x: x[2])[0]

            # Add cheapest edge to T
            T = T.union({cheapest_edge})

            # Add corresponding end vertex to X
            X = X.union({cheapest_edge[0], cheapest_edge[1]})

    # Compute total cost of MST
    mst_cost = sum([t[2] for t in T])

    return T, mst_cost


# UnionFind data structure
class UnionFind:
    def __init__(self, N):
        self.clusters = {key: key for key in range(1, N+1)}

    def find(self, p):
        return self.clusters[p]

    def union(self, p, q):
        pid = self.find(p)
        qid = self.find(q)

        for z in self.clusters:
            if self.find(z) == qid:
                self.clusters[z] = pid


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


###############
#  TEST CASE  #
###############

# Read in edges from test case
test_edges = read_edges('week-8/testEdges.txt')

# Run Prim's algorithm and Kruskal's algorithm
MST_prim, cost_prim = primMST(test_edges)
MST_kruskal, cost_kruskal = kruskalMST(test_edges)

# Both are -236 (so we're good)
print(cost_prim, cost_kruskal)

# Both also output the same MST
print(MST_prim, MST_kruskal)


######################
#  HOMEWORK PROBLEM  #
######################

# Read in edges from homework assignment #8
hw8_edges = read_edges('week-8/edges.txt')

# Run Prim's algorithm and Kruskal's algorithm
MST_prim, cost_prim = primMST(hw8_edges)
MST_kruskal, cost_kruskal = kruskalMST(hw8_edges)

# Both are -3612829
print(cost_prim, cost_kruskal)

# Both also output the same MST (do Prim's algorithm and Kruskal's algorithm do this in general? How many MSTs does
# this graph have?)
# (Returns True, because they are sets)
print(MST_prim == MST_kruskal)
