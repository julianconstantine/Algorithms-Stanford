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
    # Read array from text file

    f = open(path, mode='r')
    array = f.readlines()
    f.close()

    for i in range(len(array)):
        # Remove newline characters and convert to integer
        array[i] = int(array[i].split()[0])

    return array


class QuickSort:
    def __init__(self, A, pivot='first'):
        self.array = A
        self.comparisons = 0
        self.pivot = pivot

    def choosePivot(self, left, right):
        if self.pivot == 'last':
            self.array[left], self.array[right] = self.array[right], self.array[left]
        elif self.pivot == 'median':
            midpoint = left + (right-left)//2

            data = {left: self.array[left], midpoint: self.array[midpoint], right: self.array[right]}

            median = sorted(data, key=data.get)[1]

            self.array[left], self.array[median] = self.array[median], self.array[left]
        else:
            # Do nothing
            pass

        return self.array[left]

    def partition(self, left, right):
        p = self.choosePivot(left, right)

        i = left + 1

        for j in range(left+1, right+1):
            # print(j)
            if self.array[j] < p:
                self.array[i], self.array[j] = self.array[j], self.array[i]
                i += 1

        self.array[left], self.array[i-1] = self.array[i-1], self.array[left]

        return i-1

    def sort(self, left=0, right=None):
        if right is None:
            # Initialize first sweep
            right = len(self.array) - 1

            # Number of comparisons is (array size) - 1
            self.comparisons += len(self.array) - 1

        if right - left <= 1:
            pass
        else:
            mid = self.partition(left=left, right=right)
            # print(left, mid, right)

            self.sort(left=left, right=mid-1)

            if mid - left - 1 >= 0:
                # If the left half is non-empty, make (left size) - 1 comparisons
                self.comparisons += (mid-left-1)

            self.sort(left=mid+1, right=right)

            if right - mid - 1 >= 0:
                # If the right half is non-empty, make (right size) - 1 comparisons
                self.comparisons += (right-mid-1)


################
#  TEST CASES  #
################

# Test cases for using first element as pivot
array10 = read_array('week-2/test10.txt')
q = QuickSort(array10)
q.sort()
print(q.comparisons)  # 25

array100 = read_array('week-2/test100.txt')
q = QuickSort(array100)
q.sort()
print(q.comparisons)  # 615

array1000 = read_array('week-2/test1000.txt')
q = QuickSort(array1000)
q.sort()
print(q.comparisons)  # 10,297


# Test cases for using last element as pivot
array10 = read_array('week-2/test10.txt')
q = QuickSort(array10, 'last')
q.sort()
print(q.comparisons)  # 29

array100 = read_array('week-2/test100.txt')
q = QuickSort(array100, 'last')
q.sort()
print(q.comparisons)  # 587

array1000 = read_array('week-2/test1000.txt')
q = QuickSort(array1000, 'last')
q.sort()
print(q.comparisons)  # 10,184


# Test cases for using median-of-three pivot
array10 = read_array('week-2/test10.txt')
q = QuickSort(array10, 'median')
q.sort()
print(q.comparisons)  # 21

array100 = read_array('week-2/test100.txt')
q = QuickSort(array100, 'median')
q.sort()
print(q.comparisons)  # 518

array1000 = read_array('week-2/test1000.txt')
q = QuickSort(array1000, 'median')
q.sort()
print(q.comparisons)  # 8,921


# PROBLEM #1
# For the first part of the programming assignment, you should always use the first element of the array as the pivot
# element.

array = read_array(path='week-2/QuickSort.txt')
q = QuickSort(array)
q.sort()

# QuickSort makes 162,085 comparisons when using the first element as the pivot
#   CHECK: CORRECT!
print(q.comparisons)

# PROBLEM #2
# Compute the number of comparisons (as in Problem 1), always using the final element of the given array as the pivot
# element. Again, be sure to implement the Partition subroutine exactly as it is described in the video lectures.

# Recall from the lectures that, just before the main Partition subroutine, you should exchange the pivot element
# (i.e., the last element) with the first element.

array = read_array(path='week-2/QuickSort.txt')
q = QuickSort(array, pivot='last')
q.sort()

# QuickSort makes 164,123 comparisons when using the last element as the pivot
#   CHECK: CORRECT!
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

array = read_array(path='week-2/QuickSort.txt')
q = QuickSort(array, pivot='median')
q.sort()

# QuickSort makes 138,382 comparisons when using the median-of-3 method of choosing a pivot
#   CHECK: CORRECT!
print(q.comparisons)
