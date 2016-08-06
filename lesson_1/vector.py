import math
from decimal import Decimal, getcontext
import numpy as np

getcontext().prec = 30


class Vector(object):
    CANNOT_NORMALIZE_ZERO_VECTOR = 'Cannot normalize the zero vector'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __iter__(self):
        return iter(self.coordinates)

    def __getitem__(self, index):
        return self.coordinates[index]

    def __setitem__(self, index, value):
        self.coordinates[index] = value

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        return Vector([x + y for x, y in zip(self.coordinates, v.coordinates)])

    def minus(self, v):
        return Vector([x - y for x, y in zip(self.coordinates, v.coordinates)])

    def __mul__(self, other):
        if isinstance(other, list):
            pass
        else:
            return Vector([x * Decimal(other) for x in self.coordinates])

    def magnitude(self):
        return Decimal(math.sqrt(sum([i ** 2 for i in self.coordinates])))

    def normalize(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0') / magnitude)
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR)

    def times_scalar(self, c):
        return Vector([Decimal(c) * x for x in self.coordinates])

    def dot(self, v):
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])


def test():
    v1 = Vector([8.218, -9.341])
    v2 = Vector([-1.129, 2.111])
    v3 = Vector([7.119, 8.215])
    v4 = Vector([-8.223, 0.878])
    v5 = Vector([1.671, -1.012, -0.318])
    v = v1.normalize()

    print(v1.plus(v2))
    print(v3.minus(v4))
    print(v5 * 7.41)
    print int(math.ceil(v.magnitude())) == 1
    print Vector([-0.221, 7.437]).magnitude()
    print Vector([8.813, -1.331, -6.247]).magnitude()
    print Vector([5.581, -2.136]).normalize()
    print Vector([1.996, 3.108, -4.554]).normalize()


def main():
    test()


if __name__ == '__main__':
    main()