###############################
#  PROGRAMMING ASSIGNMENT #1  #
###############################

# COUNTING INVERSIONS
# The file integerArray.txt contains all of the 100,000 integers between 1 and 100,000 (inclusive) in some order,
# with no integer repeated.
#
# Your task is to compute the number of inversions in the file given, where the ith row of the file indicates the ith
# entry of an array.
#
# Because of the large size of this array, you should implement the fast divide-and-conquer algorithm covered in the
# video lectures.
#
# The numeric answer for the given input file should be typed in the space below.
#
# So if your answer is 1198233847, then just type 1198233847 in the space provided without any space / commas / any
# other punctuation marks. You can make up to 5 attempts, and we'll use the best one for grading.
#
# (We do not require you to submit your code, so feel free to use any programming language you want --- just type the
# final numeric answer in the following space.)

# Read in integerArray.txt
f = open('week-1/integerArray.txt', mode='r')
array = f.readlines(); f.close()

for i in range(len(array)):
    # Replace all the newline characters and convert to integer
    array[i] = int(array[i].split()[0])


# Helper function to merge arrays B and C and count up the number of split inversions
#   INPUT: Arrays B and C, total length (of both arrays) n
#   OUTPUT: Sorted array D (merged from A and B), number of split inversions

def mergeAndCountSplitInversions(B, C, n):
    A = B + C

    if n == 1:
        return A, 0
    else:
        print(n)
        i, j = 0, 0

        # B = A[0:(n//2)]
        # C = A[(n//2):n]

        # Initialize new list for D
        D = [0]*n

        num_split_inv = 0

        for k in range(n):
            # print('n: ', n)
            # print('i: ', i, 'j: ', j)
            # print('len(B): ', len(B), 'len(C): ', len(C))

            if i < len(B) and j < len(C):
                # print(i, j, B, C)
                if B[i] < C[j]:
                    # Copy the ith element of B if it is smaller than the jth element of C
                    D[k] = B[i]
                    i += 1
                else:
                    # Else there are split inversions, so copy the jth element of C
                    D[k] = C[j]
                    j += 1

                    # The number of split inversions is equal to the number of elements remaining in the array B
                    num_split_inv += len(B) - i
            elif i >= len(B) and j < len(C):
                # END CASE: We have copied over all the elements of B (but not C)
                D[k] = C[j]
                j += 1
            else:
                # END CASE: We have copied over all the elements of C (but not B)
                D[k] = B[i]
                i += 1

        return D, num_split_inv


# Main function to sort an array A and count up the number of inversions
#   INPUT: Array a, length n
#   OUTPUT: Sorted array D, number of inversions

def sortAndCountInversions(A, n):
    if n == 1:
        return A, 0
    else:
        B = A[0:(n//2)]
        C = A[(n//2):n]

        # Sort B and C and count up the number of inversions
        B_sorted, x = sortAndCountInversions(B, len(B))
        C_sorted, y = sortAndCountInversions(C, len(C))

        # Merge the (now-sorted) subarrays B and C
        D, z = mergeAndCountSplitInversions(B_sorted, C_sorted, n)

        return D, x + y + z

# Test for an array with five inversions:
#   (3, 2), (5, 2), (5, 4), (6, 2), (6, 4)
A = [1, 3, 5, 6, 2, 4]

# We get five inversions, as desired
sortAndCountInversions(A, 6)


# Sort the array of 100,000 integers and count the number of inversions
sortedArray, numInversions = sortAndCountInversions(array, len(array))

# There are 2,407,905,288 inversions in the array
#   CHECK: CORRECT!
print(numInversions)