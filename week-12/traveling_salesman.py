################################
#  PROGRAMMING ASSIGNMENT #12  #
################################

# In this assignment you will implement one or more algorithms for the traveling salesman problem, such as the dynamic
# programming algorithm covered in the video lectures. Here is a data file describing a TSP instance.
#
# The first line indicates the number of cities. Each city is a point in the plane, and each subsequent line indicates
# the x- and y-coordinates of a single city.
#
# The distance between two cities is defined as the Euclidean distance --- that is, two cities at locations (x,y) and
# (z,w) have distance sqrt((x - z)^2 + (y - w)^2) between them.
#
# In the box below, type in the minimum cost of a traveling salesman tour for this instance, rounded down to the nearest
# integer.
#
# OPTIONAL: If you want bigger data sets to play with, check out the TSP instances from around the world here. The
# smallest data set (Western Sahara) has 29 cities, and most of the data sets are much bigger than that. What's the
# largest of these data sets that you're able to solve --- using dynamic programming or, if you like, a completely
# different method?
#
# HINT: You might experiment with ways to reduce the data set size. For example, trying plotting the points. Can you
# infer any structure of the optimal solution? Can you use that structure to speed up your algorithm?

import matplotlib.pyplot as plt

from collections import defaultdict

import itertools
import datetime
import math
import os


def read_euclidean_data(path):
    """
    Reads in coordinate data from an external file.

    :param path: Path to data file
    :return: A list of coordinate pairs (x, y)
    """
    f = open(path, mode='r')
    data = f.readlines()
    f.close()

    coordinates = []

    for line in data[1:]:
        x, y = line.split()

        x = float(x)
        y = float(y)

        coordinates.append((x, y))

    return coordinates


def create_edge_list(coordinates):
    """
    Creates a weighted edge list from a set of coordinates

    :param coordinates: A list of tuples containing (x, y) coordinates
    :return: A list of tuples (i, j, dist(i, j)), where dist(i, j) is the distance between the ith and jth
             coordinate pairs
    """
    edges = []

    for i in range(len(coordinates)):
        xi, yi = coordinates[i]

        for j in range(len(coordinates)):
            xj, yj = coordinates[j]

            dist_ij = math.sqrt((xi - xj)**2 + (yi - yj)**2)

            edges.append((i+1, j+1, dist_ij))

    return edges


def get_subsets(n, k):
    """
    Generate all subsets of the numbers 1, 2, ... n of size k+1 that must include 1

    :param n: Range of subset
    :param k: Size of subset (minus 1)
    :return: List of all subsets
    """
    subsets = []

    if k == 0:
        return [{1}]
    else:
        for S0 in itertools.combinations(list(range(2, n+1)), k):
            S = set(S0).union([1])
            subsets.append(S)

        return subsets


def create_edge_lookup(edges):
    """
    Creates a lookup table keyed by edge tuples that returns the distance between any two points

    :param edges: List of edges
    :return: Dictionary of tuples (u, v) where d[(u, v)] = dist(u, v)
    """
    edge_lookup = {}

    for e in edges:
        u = e[0]
        v = e[1]
        w = e[2]
        edge_lookup[(u, v)] = w

    return edge_lookup


########################
#  DATA VISUALIZATION  #
########################

# Number of vertices
n = len(cities)

cities_x = [x for x, y in cities]
cities_y = [y for x, y in cities]

plt.plot(cities_x, cities_y, 'k-')
plt.plot(cities_x, cities_y, 'k.')
plt.close()

# Visualization of subset sizes
subset_sizes = []

for k in range(0, n):
    # Number of subsets is (n-1) choose k
    size_k = int(math.factorial(25-1)/(math.factorial(25-1-k)*math.factorial(k)))

    subset_sizes.append(size_k)

plt.plot(list(range(1, 26)), subset_sizes)
plt.close()


#########################################
#  STILL USE TUPLES, BUT WRITE TO DISK  #
#########################################


def read_from_disk(path):
    """
    Helper function that reads the solutions to subproblems line-by-line from a temporary file called current.txt
    :param path: path to file
    :return: defaultdict containing subproblems and their solutions (the A[S, j])
    """
    f = open(path, mode='r')

    d = defaultdict(lambda: float('inf'))

    for line in f:
        s_list, j, cost = line.split(' : ')

        j = int(j)
        cost = float(cost)

        s = tuple([int(t) for t in s_list.split()])

        d[(s, j)] = cost

    f.close()

    return d

# Read in data
data = read_euclidean_data('week-12/tsp.txt')
edges = create_edge_list(data)

# Lookup table for costs of edges
edge_lookup = create_edge_lookup(edges)

n = len(data)

previous = defaultdict(lambda: float('inf'))

# Initialize previous[s,1] = 0 when s = (1,)
for k in range(1, n+1):
    s = (k,)

    if k == 1:
        previous[(s, 1)] = 0

for m in range(1, n):
    # Get all subsets of 1 + (2. 3, ..., 25) for size m+1
    subsets = itertools.combinations(list(range(2, n+1)), r=m)

    # Open connection to temporary file
    f = open('week-12/current.txt', mode='w')

    for s0 in subsets:
        # Subset S
        s = tuple([1] + list(s0))

        for j in s:
            if j == 1:
                continue
            else:
                # Subset S \ {j}
                s_not_j = tuple([t for t in s if t != j])

                # Get the value of A[S, j]
                current_s_j = min([previous[(s_not_j, k)] + edge_lookup[(min(k, j), max(k, j))] for k in s_not_j])

                # Convert to string and save output in temporary file
                s_string = " ".join([str(t) for t in list(s)])
                f.write(s_string + " : " + str(j) + " : " + str(current_s_j) + "\n")

    f.close()

    # Clear out defaultdict previous and load in the new one (for the next iteration)
    del previous
    previous = read_from_disk(path='week-12/current.txt')

    print(m, datetime.datetime.now())

# Delete the temporary file
os.remove('week-12/current.txt')

# Get answer
s = tuple(range(1, n+1))

ans = min([previous[s, j] + edge_lookup[j, 1] for j in range(2, n+1)])

# Min-cost tour for first 6 cities is: 8607
#                         7          : 9498
#                         8          : 9765
#                         9          : 10769
#                         10         : 12349
#                         11         : 12518
#                         12         : 13312
#                         13         : 14662
#                         14         : 16898
#                         15         : 19269
#                         16         : 22943
#                         17         : 22953
#                         18         : 23005
#                         19         : 23101
#                         20         : 23328
#                         21         : 24146
#                         22         : 24474
#                         23         : 24522
#                         24         : 26391
#                         25         : 26442
#   CHECK: CORRECT! #swag #gucci #yolo #alanturing #datagod
print("The minimum-cost tour has cost %.0f" % math.floor(ans))
