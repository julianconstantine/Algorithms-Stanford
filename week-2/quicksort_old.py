###############################
#  PROGRAMMING ASSIGNMENT #2  #
###############################

# IMPLEMENTING QUICKSORT
# The file QuickSort.txt contains all of the integers between 1 and 10,000 (inclusive, with no repeats) in unsorted
# order. The integer in the ith row of the file gives you the ith entry of an input array.

# Your task is to compute the total number of comparisons used to sort the given input file by QuickSort. As you
# know, the number of comparisons depends on which elements are chosen as pivots, so we'll ask you to explore three
# different pivoting rules.

# You should not count comparisons one-by-one. Rather, when there is a recursive call on a subarray of length m,
# you should simply add m−1 to your running total of comparisons. (This is because the pivot element is compared to
# each of the other m−1 elements in the subarray in this recursive call.)

# WARNING: The Partition subroutine can be implemented in several different ways, and different implementations can
# give you differing numbers of comparisons. For this problem, you should implement the Partition subroutine exactly
# as it is described in the video lectures (otherwise you might get the wrong answer).


def read_array(path):
    # Read in input file
    f = open(path, mode='r')
    array = f.readlines()
    f.close()

    for i in range(len(array)):
        # Remove newline characters and convert to integer
        array[i] = int(array[i].split()[0])

    return array


def partition(A, l, r):
    p = A[l]
    i = l + 1

    for j in range(l+1, r):
        if A[j] < p:
            A[i], A[j] = A[j], A[i]
            i += 1

    A[l], A[i-1] = A[i-1], A[l]

    return i


def quickSort(A, n, left=0, right=-1):
    if right < 0:
        right = n

    if right - left <= 1:
        pass
    else:
        # p = choosePivot(A, n)
        p = A[0]

        mid = partition(A, l=left, r=right)

        quickSort(A=A, n=n, left=left, right=mid)
        quickSort(A=A, n=n, left=mid, right=right)


# PROBLEM #1
# For the first part of the programming assignment, you should always use the first element of the array as the pivot
# element.

class QuickSort:
    def __init__(self, A, ptype='first', vb=False):
        self.array = A
        self.comparisons = 0
        self.recursions = 0
        self.pivot_type = ptype
        self.verbose = vb

    def partition(self, left, right):
        if self.pivot_type == 'last':
            # If using the last element, swap it into place
            self.array[left], self.array[right] = self.array[right], self.array[left]
        elif self.pivot_type == 'median':
            midpoint = (right - left)//2

            arr = {left: self.array[left],
                   midpoint: self.array[midpoint],
                   right: self.array[right]}

            median = sorted(arr, key=arr.get)[2]

            # Swap the leftmost element with the median element of arr
            self.array[left], self.array[median] = self.array[median], self.array[left]

        # Select pivot point (now in leftmost position)
        p = self.array[left]

        i = left + 1

        for j in range(left + 1, right + 1):
            self.comparisons += 1

            if self.array[j] < p:
                self.array[i], self.array[j] = self.array[j], self.array[i]
                i += 1

        self.array[left], self.array[i-1] = self.array[i-1], self.array[left]

        return i

    def sort(self, left, right):
        if right - left <= 1:
            pass
        else:
            mid = self.partition(left=left, right=right)

            if self.verbose:
                print(left, mid, right)
                print(self.array)

            # Sort left half of array
            # print(left, right)
            self.sort(left=left, right=max(mid-1, 0))
            # self.comparisons += (mid-1) - left

            # Sort right half of array
            # print(left, right)
            self.sort(left=mid, right=right)
            # self.comparisons += right - mid

            self.recursions += 1

# Tests
array10 = read_array('week-2/test10.txt')
n = len(array10)
q = QuickSort(array10, 'first', vb=True)
q.sort(left=0, right=n-1)
q.array
q.comparisons



array = read_array('week-2/QuickSort.txt')
n = len(array)
q = QuickSort(array, 'first')
q.sort(left=0, right=n-1)

print(q.comparisons)


# PROBLEM #2
# Compute the number of comparisons (as in Problem 1), always using the final element of the given array as the pivot
# element. Again, be sure to implement the Partition subroutine exactly as it is described in the video lectures.

# Recall from the lectures that, just before the main Partition subroutine, you should exchange the pivot element
# (i.e., the last element) with the first element.

array = read_array()
n = len(array)
q = QuickSort(array, 'last', vb=True)
q.sort(left=0, right=n-1)

print(q.comparisons)

# PROBLEM #3
# Compute the number of comparisons (as in Problem 1), using the "median-of-three" pivot rule. [The primary motivation
# behind this rule is to do a little bit of extra work to get much better performance on input arrays that are nearly
# sorted or reverse sorted.] In more detail, you should choose the pivot as follows. Consider the first, middle,
# and final elements of the given array. (If the array has odd length it should be clear what the "middle" element
# is; for an array with even length 2k, use the kth element as the "middle" element. So for the array 4 5 6 7, the
# "middle" element is the second one ---- 5 and not 6!) Identify which of these three elements is the median (i.e., the
# one whose value is in between the other two), and use this as your pivot. As discussed in the first and second parts
# of this programming assignment, be sure to implement Partition exactly as described in the video lectures (including
# exchanging the pivot element with the first element just before the main Partition subroutine).

# Example: For the input array 8 2 4 5 7 1 you would consider the first (8), middle (4), and last (1) elements; since
# 4 is the median of the set {1,4,8}, you would use 4 as your pivot element.

# A careful analysis would keep track of the comparisons made in identifying the median of the three candidate
# elements. You should NOT do this. That is, as in the previous two problems, you should simply add m−1 to your
# running total of comparisons every time you recurse on a subarray with length m.

array = read_array()
q = QuickSort(array, 'median')
q.sort()


print(q.comparisons)