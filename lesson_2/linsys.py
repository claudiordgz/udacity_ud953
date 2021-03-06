from decimal import Decimal, getcontext
from copy import deepcopy

from lesson_1 import Vector
from lesson_2 import Plane

getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def swap_rows(self, row1, row2):
        self[row1], self[row2] = self[row2], self[row1]

    def multiply_coefficient_and_row(self, coefficient, row):
        n = self[row].normal_vector
        k = self[row].constant_term

        new_normal_vector = n.times_scalar(coefficient)
        new_constant_term = k * coefficient

        self[row] = Plane(normal_vector=new_normal_vector,
                          constant_term=new_constant_term)

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        n1 = self[row_to_add].normal_vector
        n2 = self[row_to_be_added_to].normal_vector
        k1 = self[row_to_add].constant_term
        k2 = self[row_to_be_added_to].constant_term

        new_normal_vector = n1.times_scalar(coefficient).plus(n2)
        new_constant_terms = (k1 * coefficient) + k2

        self[row_to_be_added_to] = Plane(normal_vector=new_normal_vector,
                                         constant_term=new_constant_terms)

    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices

    def __len__(self):
        return len(self.planes)

    def __getitem__(self, i):
        return self.planes[i]

    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def compute_triangular_form(self):
        system = deepcopy(self)
        num_equations = len(system)
        num_variables = system.dimension

        j = 0
        for i in range(num_equations):
            while j < num_variables:
                c = MyDecimal(system[i].normal_vector[j])
                if c.is_near_zero():
                    swap_succeeded = system.swap_with_row_below_for_nonzero_coefficient_if_able(i,j)
                    if not swap_succeeded:
                        j += 1
                        continue

                system.clear_coefficients_below(i, j)
                i += 1
                break

        return system

    def swap_with_row_below_for_nonzero_coefficient_if_able(self, row, col):
        num_equations = len(self)
        for k in range(row+1, num_equations):
            coefficient = MyDecimal(self[k].normal_vector[col])
            if not coefficient.is_near_zero():
                self.swap_rows(row, k)
                return True
        return False

    def clear_coefficients_below(self, row, col):
        num_equations = len(self)
        beta = MyDecimal(self[row].normal_vector[col])

        for k in range(row+1, num_equations):
            n = self[k].normal_vector
            gamma = n[col]
            alpha = -gamma/beta
            self.add_multiple_times_row_to_row(alpha, row, k)

    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


def initial_code():
    p0 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
    p1 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
    p2 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
    p3 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')

    s = LinearSystem([p0,p1,p2,p3])

    print s.indices_of_first_nonzero_terms_in_each_row()
    print '{},{},{},{}'.format(s[0],s[1],s[2],s[3])
    print len(s)
    print s

    s[0] = p1
    print s

    print MyDecimal('1e-9').is_near_zero()
    print MyDecimal('1e-11').is_near_zero()


def coding_row_operations_quiz():
    p0 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p1 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    p2 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    p3 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')

    s = LinearSystem([p0, p1, p2, p3])
    s.swap_rows(0, 1)
    s0p1 = s[0] == p1
    s1p0 = s[1] == p0
    s2p2 =s[2] == p2
    s3p3 = s[3] == p3
    if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
        print 'test case 1 failed'

    s.swap_rows(1, 3)
    if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
        print 'test case 2 failed'

    s.swap_rows(3, 1)
    if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
        print 'test case 3 failed'

    s.multiply_coefficient_and_row(1, 0)
    if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
        print 'test case 4 failed'

    s.multiply_coefficient_and_row(-1, 2)
    if not (s[0] == p1 and
                    s[1] == p0 and
                    s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                    s[3] == p3):
        print 'test case 5 failed'

    s.multiply_coefficient_and_row(10, 1)
    if not (s[0] == p1 and
                    s[1] == Plane(normal_vector=Vector(['10', '10', '10']), constant_term='10') and
                    s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                    s[3] == p3):
        print 'test case 6 failed'

    s.add_multiple_times_row_to_row(0, 0, 1)
    if not (s[0] == p1 and
                    s[1] == Plane(normal_vector=Vector(['10', '10', '10']), constant_term='10') and
                    s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                    s[3] == p3):
        print 'test case 7 failed'

    s.add_multiple_times_row_to_row(1, 0, 1)
    if not (s[0] == p1 and
                    s[1] == Plane(normal_vector=Vector(['10', '11', '10']), constant_term='12') and
                    s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                    s[3] == p3):
        print 'test case 8 failed'

    s.add_multiple_times_row_to_row(-1, 1, 0)
    if not (s[0] == Plane(normal_vector=Vector(['-10', '-10', '-10']), constant_term='-10') and
                    s[1] == Plane(normal_vector=Vector(['10', '11', '10']), constant_term='12') and
                    s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                    s[3] == p3):
        print 'test case 9 failed'


def triangular_form_quiz():
    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='2')
    s = LinearSystem([p1, p2])
    t = s.compute_triangular_form()
    if not (t[0] == p1 and
                    t[1] == p2):
        print 'test case 1 failed'

    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='2')
    s = LinearSystem([p1, p2])
    t = s.compute_triangular_form()
    if not (t[0] == p1 and
                    t[1] == Plane(constant_term='1')):
        print 'test case 2 failed'

    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    p3 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    p4 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
    s = LinearSystem([p1, p2, p3, p4])
    t = s.compute_triangular_form()
    if not (t[0] == p1 and
                    t[1] == p2 and
                    t[2] == Plane(normal_vector=Vector(['0', '0', '-2']), constant_term='2') and
                    t[3] == Plane()):
        print 'test case 3 failed'

    p1 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')
    p3 = Plane(normal_vector=Vector(['1', '2', '-5']), constant_term='3')
    s = LinearSystem([p1, p2, p3])
    t = s.compute_triangular_form()
    if not (t[0] == Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2') and
                    t[1] == Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1') and
                    t[2] == Plane(normal_vector=Vector(['0', '0', '-9']), constant_term='-2')):
        print 'test case 4 failed'


def main():
    #initial_code()
    coding_row_operations_quiz()
    triangular_form_quiz()

if __name__ == '__main__':
    main()
