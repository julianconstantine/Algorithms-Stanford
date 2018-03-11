def cubic_mult(X, Y):
    # Dimension of X, Y, Z (N x N matrices)
    N = len(X)

    # Output product Z
    Z = [[0]*N]*N

    # Number of operations performed
    operations = 0

    for i in range(N):
        for j in range(N):
            z_ij = 0

            for k in range(N):
                z_ij += X[i][k]*Y[k][j]
                operations += 1

            Z[i][j] = z_ij

    return Z, operations


def strassen_mult(X, Y):
    # Matrices are all N x N, where N = 2**k for some k
    N = len(X)

    # Output matrix product Z
    Z = [[0]*N]*N

    # Number of operations performed
    operations = 0

    def recursive_product(X, Y):
        n = len(X)

        A = X[0:(n/2)][0:(n/2)]
        B = X[0:(n/2)][(n/2):n]
        C = X[(n/2):n][0:(n/2)]
        D = X[(n/2):n][(n/2):n]

        E = Y[0:(n/2)][0:(n/2)]
        F = Y[0:(n/2)][(n/2):n]
        G = Y[(n/2):n][0:(n/2)]
        H = Y[(n/2):n][(n/2):n]

        if n > 2:
            P1 = recursive_product(X=A, Y=(F-H))
            P2 = recursive_product(X=(A+B), Y=H)
            P3 = recursive_product(X=(C+D), Y=E)

        else:


        return P1, P2, P3, P4, P5, P6, P7




