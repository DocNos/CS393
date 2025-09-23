# test_all.py
# -- Simple usage of the numpy, qiskit, and qiskit_aer packages
# mat399a 2025.08


import numpy
import qiskit
import qiskit_aer


###############################################################################
# numpy stuff
u = numpy.zeros(4,complex)
M = numpy.zeros((4,4),complex)

for i in range(0,4):
  u[i] = (i + 1j)/10
print("u =",u)

for c in range(0,4):
  for r in range(0,4):
    M[r][c] = (r + 1j*c)/10
print("M =",M)

v = M @ u
print("v =",v)

uv = numpy.dot(u,v)
print("u.v =",uv)

traceM = M.trace()
print("trace(M) =",traceM)

Mt = M.T
print("transpose(M) =",Mt)


###############################################################################
# qiskit stuff
qc = qiskit.QuantumCircuit(2,2)
qc.h(0)
qc.mcx([0],1)
qc.barrier()
qc.h([0,1])
qc.barrier()
qc.measure([0,1],[0,1])
print("quantum circuit:")
print(qc.draw())


###############################################################################
# qiskit_aer stuff
result = qiskit_aer.AerSimulator().run(qc,shots=100).result()
print("circuit output:")
print(result.data())


