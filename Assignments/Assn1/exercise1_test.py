# exercise1_test.py
# -- simple test of matrix routines

import numpy
import math
import qiskit

import exercise1 as ex1


#################################################################
# generate some square matrices
M3 = numpy.array([[1+2j,3,4-5j],\
                  [6,7+8j,9],\
                  [10+11j,12+13j,14-15j]])

qc = qiskit.QuantumCircuit(2)
qc.h(1)
qc.cp(math.pi/3,1,0)
M4 = qiskit.quantum_info.Operator(qc).to_matrix()

qc = qiskit.QuantumCircuit(2)
qc.h([0,1])
qc.z(0)
N4 = qiskit.quantum_info.Operator(qc).to_matrix()

qc = qiskit.QuantumCircuit(3)
qc.h(1)
qc.mcx([0,1],2)
qc.p(0.2*math.pi,0)
M8 = qiskit.quantum_info.Operator(qc).to_matrix()


#################################################################
# test of Hermitian conjugate
m3 = M3 - ex1.dagger(M3)
print(m3 == numpy.array([[4j,-3,-6+6j],\
                         [3,16j,-3+13j],\
                         [6+6j,3+13j,-30j]]))
print()


#################################################################
# test of Hermitian inner product
x1 = ex1.inner(M4,N4)
print(x1)
x2 = ex1.inner(M8,M8)
print(x2)
print()


#################################################################
# test of unitary predicate
u1 = ex1.isUnitary(M3)
print(u1)
u2 = ex1.isUnitary(M8)
print(u2)

