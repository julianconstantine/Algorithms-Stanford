###############################
#  PROGRAMMING ASSIGNMENT #6  #
###############################

# MEDIAN MAINTENANCE
# The goal of this problem is to implement the "Median Maintenance" algorithm (covered in the Week 5 lecture on heap
# applications). The text file contains a list of the integers from 1 to 10000 in unsorted order; you should treat this
# as a stream of numbers, arriving one by one. Letting x_i denote the ith number of the file, the kth median m_k is
# defined as the median of the numbers x_1, ..., x_k. (So, if k is odd, then mk is ((k + 1)/2)th smallest number among
# x_1, ..., x_k; if k is even, then m_k is the (k/2)th smallest number among x_1, ..., x_k.)

# In the box below you should type the sum of these 10000 medians, modulo 10000 (i.e., only the last 4 digits). That
# is, you should compute (m_1 + m_2 + m_3 + ... + m_10000) mod 10000.

# OPTIONAL EXERCISE: Compare the performance achieved by heap-based and search-tree-based implementations of the
# algorithm.

import heapq
import math


def read_array(path):
    f = open(path, mode='r')
    lines = f.readlines()
    f.close()

    numbers = []

    for line in lines:
        number = int(line.split()[0])
        numbers.append(number)

    return numbers


def median_maintenance(numbers, quiet=True):
    medians = []

    H_low = []
    H_high = []

    for i, n in enumerate(numbers):
        try:
            low_max = -heapq.nsmallest(1, H_low)[0]
        except IndexError:
            low_max = float('-inf')

        try:
            high_min = heapq.nsmallest(1, H_high)[0]
        except IndexError:
            high_min = float('inf')

        # print(low_max, high_min)
        # print(H_low, H_high)

        if n < low_max:
            # print("(1) Inserting %i into H_low with max element %f" % (n, low_max))
            heapq.heappush(H_low, -n)
        elif n > high_min:
            # print("(2) Inserting %i into H_high with min element %f" % (n, high_min))
            heapq.heappush(H_high, n)
        else:
            # print("(3) Inserting %i into H_low with max element %f" % (n, low_max))
            heapq.heappush(H_low, -n)

        if len(H_high) - len(H_low) > 1:
            # print("Swapped high to low")
            high_min = heapq.heappop(H_high)
            heapq.heappush(H_low, -high_min)
        elif len(H_low) - len(H_high) > 1:
            # print("Swapped low to high")
            low_max = -heapq.heappop(H_low)
            heapq.heappush(H_high, low_max)

        # Position of the median
        k = math.floor(i / 2)

        # print(k, i)
        # print([-h for h in H_low], H_high)

        if k > len(H_low) - 1:
            # print("Median from high")
            median = heapq.heappop(H_high)
            heapq.heappush(H_high, median)
        else:
            # print("Median from low")
            median = -heapq.heappop(H_low)
            heapq.heappush(H_low, -median)

        medians.append(median)

        if not quiet:
            print(n, median)

        # print("-------------------------------")

    return medians


###############
#  TEST CASE  #
###############

test_numbers = read_array(path='week-6/testMedian.txt')

test_medians = median_maintenance(numbers=test_numbers, quiet=False)

# The last four digits of the sum of the medians modulo 10,000 is 9335
#   CHECK: CORRECT!
sum(test_medians) % 10000


######################
#  HOMEWORK PROBLEM  #
######################

# numbers = test_numbers
numbers = read_array(path='week-6/Median.txt')

medians = median_maintenance(numbers=numbers)

# The last four digits of the sum of the medians are 1213
#   CHECK: CORRECT!
print("The sum of the 10,000 medians modulo 10,000 is %i" % (sum(medians) % 10000))
