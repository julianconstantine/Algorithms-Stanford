###############################
#  PROGRAMMING ASSIGNMENT #5  #
###############################

# DIJKSTRA'S SHORTEST-PATH ALGORITHM
# The file dijkstraData.tst contains an adjacency list representation of an undirected weighted graph with 200 vertices
# labeled 1 to 200. Each row consists of the node tuples that are adjacent to that particular vertex along with the
# length of that edge. For example, the 6th row has 6 as the first entry indicating that this row corresponds to the
# vertex labeled 6. The next entry of this row "141,8200" indicates that there is an edge between vertex 6 and vertex
# 141 that has length 8200. The rest of the pairs of this row indicate the other vertices adjacent to vertex 6 and
# the lengths of the corresponding edges.

# Your task is to run Dijkstra's shortest-path algorithm on this graph, using 1 (the first vertex) as the source
# vertex, and to compute the shortest-path distances between 1 and every other vertex of the graph. If there is no
# path between a vertex v and vertex 1, we'll define the shortest-path distance between 1 and v to be 1000000.

# You should report the shortest-path distances to the following ten vertices, in order: 7,37,59,82,99,115,133,165,
# 188,197. You should encode the distances as a comma-separated string of integers. So if you find that all ten of
# these vertices except 115 are at distance 1000 away from vertex 1 and 115 is 2000 distance away, then your answer
# should be 1000,1000,1000,1000,1000,2000,1000,1000,1000,1000. Remember the order of reporting DOES MATTER, and the
# string should be in the same order in which the above ten vertices are given. The string should not contain any
# spaces. Please type your answer in the space provided.


def read_weighted_adjacency_list(path):
    # Read the adjacency list from a specified file
    f = open(path, mode='r')
    data = f.readlines()

    adjacency_list = {}

    for row in data:
        row_data = row.split()
        vertex = int(row_data[0])

        pairs = [t.split(',') for t in row_data[1:]]
        weighted_edges = {int(t[0]): int(t[1]) for t in pairs}

        adjacency_list[vertex] = weighted_edges

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
    # Implementation of Dijkstra's algorithm without using a heap
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

        print(v_star, w_star, score)

        # A[w_star] = A[v_star] + l_e
        A[w_star] = score
        B[w_star] = B[v_star] + [(v_star, w_star)]

        X.add(w_star)

    return A, B


################
#  TEST CASES  #
################

test_list1 = {
    1: {2: 1, 8: 2},
    2: {1: 1, 3: 1},
    3: {2: 1, 4: 1},
    4: {3: 1, 5: 1},
    5: {4: 1, 6: 1},
    6: {5: 1, 7: 1},
    7: {6: 1, 8: 1},
    8: {7: 1, 1: 2}
}

G1 = DirectedGraph(adjacency_list=test_list1)

A, B = slowDijkstra(G=G1, s=1)


################
#  ASSIGNMENT  #
################

adj_list = read_weighted_adjacency_list(path='week-5/dijkstraData.txt')
G = DirectedGraph(adjacency_list=adj_list)

A, B = slowDijkstra(G=G, s=1)

# Returns: [2599, 2610, 2947, 2052, 2367, 2399, 2029, 2442, 2505, 3068]
#   CHECK: CORRECT!
print([A[x] for x in [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]])
