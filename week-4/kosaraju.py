###############################
#  PROGRAMMING ASSIGNMENT #4  #
###############################

# KOSARAJU'S ALGORITHM
# The file contains the edges of a directed graph. Vertices are labeled as positive integers from 1 to 875714. Every
# row indicates an edge, the vertex label in first column is the tail and the vertex label in second column is the head
# (recall the graph is directed, and the edges are directed from the first column vertex to the second column vertex).
# So for example, the 11th row looks like: "2 47646". This just means that the vertex with label 2 has an outgoing
# edge to the vertex with label 47646.

# Your task is to code up the algorithm from the video lectures for computing strongly connected components (SCCs),
# and to run this algorithm on the given graph.

# Output Format: You should output the sizes of the 5 largest SCCs in the given graph, in decreasing order of sizes,
# separated by commas (avoid any spaces). So if your algorithm computes the sizes of the five largest SCCs to be 500,
# 400, 300, 200 and 100, then your answer should be "500,400,300,200,100" (without the quotes). If your algorithm
# finds less than 5 SCCs, then write 0 for the remaining terms. Thus, if your algorithm computes only 3 SCCs whose
# sizes are 400, 300, and 100, then your answer should be "400,300,100,0,0" (without the quotes). (Note also that your
# answer should not have any spaces in it.)

from collections import defaultdict

import pickle
import sys


####################################
#  CLASS AND FUNCTION DEFINITIONS  #
####################################

def read_edgelist():
    f = open('week-4/SCC.txt', mode='r')
    data = f.readlines()
    f.close()

    edges = []

    for row in data:
        u, v = row.split()  # Get edge tuple
        u, v = int(u), int(v)  # Convert to integer
        edges.append((u, v))  # Append to edge list

    return edges


def get_scc_sizes(leaders):
    scc_sizes = defaultdict(int)

    for node in leaders:
        scc = leaders[node]
        scc_sizes[scc] += 1

    return scc_sizes


def top_five_sccs(leaders):
    scc_sizes = get_scc_sizes(leaders)

    top_five = sorted(scc_sizes.values(), reverse=True)[0:min(5, len(scc_sizes))]

    return top_five + [0]*(5 - len(top_five))


def edge_list_to_adjacency_list(edge_list):
    adjacency_list = {}

    for edge in edge_list:
        u, v = edge

        try:
            adjacency_list[u] += [v]
        except KeyError:
            adjacency_list[u] = [v]

        if v not in adjacency_list:
            adjacency_list[v] = []

    return adjacency_list


class KosarajuGraph:
    # Mostly the same as the UndirectedGraph implementation, but with a few extra variables
    def __init__(self, adjacency_list):
        self.adj_list = adjacency_list
        self.vertices = [v for v in self.adj_list]
        self.explored = {key: False for key in self.vertices}

        # Global variables for Kosaraju's Algorithm
        self.t = 0
        self.s = None

        # Leaders
        self.leaders = {key: 0 for key in self.vertices}

        # Finishing times
        self.finishing_times = {key: 0 for key in self.vertices}

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

    def DFS(self, i):
        self.exploreVertex(vertex=i)

        self.leaders[i] = self.s

        for j in self.adj_list[i]:
            if not self.isExplored(vertex=j):
                # print(i, j)
                self.DFS(j)

        # Increment t by one
        self.t += 1

        # Set ith finishing time
        self.finishing_times[i] = self.t

    def StackDFS(self, i):
        stack = [(i, 0)]

        self.exploreVertex(i)

        self.leaders[i] = self.s

        while len(stack) > 0:
            v, index = stack.pop()

            while index < len(self[v]):
                tail = self[v][index]
                index += 1

                if not self.isExplored(tail):
                    self.exploreVertex(tail)
                    stack.append((v, index-1))
                    stack.append((tail, 0))
                    break

            if index == len(self[v]):
                self.t += 1
                self.finishing_times[i] = self.t

    def DFSLoop(self, ordering=None):
        if ordering is None:
            iterator = range(len(self.vertices), 0, -1)
        else:
            iterator = iter(sorted(ordering, key=ordering.get, reverse=True))

        for i in iterator:
            if not self.isExplored(vertex=i):
                # print(i)
                self.s = i
                # self.DFS(i)
                self.StackDFS(i)


################
#  TEST CASES  #
################

# Test edge lists
test_edges_1 = [(1, 4), (2, 8), (3, 6), (4, 7), (5, 2), (6, 9), (7, 1), (8, 5), (8, 6), (9, 7), (9, 3)]

test_edges_2 = [(1, 2), (2, 6), (2, 3), (2, 4), (3, 1), (3, 4), (4, 5), (5, 4), (6, 5), (6, 7), (7, 6), (7, 8), (8, 5), (8, 7)]

test_edges_3 = [(1, 2), (2, 3), (3, 1), (3, 4), (5, 4), (6, 4), (8, 6), (6, 7), (7, 8)]

test_edges_4 = [(1, 2), (2, 3), (3, 1), (3, 4), (5, 4), (6, 4), (8, 6), (6, 7), (7, 8), (4, 3), (4, 6)]

test_edges_5 = [(1, 2), (2, 3), (2, 4), (2, 5), (3, 6), (4, 5), (4, 7), (5, 2), (5, 6), (5, 7), (6, 3), (6, 8), (7, 8), (7, 10), (8, 7), (9, 7), (10, 9), (10, 11), (11, 12), (12, 10)]

# Reversed edge lists
test_edges_1_reversed = [(e[1], e[0]) for e in test_edges_1]
test_edges_2_reversed = [(e[1], e[0]) for e in test_edges_2]
test_edges_3_reversed = [(e[1], e[0]) for e in test_edges_3]
test_edges_4_reversed = [(e[1], e[0]) for e in test_edges_4]
test_edges_5_reversed = [(e[1], e[0]) for e in test_edges_5]

# Convert to adjacency lists
test_adj_list_1 = edge_list_to_adjacency_list(test_edges_1)
test_adj_list_2 = edge_list_to_adjacency_list(test_edges_2)
test_adj_list_3 = edge_list_to_adjacency_list(test_edges_3)
test_adj_list_4 = edge_list_to_adjacency_list(test_edges_4)
test_adj_list_5 = edge_list_to_adjacency_list(test_edges_5)

test_adj_list_1_rev = edge_list_to_adjacency_list(test_edges_1_reversed)
test_adj_list_2_rev = edge_list_to_adjacency_list(test_edges_2_reversed)
test_adj_list_3_rev = edge_list_to_adjacency_list(test_edges_3_reversed)
test_adj_list_4_rev = edge_list_to_adjacency_list(test_edges_4_reversed)
test_adj_list_5_rev = edge_list_to_adjacency_list(test_edges_5_reversed)

# Test case 1
G1 = KosarajuGraph(adjacency_list=test_adj_list_1)
G1_rev = KosarajuGraph(adjacency_list=test_adj_list_1_rev)

G1_rev.DFSLoop()

ordering = G1_rev.finishing_times

G1.DFSLoop(ordering=ordering)

# SCCs 7, 8, 9 each have size 3
sccs = get_scc_sizes(G1.leaders)

# Final answer: 3,3,3,0,0
#   CHECK: CORRECT!
print(top_five_sccs(G1.leaders))


# Test case 2
G2 = KosarajuGraph(adjacency_list=test_adj_list_2)
G2_rev = KosarajuGraph(adjacency_list=test_adj_list_2_rev)

G2_rev.DFSLoop()

ordering = G2_rev.finishing_times

G2.DFSLoop(ordering=ordering)

# SCCs 2 and 8 have size 3, SCC 5 has size 2
get_scc_sizes(G2.leaders)

# Final answer: 3,3,2,0,0
#   CHECK: CORRECT!
print(top_five_sccs(G2.leaders))


# Test case 3
G3 = KosarajuGraph(adjacency_list=test_adj_list_3)
G3_rev = KosarajuGraph(adjacency_list=test_adj_list_3_rev)

G3_rev.DFSLoop()

ordering = G3_rev.finishing_times

G3.DFSLoop(ordering=ordering)

# SCCs 3 and 8 have size 3; SCCs 4 and 5 have size 1
get_scc_sizes(G3.leaders)

# Final answer: 3,3,1,1,0
#   CHECK: CHECK!
print(top_five_sccs(G3.leaders))


# Test case 4
G4 = KosarajuGraph(adjacency_list=test_adj_list_4)
G4_rev = KosarajuGraph(adjacency_list=test_adj_list_4_rev)

G4_rev.DFSLoop()

ordering = G4_rev.finishing_times

G4.DFSLoop(ordering=ordering)

# SCC 8 has size 7, SCC 5 has size 1
get_scc_sizes(G4.leaders)

# Final answer: 7,1,0,0,0
#   CHECK: CORRECT!
print(top_five_sccs(G4.leaders))


# Test case 5
G5 = KosarajuGraph(adjacency_list=test_adj_list_5)
G5_rev = KosarajuGraph(adjacency_list=test_adj_list_5_rev)

G5_rev.DFSLoop()

ordering = G5_rev.finishing_times

G5.DFSLoop(ordering=ordering)

# SCC 12 has size 6, SCC 4 has size 3, SCC 6 has size 2, SCC1 has size 1
get_scc_sizes(G5.leaders)

# Final answer: 6,3,2,1,0
#   CHECK: CORRECT!
print(top_five_sccs(G5.leaders))


###########################################
#  CONVERT EDGE LISTS TO ADJACENCY LISTS  #
###########################################

# This code only needs to be run once to "pickle" the adjacency lists
"""
# Read edge list
edges = read_edgelist()

# Create reversed edge list
edges_reversed = [(e[1], e[0]) for e in edges]

# Create adjacency lists from the edge lists
adj_list = edge_list_to_adjacency_list(edge_list=edges)
adj_list_rev = edge_list_to_adjacency_list(edge_list=edges_reversed)

# Dump adjacency lists to JSON files so we can re-use them
# json.dump(obj=adj_list, fp=open('week-4/kosaraju.json', mode='w'), indent=4)
# json.dump(obj=adj_list_rev, fp=open('week-4/kosaraju_reversed.json', mode='w'), indent=4)

# Serialize the adjacency lists (faster than saving to JSON files)
pickle.dump(obj=adj_list, file=open('week-4/kosaraju.pkl', mode='wb'))
pickle.dump(obj=adj_list_rev, file=open('week-4/kosaraju_reversed.pkl', mode='wb'))
"""

####################################
#  IMPLEMENT KOSARAJU'S ALGORITHM  #
####################################

# Current recursion limit is 1,000
sys.getrecursionlimit()

# Reset the recursion limit to 10,000
sys.setrecursionlimit(500000)


# Read in adjacency lists
adj_list = pickle.load(file=open('week-4/kosaraju.pkl', mode='rb'))
adj_list_rev = pickle.load(file=open('week-4/kosaraju_reversed.pkl', mode='rb'))

# Create graphs from adjacency lists
G = KosarajuGraph(adjacency_list=adj_list)
G_rev = KosarajuGraph(adjacency_list=adj_list_rev)

G_rev.DFSLoop()

ordering = G_rev.finishing_times

G.DFSLoop(ordering=ordering)

get_scc_sizes(G.leaders)

# SOLUTION: 434821, 968, 459, 313, 211
#   CHECK: CORRECT
print(top_five_sccs(G.leaders))
