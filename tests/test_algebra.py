'''Pytest module for algebra'''

import algebra


def test_gf4():
    '''Alternative GF(4)'''
    field = algebra.FieldTwo(2, algebra.conway()[1])
    elements = field.elements

    assert field.add(elements[0], elements[2]) == elements[2]
    assert field.mult(elements[1], elements[2]) == elements[3]
    assert field.add(elements[2], elements[1]) == elements[3]
    assert field.mult(elements[2], elements[3]) == elements[2]
    assert field.mult(elements[3], elements[3]) == elements[3]


def test_gf1024():
    '''GF(1024)'''
    field = algebra.FieldTwo(10, algebra.conway()[9])
    elements = field.elements

    assert field.add(elements[600], elements[500]) == elements[469]
    assert field.mult(elements[600], elements[500]) == elements[77]


def test_gf16384():
    '''Alternative GF(16384)'''
    field = algebra.FieldTwo(14, algebra.conway()[13])
    elements = field.elements

    assert field.mult(elements[2684], elements[13700]) == elements[1]


if __name__ == '__main__':
    test_gf4()
