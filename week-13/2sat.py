################################
#  PROGRAMMING ASSIGNMENT #13  #
################################

# In this assignment you will implement one or more algorithms for the 2SAT problem. Here are 6 different 2SAT
# instances:
#
# The file format is as follows. In each instance, the number of variables and the number of clauses is the same,
# and this number is specified on the first line of the file. Each subsequent line specifies a clause via its two
# literals, with a number denoting the variable and a "-" sign denoting logical "not". For example, the second
# line of the first data file is "-16808 75250", which indicates the clause "not x16808 or x75270"
#
# Your task is to determine which of the 6 instances are satisfiable, and which are unsatisfiable. In the box
# below, enter a 6-bit string, where the ith bit should be 1 if the ith instance is satisfiable, and 0 otherwise.
# For example, if you think that the first 3 instances are satisfiable and the last 3 are not, then you should
# enter the string 111000 in the box below.
#
# DISCUSSION: This assignment is deliberately open-ended, and you can implement whichever 2SAT algorithm you want.
# For example, 2SAT reduces to computing the strongly connected components of a suitable graph (with two vertices
# per variable and two directed edges per clause, you should think through the details). This might be an
# especially attractive option for those of you who coded up an SCC algorithm for my Algo 1 course. Alternatively,
# you can use Papadimitriou's randomized local search algorithm. (The algorithm from lecture is probably too
# slow as stated, so you might want to make one or more simple modifications to it --- even if this means
# breaking the analysis given in lecture --- to ensure that it runs in a reasonable amount of time.) A third
# approach is via backtracking. In lecture we mentioned this approach only in passing; see Chapter 9 of the
# Dasgupta-Papadimitriou-Vazirani book, for example, for more details.

from collections import defaultdict

import numpy as np

import datetime
import random
import math


def read_2sat_clauses(path):
    f = open(path, mode='r')
    data = f.readlines()
    f.close()

    clauses = []

    for line in data[1:]:
        x, y = line.split()

        clause = {}

        if x.startswith('-'):
            x = int(x.split('-')[1])
            clause[x] = False
        else:
            x = int(x)
            clause[x] = True

        if y.startswith('-'):
            y = int(y.split('-')[1])
            clause[y] = False
        else:
            y = int(y)
            clause[y] = True

        clauses.append(clause)

    return clauses


def compress(clauses):
    """
    Compress input size by dropping all clauses containing a variable the only appears once
    """

    counts = defaultdict(int)

    for clause in clauses:
        x, y = clause.keys()
        counts[x] += 1
        counts[y] += 1

    compressed_clauses = []

    for clause in clauses:
        x, y = clause.keys()

        if counts[x] > 1 and counts[y] > 1:
            compressed_clauses.append(clause)

    return compressed_clauses


def initialize_variable_assignment(clauses):
    variables = []

    for clause in clauses:
        x, y = clause.keys()

        variables += [x, y]

    unique_variables = list(set(variables))
    booleans = np.random.choice(a=[True, False], size=len(unique_variables))

    assignment = {x: booleans[i] for i, x in enumerate(unique_variables)}

    return assignment


def is_satisfied(clause, assignment):
    x, y = clause.keys()

    return clause[x] == assignment[x] or clause[y] == assignment[y]


def get_unsatisfied_clauses(clauses, assignment):
    # unsatisfied_clauses = []
    unsatisfied_clauses = set()

    for i, clause in enumerate(clauses):
        if not is_satisfied(clause, assignment):
            # unsatisfied_clauses.append(i)
            unsatisfied_clauses.add(i)

    return unsatisfied_clauses


def clause_map(clauses):
    lookup = defaultdict(list)

    for i, clause in enumerate(clauses):
        x, y = clause.keys()
        lookup[x] += [i]
        lookup[y] += [i]

    return lookup


raw_clauses = read_2sat_clauses(path='week-13/2sat6.txt')
clauses = compress(clauses=raw_clauses)
clause_neighbors = clause_map(clauses)

n = len(clauses)

satisfiable = False

for i in range(math.floor(math.log2(n))):
    assignment = initialize_variable_assignment(clauses)
    unsatisfied_clauses = set(get_unsatisfied_clauses(clauses, assignment))

    for j in range(2*n**2):
        num_unsatisfied = len(unsatisfied_clauses)

        if num_unsatisfied == 0:
            satisfiable = True
            break
        else:
            # Choose a random unsatisfied clauses (index)
            # u_index = math.floor(num_unsatisfied * np.random.random())

            index = random.choice(tuple(unsatisfied_clauses))
            # index = unsatisfied_clauses.pop()
            # unsatisfied_clauses.add(index)

            c = clauses[index]
            x, y = c.keys()

            if np.random.random() <= 0.5:
                z = x
            else:
                z = y

        neighbor_indices = clause_neighbors[z]
        # neighbors = {k: clauses[k] for k in neighbor_indices}

        assignment[z] = not assignment[z]

        if is_satisfied(c, assignment):
            unsatisfied_clauses.remove(index)

        for k in neighbor_indices:
            if is_satisfied(clauses[k], assignment):
                try:
                    unsatisfied_clauses.remove(k)
                except KeyError:
                    pass
            else:
                unsatisfied_clauses.add(k)

        if j % 10000 == 0:
            print(j, num_unsatisfied, datetime.datetime.now())

    if satisfiable:
        break

if satisfiable:
    print("SATISFIABLE")
else:
    print("UNSATISFIABLE")

# Yep, this is correct ...
# 1 is satisfiable
# 2 is ???
# 3 is satisfiablw
# 4 is satisfiable
# 5 is ???
# 6 is ???