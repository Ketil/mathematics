'''This module contains classes for working with fields'''

import numpy


def conway():
    '''Returns a list of conway polynomials for field GF(2**m) for
    1 <= m <= 14

    You should consider the binary representation of the integers and use them
    as coefficient in the polynomial. E.g. 3 = 2**1 + 2**0 -> x + 1 and
    19 = 16 + 2 + 1 = 2**4 + 2**1 + 2**0 -> x**4 +  x + 1
    '''
    return [3, 7, 11, 19, 37, 91, 131, 285, 529, 1135, 2053, 4331, 8219, 16553]


def get_field_two(exponent):
    '''Returns field of size 2**exponent'''
    return FieldTwo(exponent, conway()[exponent-1])

class FieldTwo():
    '''Class containing logic for field with prime p=2

    The exponential representation is nonstandard in that the additive zero
    element is represented as 0.

    elements is a list of elements in the polynomial representation, ordered by
    the exponential representation

    pol_to_element is a list of elements in exponential representation ordered
    by the polynomial representation
    '''
    def __init__(self, exponent, reducing_polynomial=None, elements=None, symbol='α'):
        '''Requires reducing_polynomial or elements'''
        self.order = 1 << exponent
        self.exponent = exponent
        self.symbol = symbol

        self.numpy_add = numpy.vectorize(self.add)
        self.numpy_sub = self.numpy_add
        self.numpy_mult = numpy.vectorize(self.mult)
        if elements is not None:
            self.elements = elements
        else:
            self.elements = self.order * [0]
            self.elements[0] = 0
            self.elements[1] = 2

            size = 2
            while size < self.order:
                new_element = self.elements[size-1] << 1
                if new_element >= self.order:
                    new_element = new_element ^ reducing_polynomial
                self.elements[size] = new_element
                size += 1
        self.pol_to_element = self.order * [0]
        for i, j in enumerate(self.elements):
            self.pol_to_element[j] = i
        self.element_length = len(str(self.order)) + 2

    def polystring(self, poly, latex=False):
        '''Makes a string of a polynomial in the field'''
        if poly == 0:
            return '0'.center(self.element_length)
        if poly == 1:
            return '1'.center(self.element_length)
        if poly == 2:
            return self.symbol.center(self.element_length)
        if poly == -1:
            return 'err'.center(self.element_length)
        if latex:
            return '{}^{{{}}}'.format(self.symbol, self.pol_to_element[poly]).center(
                self.element_length)
        return '{}^{}'.format(self.symbol, self.pol_to_element[poly]).center(
            self.element_length)

    def one(self):
        '''Returns the one element of the field'''
        return self.elements[-1]

    def zero(self):
        '''Returns the zero element of the field'''
        return self.elements[0]

    def sum(self, iterable):
        '''Returns the sum of a sequence'''
        mysum = self.zero()
        for item in iterable:
            mysum = self.add(mysum, item)
        return mysum

    @staticmethod
    def add(first, second):
        '''Adds two FieldElement objects in this field'''
        return first ^ second

    @staticmethod
    def sub(first, second):
        '''Subtracts second from first in this field'''
        return first ^ second

    def __iter__(self):
        return iter(self.elements.items())

    def mult(self, first, second):
        '''Multiplies two FieldElement objects in this field'''
        if first == 0 or second == 0:
            return self.elements[0]
        return self.elements[
            (-1 + self.pol_to_element[first] + self.pol_to_element[second])
            % (self.order-1)
            + 1]

    def inverse(self, element):
        '''Returns the inverse of an element if it exist, or raises an
        exception'''
        if element == 0:
            raise ValueError("0 element doesn't have multiplicative inverse")
        if element == 1:
            return element
        elem = self.elements[self.order - self.pol_to_element[element] - 1]
        return elem
