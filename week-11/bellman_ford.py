# Implements the Bellman-Ford algorithm, which DOES NOT COMPUTE ALL-PAIRS SHORTEST-PATHS
# That's why this wasn't working

# Ignore the unit tests! (At least this tests out the BF algorithm)

import numpy as np

import datetime


def read_weighted_graph(path):
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

    return n, m, lines


def get_vertices(edges):
    u_list = [e[0] for e in edges]
    v_list = [e[1] for e in edges]

    vertices = list(set(u_list + v_list))

    return vertices


# BELLMAN-FORD
def bellman_ford(n, V, G):
    # Support 1-based indexing in second dimension
    # Need extra row at end for first dimension to check for negative cycles
    A = np.zeros((n+1, n+1))

    s = V[0]

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


def get_min(A):
    n = A.shape[0] - 1

    A_n = A[n]
    A_nm = A[n-1]

    for i in range(len(A_n)):
        if A_n[i] != A_nm[i]:
            return None

    return int(min(A[n-1]))


##################
#  TEST CASE #1  #
##################

# Read in edge list
n_test1, m_test1, G_test1 = read_weighted_graph(path='week-11/test1.txt')

# Get vertex list
V_test1 = get_vertices(G_test1)

# Run the Bellman-Ford algorithm
A_test1 = bellman_ford(n=n_test1, V=V_test1, G=G_test1)

# The minimum shortest-path for the graph is -10003
#   CHECK: CORRECT!
ans = get_min(A_test1)

if ans is None:
    print("NULL")
else:
    print(ans)


##################
#  TEST CASE #2  #
##################

# Read in edge list
n_test2, m_test2, G_test2 = read_weighted_graph(path='week-11/test2.txt')

# Get vertex list
V_test2 = get_vertices(G_test2)

# Run the Bellman-Ford algorithm
A_test2 = bellman_ford(n=n_test2, V=V_test2, G=G_test2)

# The minimum shortest-path for the graph is -6
#   CHECK: CORRECT!
ans = get_min(A_test2)

if ans is None:
    print("NULL")
else:
    print(ans)


##################
#  TEST CASE #3  #
##################

# Read in edge list
n_test3, m_test3, G_test3 = read_weighted_graph(path='week-11/test3.txt')

# Get vertex list
V_test3 = get_vertices(G_test3)

# Run the Bellman-Ford algorithm
A_test3 = bellman_ford(n=n_test3, V=V_test3, G=G_test3)

# This graph contains a negative-cost cycle
#   CHECK: CORRECT!
ans = get_min(A_test3)

if ans is None:
    print("NULL")
else:
    print(ans)


##################
#  TEST CASE #4  #
##################

# Read in edge list
n_test4, m_test4, G_test4 = read_weighted_graph(path='week-11/test4.txt')

# Get vertex list
V_test4 = get_vertices(G_test4)

# Run the Bellman-Ford algorithm
A_test4 = bellman_ford(n=n_test4, V=V_test4, G=G_test4)

# The minimum shortest-path for this graph is -3
#   CHECK: INCORRECT (should be -4)
ans = get_min(A_test4)

if ans is None:
    print("NULL")
else:
    print(ans)


##################
#  TEST CASE #5  #
##################

# Read in edge list
n_test5, m_test5, G_test5 = read_weighted_graph(path='week-11/test5.txt')

# Get vertex list
V_test5 = get_vertices(G_test5)

# Run the Bellman-Ford algorithm
A_test5 = bellman_ford(n=n_test5, V=V_test5, G=G_test5)

# The minimum shortest-path for this graph is -5
#   CHECK: ???
ans = get_min(A_test5)

if ans is None:
    print("NULL")
else:
    print(ans)


##################
#  TEST CASE #6  #
##################

# Read in edges
n1b, m1b, G1b = read_weighted_graph(path='week-11/g1b.txt')
n2b, m2b, G2b = read_weighted_graph(path='week-11/g2b.txt')
n3b, m3b, G3b = read_weighted_graph(path='week-11/g3b.txt')

# Get vertex lists
V1b = get_vertices(G1b)
V2b = get_vertices(G2b)
V3b = get_vertices(G3b)

# Run the Bellman-Ford algorithm
A1b = bellman_ford(n=n1b, V=V1b, G=G1b)
A2b = bellman_ford(n=n2b, V=V2b, G=G2b)
A3b = bellman_ford(n=n3b, V=V3b, G=G3b)

min1 = get_min(A=A1b)
min2 = get_min(A=A2b)
min3 = get_min(A=A3b)

# Graph G1b has a negative cycle
# Graph G2b has minimum shortest-path cost -1
# Graph G3b has minimum shortest-path cost -4
print(min1, min2, min3)


#########################
#  HOMEWORK ASSIGNMENT  #
#########################

# Read in edges and create vertex lists
n1, m1, G1 = read_weighted_graph(path='week-11/g1.txt')
V1 = get_vertices(G1)

n2, m2, G2 = read_weighted_graph(path='week-11/g2.txt')
V2 = get_vertices(G2)

n3, m3, G3 = read_weighted_graph(path='week-11/g3.txt')
V3 = get_vertices(G3)

# Run Bellman-Ford algorithm on first graph
A1 = bellman_ford(n=n1, V=V1, G=G1)
ans1 = get_min(A=A1)

#  Graph 1 has a negative cycle
if ans1 is None:
    print("Graph 1 has a negative cycle")
else:
    print("Minimum-cost shortest-path of graph 1 has cost: %i" % ans1)

# Run the Bellman-Ford algorithm on the second graph
A2 = bellman_ford(n=n2, V=V2, G=G2)
ans2 = get_min(A=A2)

# Graph 2 has a negative cycle
if ans2 is None:
    print("Graph 2 has a negative cycle")
else:
    print("Minimum-cost shortest-path of graph 2 has cost: %i" % ans2)

# Run the Bellman-Ford algorithm on the third graph
A3 = bellman_ford(n=n3, V=V3, G=G3)
ans3 = get_min(A=A3)

# Minimum-cost shortest-path of graph 3 has cost: -12
if ans3 is None:
    print("Graph 2 has a negative cycle")
else:
    print("Minimum-cost shortest-path of graph 3 has cost: %i" % ans3)


# Final answer: -12
#   CHECK: INCORRECT :(


#####################################


# Support 1-based indexing in second dimension
A = np.zeros((n, n+1))

s = V[0]

# Initialize A[0, s] - 0; A[0, v] = +inf, v != s
for v in V:
    if v == s:
        A[0, v] = 0
    else:
        A[0, v] = float('inf')

for i in range(1, n):
    for v in V:
        # Compute minimum
        incident_edges = [e for e in G if e[1] == v]

        incident_costs = [(w, v, cost + A[i-1, w]) for (w, v, cost) in incident_edges]

        A[i, v] = sorted(incident_costs, key=lambda x: -x[2])[0][2]

    print(i)