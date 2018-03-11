###############################
#  PROGRAMMING ASSIGNMENT #6  #
###############################

# THE 2-SUM PROBLEM
# The goal of this problem is to implement a variant of the 2-SUM algorithm (covered in the Week 6 lecture on hash
# table applications).

# The file contains 1 million integers, both positive and negative (there might be some repetitions!).This is your
# array of integers, with the ith row of the file specifying the ith entry of the array.

# Your task is to compute the number of target values t in the interval [-10000,10000] (inclusive) such that there
# are distinct numbers x,y in the input file that satisfy x+y=t. (NOTE: ensuring distinctness requires a one-line
# addition to the algorithm from lecture.)

# Write your numeric answer (an integer between 0 and 20001) in the space provided.

# OPTIONAL CHALLENGE: If this problem is too easy for you, try implementing your own hash table for it. For example,
# you could compare performance under the chaining and open addressing approaches to resolving collisions.


class HashTable:
    def __init__(self):
        self.array = dict()

    def __getitem__(self, item):
        return item in self.array

    def __setitem__(self, key, value):
        self.array[key] = value

    def insert(self, keys):
        for key in keys:
            self.array[key] = True


def read_array():
    f = open('week-6/2sum_data.txt', mode='r')

    numbers = []
    lines = f.readlines(); f.close()

    for line in lines:
        number = int(line.split()[0])
        numbers.append(number)

    return numbers


def two_sum(numbers):
    HT = HashTable()

    HT.insert(numbers)

    pairs = []

    count = 0

    for t in range(-10000, 10001, 1):
        for x in numbers:
            if HT[t - x]:
                if x != t - x:
                    # Count only distinct pairs
                    pairs.append((x, t - x))
                    count += 1
                    break

        if t % 100 == 0:
            print(t)

    return pairs, count


###############
#  TEST CASE  #
###############

test_numbers = [
    68037543430,
    -21123414637,
    56619844751,
    59688006695,
    82329471587,
    21123414637,
    3,
    -60489726142,
    2,
    2,
    -32955448858,
    32955438858,
    53645918962,
    -44445057840,
    10793991159
]

pairs, count = two_sum(numbers=test_numbers)

print(pairs)
print(count)


####################
#  ACTUAL PROBLEM  #
####################

numbers = read_array()

pairs, count = two_sum(numbers=numbers)

# For problem 1, I get 427 pairs
#   CHECK: CORRECT!
print(pairs)
print(count)

