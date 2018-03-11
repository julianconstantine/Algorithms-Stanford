import random


# Linear-time algorithm to find optimal value of WIS
def linearWIS(G):
    # Initialize an array of zeroes
    A = [0]*len(G)

    # Initialize a[1] to be weights[1]
    A[1] = G[1]

    # Iterate through weights and add to WIS
    for i in range(2, len(G)):
        A[i] = max(A[i-1], A[i-2] + G[i])

    return A


# Linear-time reconstruction algorithm to find optimal WIS
def reconstructWIS(G, A):
    S = set()

    # Initialize i to the final index of the array A
    i = len(A) - 1

    while i >= 1:
        if A[i-1] >= A[i-2] + G[i]:
            # Case 1 wins
            i -= 1
        else:
            # Case 2 wins, add v_i to S
            S = S.union({i})
            i -= 2

    return S


# Test graph
test_vertices = list(range(5))
test_weights = [1, 5, 1, 1, 5]

testGraph = {test_vertices[i]: test_weights[i] for i in range(5)}

# Want to get 10
#   CHECK: CORRECT!
testArray = linearWIS(testGraph)
print(testArray[-1])

# Want to get {1, 4} (corresponds to the vertices with weight 5)
#   CHECK: CORRECT!
print(reconstructWIS(G=testGraph, A=testArray))


# Generate a random path graph
vertices = list(range(100))
weights = random.sample(population=list(range(10000)), k=100)

pathGraph = {vertices[i]: weights[i] for i in range(100)}

# Print out the optimal value
print(linearWIS(pathGraph)[-1])