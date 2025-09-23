"""
CS393 Quantum Algorithms - Fall 2025
Matt Klassen, Instructor
Nixx Varboncoeur - 09_12_25 
"""
import numpy as np

def adjoint(M):
    """
for element in np.nditer(M, flags=['readwrite']):
        if np.iscomplex(element):
            element[...] = np.conj(element)
pass by reference? Need return M or no?
in for loop, is iterating over items or index?
is length var necessary?
where:
M : numpy square matrix
returns:
Hermitian conjugate of M
"""  
    result = np.conj(M.T)
    # Boolean index mask
    # np.abs(result) -> new array with abs of each element
    #                   absolute value of result
    # np.abs(result) < 1e-20 -> boolean array of the same
    #               shape (row, col) as result. each element   
    #               set to boolean of following comparison
    # result[] -> mask, selecting only the elements where true
    # (alt) result[~] -> select where false
    # result[] = 0 -> sets all elements where true to 0             
    result[np.abs(result) < 1e-20] = 0
    return result

def inner(A,B):
    """
where:
A,B : numpy square matrices
returns:
Hermitian inner product of A and B
"""
    result = np.trace(adjoint(A)@B)
    real = result.real if abs(result.real) >= 1e-20 else 0
    imag = result.imag if abs(result.imag) >= 1e-10 else 0
    return complex(real, imag)

    
def isUnitary(A):
    """
where:
A: numpy square matrix
returns:
True if A is unitary, False otherwise
"""
    """ 
    shape tuple of array dimensions (numpy) 
    shape[0] -> num rows
    shape[1] -> num cols
    input square matrix, only need first index
    """
    iden = np.eye(A.shape[0])
    """ 
    @ -> matrix multiplication
    matrix is unitary if A† @ A == I
    """
    product = adjoint(A) @ A
    """
    np.allclose() -> comparison with floating point 
    precision tolerance
    atol -> size of tolerance
    """
    return np.allclose(product, iden, atol = 1e-10)