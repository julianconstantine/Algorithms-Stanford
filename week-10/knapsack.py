################################
#  PROGRAMMING ASSIGNMENT #10  #
################################

# PROBLEM #1
# In this programming problem and the next you'll code up the knapsack algorithm from lecture.
#
# Let's start with a warm-up. Download the text file knapsack1.txt.
#
# This file describes a knapsack instance, and it has the following format:
#
#       [knapsack_size][number_of_items]
#
#       [value_1] [weight_1]
#
#       [value_2] [weight_2]
#
#       ...
#
# For example, the third line of the file is "50074 659", indicating that the second item has value 50074 and size
# 659, respectively.
#
# You can assume that all numbers are positive. You should assume that item weights and the knapsack capacity are
# integers.
#
# In the box below, type in the value of the optimal solution.
#
# ADVICE: If you're not getting the correct answer, try debugging your algorithm using some small test cases. And
# then post them to the discussion forum!

import numpy as np

import datetime


def knapsack(values, weights, W, verbose=False):
    n = len(values)

    # This does not work because on the second replication, Python copies the list by reference rather than by value
    # A = [[0]*(W + 1)]*(n+1)

    # Use a NumPy array instead
    A = np.zeros((n+1, W+1), dtype='int')

    for i in range(n):
        w_i = weights[i]
        v_i = values[i]

        for x in range(0, W+1):
            if x < w_i:
                A[i+1, x] = A[i, x]
            else:
                A[i+1, x] = max(A[i, x], A[i, x-w_i] + v_i)

        print(i, datetime.datetime.now())

    return A


# def cachedKnapsack(values, weights, W, verbose=False):
#     n = len(values)
#
#     # Use a NumPy array instead
#     A = np.zeros((n+1, W+1), dtype='int')
#
#     for i in range(n):
#         w_i = weights[i]
#         v_i = values[i]
#
#         for x in range(0, W+1):
#             if x < w_i:
#                 A[i+1, x] = A[i, x]
#             else:
#                 A[i+1, x] = max(A[i, x], A[i, x-w_i] + v_i)
#
#         print(i, datetime.datetime.now())
#
#     return A


def read_objects(path):
    f = open(path, mode='r')
    data = f.readlines()
    f.close()

    values = []
    weights = []

    max_capacity = int(data[0].split()[0])

    for line in data[1:]:
        v, w = line.split()
        v, w = int(v), int(w)

        values.append(v)
        weights.append(w)

    return values, weights, max_capacity


#####################
#  LECTURE EXAMPLE  #
#####################

MAX_CAPACITY = 6
weights = [4, 3, 2, 3]
values = [3, 2, 4, 4]

n, W = 4, 6

# Run the dynamic programming algorithm
array = knapsack(values, weights, MAX_CAPACITY)

# The optimal value of this instance of the Knapsack problem is 8 (as desired
print(array[n, W])


#######################
#   HOMEWORK PROBLEM  #
#######################

# Read in data
values, weights, max_capacity = read_objects(path='week-10/knapsack1.txt')

# Parameters n and W (number of items and maximum capacity of knapsack)
n, W = len(values), max_capacity

# Run knapsack algorithm
array = knapsack(values=values, weights=weights, W=max_capacity)

# The optimal value of the knapsack problem for these paramters is 2493893
#   CHECK: CORRECT!
print(array[n, W])


# PROBLEM #2
# This problem also asks you to solve a knapsack instance, but a much bigger one.
#
# Download the text file knapsack_big.txt.
#
# This file describes a knapsack instance, and it has the following format:
#
#       [knapsack_size][number_of_items]
#
#       [value_1] [weight_1]
#
#       [value_2] [weight_2]
#
#       ...
#
# For example, the third line of the file is "50074 834558", indicating that the second item has value 50074 and size
# 834558, respectively. As before, you should assume that item weights and the knapsack capacity are integers.
#
# This instance is so big that the straightforward iterative implementation uses an infeasible amount of time and
# space. So you will have to be creative to compute an optimal solution. One idea is to go back to a recursive
# implementation, solving subproblems --- and, of course, caching the results to avoid redundant work --- only on
# an "as needed" basis. Also, be sure to think about appropriate data structures for storing and looking up
# solutions to subproblems.
#
# In the box below, type in the value of the optimal solution.
#
# ADVICE: If you're not getting the correct answer, try debugging your algorithm using some small test cases. And
# then post them to the discussion forum!

# Read in data
values, weights, max_capacity = read_objects(path='week-10/knapsack_big.txt')

# Parameters and W (number of items and maximum capacity of knapsack)
n, W = len(values), max_capacity

# Solve the knapsack problem using the algorithm from class
array = knapsack(values=values, weights=weights, W=max_capacity, verbose=True)

# The value of the optimal solution is 4243395
#   CHECK: CORRECT!
print(array[n, W])
