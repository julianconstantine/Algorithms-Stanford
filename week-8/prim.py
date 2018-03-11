##############################
#  WEEK 8: PRIM'S ALGORITHM  #
##############################

# The file edges.txt describes an undirected graph with integer edge costs. It has the format
#
# [number_of_nodes] [number_of_edges]
#
# [one_node_of_edge_1] [other_node_of_edge_1] [edge_1_cost]
#
# [one_node_of_edge_2] [other_node_of_edge_2] [edge_2_cost]
#
# ...
#
# For example, the third line of the file is "2 3 -8874", indicating that there is an edge connecting vertex #2 and
# vertex #3 that has cost -8874.
#
# You should NOT assume that edge costs are positive, nor should you assume that they are distinct.
#
# Your task is to run Prim's minimum spanning tree algorithm on this graph. You should report the overall cost of a
# minimum spanning tree --- an integer, which may or may not be negative --- in the box below.
#
# IMPLEMENTATION NOTES: This graph is small enough that the straightforward O(mn) time implementation of Prim's
# algorithm should work fine. OPTIONAL: For those of you seeking an additional challenge, try implementing a heap-based
# version. The simpler approach, which should already give you a healthy speed-up, is to maintain relevant edges in a
# heap (with keys = edge costs). The superior approach stores the unprocessed vertices in the heap, as described in
# lecture. Note this requires a heap that supports deletions, and you'll probably need to maintain some kind of mapping
# between vertices and their positions in the heap.


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

###############
#  TEST CASE  #
###############

# Read in test edges
test_edges = read_edges(file='week-8/testEdges.txt')

# Run Prim's Algorithm
MST, cost = primMST(edges=test_edges)

# The cost of the MST is -236
#   CHECK: CORRECT!
print(cost)


################
#  ASSIGNMENT  #
################

# Read in edges
edges = read_edges('week-8/edges.txt')

# Read Prim's Algorithm
MST, cost = primMST(edges=edges)

# The cost of the MST is -3612829
#   CHECK: CORRECT!
print(cost)
