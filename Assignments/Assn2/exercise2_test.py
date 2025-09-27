# exercise2_test.py
# -- simple test of function in exercise set #2

import math
import numpy
import qiskit

import exercise2 as ex2


#################################################################
# (1) unmeasured quantum circuit
qc = ex2.Q1()
print(qc.draw())
print()


#################################################################
# (2) unitary matrix
A = 1j*math.cos(1)
B = -math.sin(1)
U = ex2.Q2()
v = U @ numpy.array([0,A,B,0])
expected = (1j/math.sqrt(2)) * numpy.array([A-B,A+B,0,0])
print(numpy.isclose(v,expected,1e-20))


#################################################################
# (3) probabilities
p = ex2.Q3(A,B,0,0)
expected = [0.5*abs(B)**2,0.5*abs(B)**2,0.5*abs(A)**2,0.5*abs(A)**2]
print(numpy.isclose(p,expected,1e-20))

