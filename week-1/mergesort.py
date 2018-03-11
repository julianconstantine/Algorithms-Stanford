def merge(B, C):
    A = B + C
    n = len(A)

    if n == 1:
        return A, 0
    else:
        print(n)
        i, j = 0, 0

        # Initialize new list for D
        D = [0]*n

        num_ops = 0

        for k in range(n):
            # One incrementation (in k) per iteration
            num_ops += 1

            print('------------------')
            print('Iteration: ', k)
            print(B, C)
            print(D)
            print('------------------')

            if i < len(B) and j < len(C):
                if B[i] < C[j]:
                    # Copy the ith element of B if it is smaller than the jth element of C
                    D[k] = B[i]
                    i += 1

                    # One assignment, one incrementation
                    num_ops += 2
                else:
                    # Else there are split inversions, so copy the jth element of C
                    D[k] = C[j]
                    j += 1

                    # One assignment, one incrementation
                    num_ops += 2
            elif i >= len(B) and j < len(C):
                # END CASE: We have copied over all the elements of B (but not C)
                D[k] = C[j]
                j += 1

                # One assignment, one incrementation
                num_ops += 2
            else:
                # END CASE: We have copied over all the elements of C (but not B)
                D[k] = B[i]
                i += 1

                # One assignment, one incrementation
                num_ops += 2

        print('------------------')
        print('Iteration: ', 'FINAL')
        print(B, C)
        print(D)
        print('------------------')

        return D, num_ops


def mergesort(A):
    n = len(A)

    if n == 1:
        return A, 0
    else:
        B = A[0:(n//2)]
        C = A[(n//2):n]

        B_sorted, x = mergesort(B)
        C_sorted, y = mergesort(C)

        D, z = merge(B_sorted, C_sorted)

        return D, x + y + z






