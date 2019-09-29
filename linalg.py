'''Module for linalg functions'''
import numpy

def reduce_rows(matrix, solution, field):
    '''row reduce a matrix in a field'''

    height, width = matrix.shape
    h_i = 0
    w_i = 0
    rank = 0
    while h_i < height and w_i < width:
        if matrix[h_i, w_i] != field.one():
            # Find best row to swap
            best = i = h_i
            while i < height - 1:
                i += 1
                if matrix[i, w_i] != field.zero():
                    if matrix[best, w_i] == field.zero():
                        best = i
                    elif matrix[i, w_i] == field.one():
                        best = i
                        i = height
            # Swap row h with best row
            if h_i != best:
                matrix[h_i, :], matrix[best, :] = (matrix[best, :],
                                                   matrix[h_i, :].copy())
                solution[h_i], solution[best] = solution[best], solution[h_i]

        # If column is only zeros we should move onwards to next column
        if matrix[h_i, w_i] != field.zero():
            rank += 1
            # Scale row so that we get 1 as leading coefficients
            if matrix[h_i, w_i] != field.one():
                inverse = field.inverse(matrix[h_i, w_i])
                matrix[h_i, :] = field.numpy_mult(
                        inverse,
                        matrix[h_i, :].copy())
                solution[h_i] = field.mult(solution[h_i], inverse)
            # Add row h to get lower triangular matrix
            for i in range(h_i+1, height):
                constant = matrix[i, w_i]
                solution[i] = field.sub(
                        solution[i],
                        field.mult(constant, solution[h_i]))
                for j in range(w_i, width):
                    matrix[i, j] = field.sub(matrix[i, j], field.mult(constant, matrix[h_i, j]))
            h_i += 1
        w_i += 1
    return rank

def reduce_upper_triangle(matrix, vec, rank, field):
    i = rank - 1


    for i in range(rank-1, -1, -1):
        # Remove multiples of leading coefficient from other equations
        j = 0
        while matrix[i, j] == 0 and j < len(matrix[0]):
            # Index of leading coefficient
            j += 1
        for i_2 in range(i):
#            if i_2 == 4:
#                print(matrix[:, 9:-9], vec[4])
            if matrix[i_2, j] != 0:
                vec[i_2] = field.sub(vec[i_2], field.mult(matrix[i_2, j], vec[i]))
                matrix[i_2, :] =  field.numpy_sub(matrix[i_2, :],                       field.numpy_mult(matrix[i_2, j], matrix[i, :]))


def solve(matrix, vec, field, x=None):
    '''solve matrix * x = vec'''
    if field is None:
        field = matrix[0, 0].field
    if x is None:
        x = numpy.full(len(matrix[0]), -1, dtype=type(field.zero()))
    else:
        for j, val in enumerate(x):
            if val != -1:
                for i, row in enumerate(matrix):
                    try:
                        vec[i] = field.sub(vec[i], field.mult(matrix[i, j], val))
                        matrix[i, j] = field.zero()
                    except IndexError as e:
                        print(e)
                        print('starting debugger')
                        import pdb; pdb.set_trace()
    height, width = matrix.shape

    # Reduce until last row or last column
    rank = reduce_rows(matrix, vec, field)

    reduce_upper_triangle(matrix, vec, rank, field)

   # solution = [(tuple(row), vec[i]) for i, row in enumerate(matrix)]
    for i, row in enumerate(matrix):
        coeff = [(j, v) for (j, v) in enumerate(row) if abs(v) > 1e-14]
        if len(coeff) == 1:
            j, v = coeff[0]
            x[j] = vec[i] * v
            if v != 1:
                print('Want to debug this to check if behaviour is correct')

    #r2 = [(val, [i for i, v in enumerate(coeff) if v != 0]) for coeff, val in solution]
    #return r2, rank
    return x, rank


def simplify_full_rank(solution):
    '''Simplify solution when matrix is of full rank'''
    return [sol[1] for sol in solution]


def matrix_printer(array, length, field, latex=False):
    '''Prints matrix so that it is easier to read for humans'''
    if len(array.shape) == 1:
        array = array.reshape(1, -1)
    if latex:
        sep = '&'
    else:
        sep = ' '

    for row in array:
        print('|', end='')
        for element in row:
            if isinstance(element, numpy.ndarray):
                pass
            print('{:{}}'.format(field.polystring(element), length), end=sep)
        print('|')


def matrix_string(array, length, field, latex=False):
    '''Prints matrix so that it is easier to read for humans'''
    r = []
    if len(array.shape) == 1:
        array = array.reshape(1, -1)
    if latex:
        sep = '&'
    else:
        sep = ' '

    for row in array:
        r.append('|')
        for element in row:
            if isinstance(element, numpy.ndarray):
                pass
            r.append('{:{}}{}'.format(field.polystring(element), length, sep))
        r.append('|\n')
    return ''.join(r)


if __name__ == '__main__':
    import numpy
    from helper import RealField

    X = numpy.array((-2., 0., 3.))
    MAT = numpy.array([[1., 2., 3.], [1., 2., 3.], [2., 4., 4.]])
    VEC = numpy.array([4., 4., 6.])
    SOL, RANK = solve(MAT, VEC, RealField)
#    assert all(sol == x)
#    assert rank == 2
