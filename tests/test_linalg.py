#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 13:59:00 2018

@author: ketil
"""

import numpy

from helper import RealField
from linalg import solve, simplify_full_rank


def test_floating0():
    '''testcase floating 0'''
    mat = numpy.array([[3., 3., 3.], [3., 4., 5.], [1., 5., 6.]])
    # X = numpy.array([1, 2, 3])
    vec = numpy.array([18., 26., 29.])

    sol = numpy.array([1., 2., 3.])
    sol2, rank = solve(mat, vec, field=RealField)
    #sol2, rank = solve(mat, vec, field=RealField)
    
    for i, val in enumerate(sol2):
        assert sol[i] - val < 1e-14
    assert rank == 3


def test_floating1():
    '''testcase floating1'''
    mat = numpy.array([[3., 3., 3., 6.], [3., 4., 5., 6.], [1., 5., 6., 2.]])
    vec = numpy.array([42., 50., 37.])

    sol = [-1, 2, 3, -1]
    sol2, rank = solve(mat, vec, field=RealField)
    mat = mat.round(decimals=14)
    sol2, rank = solve(mat, vec, field=RealField)
    #sol2 = numpy.array(simplify_full_rank(sol2), dtype=float)
    for i, val in enumerate(sol2):
        assert sol[i] - val < 1e-14
    assert rank == 3


def test_gf8_matrix():
    '''testcase GF8'''
    import algebra
    field = algebra.get_field_two(3)

    mat = numpy.array([[3, 2], [1, 2]])
    vec = numpy.array([3, 2])
    sol = numpy.array([5, 6])

    sol2, rank = solve(mat, vec, field=field)
    for i, val in enumerate(sol2):
        assert sol[i] == val
    assert rank == 2


def test_floating2():
    '''testcase 2'''
    mat = numpy.array([[3., 0., 0.], [0., 6., 0.], [0., 8., 0]])
    vec = numpy.array([3., 6., 8])

    sol = numpy.array([1., 1., 0.])
    _, rank = solve(mat, vec, RealField)

    assert all(sol == [1., 1., 0.])
    assert rank == 2


def test_rank_2():
    '''testcase rank_2'''

    vec = numpy.array([14., 14., 20.])
    mat = numpy.array([[1., 2., 3.], [1., 2., 3.], [2., 3., 4.]])
    _ = numpy.array((1., 2., 3.))
    _, rank = solve(mat, vec, RealField)
#    assert all(sol == sol2)
    assert rank == 2


if __name__ == '__main__':
    test_floating0()
    test_floating1()
    test_floating2()
    test_gf8_matrix()
    test_rank_2()
