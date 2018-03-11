import numpy as np
import pandas as pd


def int2list(num, size=0):
    numlist = [int(digit) for digit in str(num)]

    return [0]*(size-len(numlist)) + numlist


class Integer(int):
    def __init__(self, n):
        super(int, self).__init__()

        # Store the integers as digits
        self.digits = [int(i) for i in str(n)]
        self.digits.reverse()

    def __getitem__(self, index):
        return self.digits[index]


def list2Integer(x):
    n = len(x)

    value = sum([x[i]*10**i for i in range(n)])

    return Integer(value)

    # def __add__(self, other):
    #     return Integer(int.__add__(int(self), other))
    #
    # def __sub__(self, other):
    #     return Integer(int.__sub__(int(self), other))
    #
    # def __mul__(self, other):
    #     return Integer(int.__mul__(int(self), other))


class GradeSchoolMath:
    def __init__(self):
        self.operations = 0
        self.number = Integer(0)
        self.other = Integer(0)

    def add(self, x, y):
        # Reset the number of operations performed to zero
        self.operations = 0

        # Reset number and other to x and y
        self.number = Integer(x)
        self.other = Integer(y)

        size = max(len(self.number.digits), len(self.other.digits))
        slist = [0]*size
        carry = 0

        for i in range(size):
            try:
                xi = self.number[i]
            except IndexError:
                xi = 0

            try:
                yi = self.other[i]
            except IndexError:
                yi = 0

            si = xi + yi + carry
            self.operations += 2

            slist[i] = si % 10
            self.operations += 1

            carry = si//10
            self.operations += 1

        if carry > 0:
            slist += [carry]
            self.operations += 1

        return list2Integer(slist), self.operations

    def multiply(self, x, y):
        # Reset the number of operations performed to zero
        self.operations = 0

        # Reset number and other to x and y
        # self.number will always be "on top" and self.other will always be "on bottom
        if x >= y:
            self.number = Integer(x)
            self.other = Integer(y)
        else:
            self.number = Integer(y)
            self.other = Integer(x)

        subproducts = []

        for i in range(len(self.other.digits)):
            carry = 0
            plist = [0]*i

            for j in range(len(self.number.digits)):
                yi = self.other[i]
                xj = self.number[j]

                pij = yi*xj + carry
                self.operations += 2

                plist.append(pij % 10)
                self.operations += 1

                carry = pij//10
                self.operations += 1

            if carry > 0:
                plist.append(carry)
                self.operations += 1

            subproducts.append(plist)

        product = sum([list2Integer(s) for s in subproducts])

        return product, self.operations

data = pd.DataFrame()

x_vec = np.random.randint(low=0, high=1000000, size=1000000)
y_vec = np.random.randint(low=0, high=1000000, size=1000000)

g = GradeSchoolMath()

opns = [g.multiply(x[i], y[i])[1] for i in range(len(x_vec))]

data['x'] = x_vec
data['y'] = y_vec
data['ops'] = opns

data.to_csv('week-1/integer_mult_data.csv', index=False)