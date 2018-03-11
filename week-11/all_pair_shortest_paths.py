################################
#  PROGRAMMING ASSIGNMENT #11  #
################################

# In this assignment you will implement one or more algorithms for the all-pairs shortest-path problem. Here are data
# files describing three graphs:
#
#       g1.txt
#
#       g2.txt
#
#       g3.txt
#
# The first line indicates the number of vertices and edges, respectively. Each subsequent line describes an edge (the
# first two numbers are its tail and head, respectively) and its length (the third number). NOTE: some of the edge
# lengths are negative. NOTE: These graphs may or may not have negative-cost cycles.
#
# Your task is to compute the "shortest shortest path". Precisely, you must first identify which, if any, of the three
# graphs have no negative cycles. For each such graph, you should compute all-pairs shortest paths and remember the
# smallest one (i.e., compute min{d(u,v) | (u, v) in E}, where d(u,v) denotes the shortest-path distance from u to v).
#
# If each of the three graphs has a negative-cost cycle, then enter "NULL" in the box below. If exactly one graph has
# no negative-cost cycles, then enter the length of its shortest shortest path in the box below. If two or more of
# the graphs have no negative-cost cycles, then enter the smallest of the lengths of their shortest shortest paths
# in the box below.
#
# OPTIONAL: You can use whatever algorithm you like to solve this question. If you have extra time, try comparing the
# performance of different all-pairs shortest-path algorithms!
#
# OPTIONAL: Here is a bigger data set to play with.
#
#   large.txt
#
# For fun, try computing the shortest shortest path of the graph in the file above.

import numpy as np

import datetime
import pickle
import networkx as nx


def read_weighted_graph(path):
    """
    Reads in a weighted edge list representation of a directede graph
    """
    f = open(path, mode='r')
    data = f.readlines()
    f.close()

    # Number of vertices and edges
    n, m = data[0].split()
    n = int(n)
    m = int(m)

    lines = []

    for line in data[1:]:
        u, v, cost = line.split()
        u = int(u)
        v = int(v)
        cost = int(cost)
        lines.append((u, v, cost))

    return lines


def get_vertices(edges):
    """
    Get list of vertices from an edge list representation of a directed graph
    """
    u_list = [e[0] for e in edges]
    v_list = [e[1] for e in edges]

    vertices = list(set(u_list + v_list))

    return vertices


def add_imaginary_vertex(graph):
    """
    Adds an imaginary vertex s (labeled 0) to an edge-list representation of a graph. The new vertex will have an edge
    to each of the other vertices in the graph of cost 0.
    """
    # Get vertex list of graph
    vertices = get_vertices(graph)

    # Initialize an edge from vertex 0 to each of the vertices of the original graph
    new_edges = [(0, v, 0) for v in vertices]

    # Add these new edges to the graph
    new_graph = graph + new_edges

    return new_graph


def bellman_ford(G, s):
    """
    Run Bellman-Ford algorithm on graph G with vertices V, |V| = n, and source vertex s
    """
    V = get_vertices(G)
    n = len(V)

    # Support 1-based indexing in second dimension
    # Need extra row at end for first dimension to check for negative cycles
    A = np.zeros((n+1, n))

    # Initialize A[0, s] - 0; A[0, v] = +inf, v != s
    for v in V:
        if v == s:
            A[0, v] = 0
        else:
            A[0, v] = float('inf')

    for i in range(1, n+1):
        for v in V:
            # Compute minimum
            incident_edges = [e for e in G if e[1] == v]

            if len(incident_edges) > 0:
                incident_costs = [(w, v, cost + A[i-1, w]) for (w, v, cost) in incident_edges]

                min_incident_cost = sorted(incident_costs, key=lambda x: x[2])[0][2]

                A[i, v] = min(A[i-1, v], min_incident_cost)
            else:
                A[i, v] = A[i-1, v]

        if i % 10 == 0:
            print(i, datetime.datetime.now())

    return A


def detect_negative_cycles(A):
    n = A.shape[0] - 1

    A_n = A[n]
    A_nm = A[n-1]

    for i in range(len(A_n)):
        if A_n[i] != A_nm[i]:
            return True

    return False


def reweight_edges(edge_list, weights):
    new_edge_list = []

    for i, e in enumerate(edge_list):
        u, v, w = e

        w_new = w + weights[u] - weights[v]

        new_edge_list.append((u, v, w_new))

    return new_edge_list


def edge_list_to_adjacency_list(edge_list):
    """
    Converts edge list representation of a graph to adjacency list representation
    """
    adjacency_list = {}

    for edge in edge_list:
        u, v, w = edge

        try:
            adjacency_list[u][v] = w
        except KeyError:
            adjacency_list[u] = {v: w}

        if v not in adjacency_list:
            adjacency_list[v] = {}

    return adjacency_list


class DirectedGraph:
    def __init__(self, adjacency_list):
        self.adj_list = adjacency_list
        self.explored = {key: False for key in self.adj_list.keys()}
        self.vertices = set([v for v in self.adj_list])

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


def slowDijkstra(G, s):
    """
    Implementation of Dijkstra's algorithm using a DirectedGraph class based on an adjacency list representation of a graph
    """
    V = G.vertices
    X = {s}

    A = {s: 0}
    B = {s: []}

    while X != V:
        dijkstra_scores = {}

        for v in X:
            edges = G[v]

            for w in edges:
                if w not in X:
                    dijkstra_scores[(v, w)] = A[v] + edges[w]

        e, score = sorted(dijkstra_scores.items(), key=lambda x: x[1])[0]

        v_star, w_star = e

        # print(v_star, w_star, score)

        # A[w_star] = A[v_star] + l_e
        A[w_star] = score
        B[w_star] = B[v_star] + [(v_star, w_star)]

        X.add(w_star)

    return A, B


def prepare_for_dijkstra(edge_list, bf_matrix):
    # Step 1: Clear out any edges with the extra 0 vertex
    clean_edges = [e for e in edge_list if e[0] != 0 and e[1] != 0]

    # Read weights from array output
    vertex_weights = {(i + 1): int(w) for i, w in enumerate(bf_matrix[bf_matrix.shape[0] - 2, 1:].tolist())}

    # Reweight edges
    reweighted_edges = reweight_edges(edge_list=clean_edges, weights=vertex_weights)

    # # Create adjacency list
    # adj_list = edge_list_to_adjacency_list(reweighted_edges)
    #
    # # Delete empty/extraneous keys
    # adj_list = {k: adj_list[k] for k in adj_list if adj_list[k] != {}}
    #
    # # Output DirectedGraph object
    # graph = DirectedGraph(adjacency_list=adj_list)

    graph = nx.DiGraph()
    graph.add_weighted_edges_from(reweighted_edges)

    return graph


def find_min_APSP(graph_original, graph_reweighted, vertices):
    shortest_paths = {}
    distances = {}

    for i, u in enumerate(vertices):
        for j, v in enumerate(vertices):
            try:
                shortest_uv_path = nx.shortest_path(graph_reweighted, u, v, weight='weight')
                shortest_paths[(u, v)] = shortest_uv_path

                if len(shortest_uv_path) == 1:
                    distances[(u, v)] = 0
                else:
                    uv_sum = 0

                    for k in range(len(shortest_uv_path) - 1):
                        e1, e2 = shortest_uv_path[k:(k + 2)]
                        uv_sum += graph_original.get_edge_data(e1, e2)['weight']

                    distances[(u, v)] = uv_sum
            except nx.exception.NetworkXNoPath:
                distances[(u, v)] = float('inf')

        print(i, datetime.datetime.now())

    argmin = sorted(distances, key=distances.get)[0]
    return distances[argmin]


#####################
#  SMALL TEST CASES #
#####################

# TEST CASE #1B
G1b_original = read_weighted_graph(path='week-11/g1b.txt')
G1b = add_imaginary_vertex(G1b_original)
A1b = bellman_ford(G1b, 0)

V1b = get_vertices(G1b_original)

# The graph g1b has a negative cycle
#   CHECK: CORRECT!
if detect_negative_cycles(A1b):
    print("Graph has a negative cycle")


# TEST CASE #2B
G2b_original = read_weighted_graph(path='week-11/g2b.txt')
G2b = add_imaginary_vertex(G2b_original)
A2b = bellman_ford(G2b, 0)

V2b = get_vertices(G2b_original)

# No negative cycle
if detect_negative_cycles(A2b):
    print("Graph has a negative cycle")

# Find minimum shortest-path pairs
DG2b = prepare_for_dijkstra(G2b, A2b)

graph = nx.DiGraph()
graph.add_weighted_edges_from(G2b_original)

# The shortest of the shortest paths is -2
#   CHECK: CORRECY!
find_min_APSP(graph_original=graph, graph_reweighted=DG2b, vertices=V2b)


# TEST CASE #3B
G3b_original = read_weighted_graph(path='week-11/g3b.txt')
G3b = add_imaginary_vertex(G3b_original)
A3b = bellman_ford(G3b, 0)

V3b = get_vertices(G3b_original)

# No negative cycles
detect_negative_cycles(A3b)

# Find minimum shortest-path pairs
DG3b = prepare_for_dijkstra(G3b, A3b)

graph = nx.DiGraph()
graph.add_weighted_edges_from(G3b_original)

# The shortest of the shortest paths is -4
#   CHECK: CORRECT!
find_min_APSP(graph_original=graph, graph_reweighted=DG3b, vertices=V3b)


######################
#  OTHER TEST CASES  #
######################

# TEST CASE #1
G_test1_original = read_weighted_graph(path='week-11/test1.txt')
G_test1 = add_imaginary_vertex(G_test1_original)
A_test1 = bellman_ford(G_test1, 0)

V_test1 = get_vertices(G_test1_original)

# No negative cycles
detect_negative_cycles(A_test1)

# Find minimum shortest-path pairs
DG_test1 = prepare_for_dijkstra(G_test1, A_test1)

graph = nx.DiGraph()
graph.add_weighted_edges_from(G_test1_original)

# The shortest of all shortest paths is -10003
#   CHECK: CORRECT!
find_min_APSP(graph_original=graph, graph_reweighted=DG_test1, vertices=V_test1)


# TEST CASE #2
G_test2_original = read_weighted_graph(path='week-11/test2.txt')
G_test2 = add_imaginary_vertex(G_test2_original)
A_test2 = bellman_ford(G_test2, 0)

V_test2 = get_vertices(G_test2_original)

# No negative cycles
detect_negative_cycles(A_test2)

# Find minimum shortest-path pairs
DG_test2 = prepare_for_dijkstra(G_test2, A_test2)

graph = nx.DiGraph()
graph.add_weighted_edges_from(G_test2_original)

# The shortest of all shortest paths is -6
#   CHECK: CORRECT!
find_min_APSP(graph_original=graph, graph_reweighted=DG_test2, vertices=V_test2)


# TEST CASE #3
G_test3_original = read_weighted_graph(path='week-11/test3.txt')
G_test3 = add_imaginary_vertex(G_test3_original)
A_test3 = bellman_ford(G_test3, 0)

V_test3 = get_vertices(G_test3_original)

# This graph has a negative cycle
#   CHECK: CORRECT!
detect_negative_cycles(A_test3)


# TEST CASE #4
G_test4_original = read_weighted_graph(path='week-11/test4.txt')
G_test4 = add_imaginary_vertex(G_test4_original)
A_test4 = bellman_ford(G_test4, 0)

V_test4 = get_vertices(G_test4_original)

# This graph has no negative cycles
detect_negative_cycles(A_test4)

# Find minimum shortest-path pairs
DG_test4 = prepare_for_dijkstra(G_test4, A_test4)

graph = nx.DiGraph()
graph.add_weighted_edges_from(G_test4_original)

# The shortest of all shortest paths is -4
#   CHECK: CORRECT!
find_min_APSP(graph_original=graph, graph_reweighted=DG_test4, vertices=V_test4)


#########################
#  HOMEWORK ASSIGNMENT  #
#########################

# Read the weighted graphs
G3_original = read_weighted_graph(path='week-11/g3.txt')
G3 = add_imaginary_vertex(G3_original)

V3 = get_vertices(G3_original)

# Run the Bellman-Ford algorithm

# Save the BF matrix output

# Reload the BF matrix output
f1 = open('week-11/bf_g1.pkl', mode='rb')
A1 = pickle.load(file=f1)
f1.close()

f2 = open('week-11/bf_g2.pkl', mode='rb')
A2 = pickle.load(file=f2)
f2.close()

f3 = open('week-11/bf_g3.pkl', mode='rb')
A3 = pickle.load(file=f3)
f3.close()

# Graph 1 has a negative cycle
if detect_negative_cycles(A1):
    print("Graph 1 has a negative cycle")

# Graph 2 has a negative cycle
if detect_negative_cycles(A2):
    print("Graph 2 has a negative cycle")

# Graph 3 does NOT havea negative cycle
if detect_negative_cycles(A3):
    print("Graph 3 has a negative cycle")

# Prepare graph 3 to back-out the shortest paths using "Dijkstra"/NetworkX
reweighted_nxGraph3 = prepare_for_dijkstra(G3, A3)

nxGraph3 = nx.DiGraph()
nxGraph3.add_weighted_edges_from(G3_original)

final_answer = find_min_APSP(graph_original=nxGraph3, graph_reweighted=reweighted_nxGraph3, vertices=V3)

# The smallest shortest-path in graph 3 has length -19
#   CHECK: CORRECT!
print(final_answer)
