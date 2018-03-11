# Implement the optimal binary search tree algorithm from lecture

import numpy as np

weights = {1: 0.05, 2: 0.4, 3: 0.08, 4: 0.04, 5: 0.1, 6: 0.1, 7: 0.23}
# weights = {1: 0.2, 2: 0.05, 3: 0.17, 4: 0.1, 5: 0.2, 6: 0.03, 7: 0.25}

n = len(weights)

# Initialize an (n+1) x (n+1) array of zeros (to support 1-based indexing)
# This means that the first row and first column will remain filled with zeros at the end of the algorithm
A = np.zeros((n+1, n+1))

for s in range(n):
    print("Iteration: %i" % s)

    for i in range(1, n - s + 1):
        print(i)
        sum_p = sum([weights[k] for k in range(i, i+s+1)])

        min_list = []

        for r in range(i, i+s+1):
            # try:
            if r-1 > 0:
                A_r1 = A[i, r-1]
            # except IndexError:
            else:
                A_r1 = 0

            # try:
            if r+1 <= n:
                A_r2 = A[r+1, i+s]
            # except IndexError:
            else:
                A_r2 = 0

            min_list.append(sum_p + A_r1 + A_r2)

            A[i, i+s] = min(min_list)

ans = A[1, n]

# The final answer is 2.18
#   CHECK: CORRECT!
print(ans)
