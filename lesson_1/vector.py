import math
from decimal import Decimal, getcontext
import numpy as np

getcontext().prec = 30


class Vector(object):
    CANNOT_NORMALIZE_ZERO_VECTOR = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'No unique parallel component'

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

    def angle_within(self, v, in_degrees=False):
        try:
            u1 = self.normalize()
            u2 = v.normalize()
            angle_in_radians = math.acos(np.clip(u1.dot(u2), -1.0, 1.0))
            if in_degrees:
                degrees_per_radian = 180. / math.pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e

    def is_parallel(self, v):
        return (self.is_zero() or
                v.is_zero() or
                self.angle_within(v) == 0 or
                self.angle_within(v) == math.pi)

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def is_orthogonal(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_parallel_to(self, basis):
        try:
            u = basis.normalize()
            weight = self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR:
                raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR)
            else:
                raise e


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
    print v1.is_orthogonal(v2)
    print v1.is_parallel(v2)
    print v1.is_parallel(v1)


def coding_vector_projections_quiz():
    v1 = Vector([3.039, 1.879])
    b1 = Vector([0.825, 2.036])
    print v1.component_parallel_to(b1)

    v2 = Vector([-9.88, -3.264, -8.159])
    b2 = Vector([-2.155, -9.353, -9.473])
    print v2.component_orthogonal_to(b2)

    v3 = Vector([3.009, -6.172, 3.692, -2.51])
    b3 = Vector([6.404, -9.144, 2.759, 8.718])
    vpar = v3.component_parallel_to(b3)
    vort = v3.component_orthogonal_to(b3)
    print vpar
    print vort


def checking_parallel_orthogonal_quiz():
    v1 = Vector([-7.579, -7.88])
    w1 = Vector([22.737, 23.64])
    v2 = Vector([-2.029, 9.97, 4.172])
    w2 = Vector([-9.231, -6.639, -7.245])
    v3 = Vector([-2.328, -7.284, -1.214])
    w3 = Vector([-1.821, 1.072, -2.94])
    v4 = Vector([2.118, 4.827])
    w4 = Vector([0, 0])

    for i, j in zip([v1, v2, v3, v4], [w1, w2, w3, w4]):
        print(i.is_parallel(j))
        print(i.is_orthogonal(j))


def main():
    test()
    checking_parallel_orthogonal_quiz()
    coding_vector_projections_quiz()


if __name__ == '__main__':
    main()