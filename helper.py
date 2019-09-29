#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 14:50:57 2018

@author: ketil
"""
import numpy


class RealField():
    '''Temp class'''
    @classmethod
    def zero(cls):
        '''zero element'''
        return 0.0

    @classmethod
    def one(cls):
        '''one element'''
        return 1.0

    @classmethod
    def inverse(cls, element):
        '''inverse of element'''
        if element == 0:
            raise ValueError('0 is not invertible')
        return 1/element

    @classmethod
    def add(cls, first, second):
        '''Adds two elements in a field'''
        return first + second

    @classmethod
    def sub(cls, first, second):
        '''Subtracts second element from first in a field'''
        return first - second

    @classmethod
    def mult(cls, first, second):
        '''Multiplies two elements in a field'''
        return first * second

    def numpy_mult(first, second):
        '''Multiplies a vector with a scalar'''
        return first * second

    def numpy_sub(first, second):
        '''Subtracts a vector from another componentwise'''
        return first - second

