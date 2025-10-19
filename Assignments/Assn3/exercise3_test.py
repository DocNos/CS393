# exercise3_test.py
# -- simple test of function in exercise set #3

import numpy
import qiskit
import qiskit_aer

import exercise3_sol as ex3


###############################################################################
# some circuits/mappings
qc1 = qiskit.QuantumCircuit(3)
qc1.h([0,2])
qc1.mcx([0,2],1)

qbits1 = [1,2]
cbits1 = [0,1]


qc2 = qiskit.QuantumCircuit(2)
qc2.h([0,1])
qc2.y(0)
qc2.cx(1,0)
qc2.h(1)

qbits2 = [0,1]
cbits2 = [1,0]


###############################################################################
# (1) classical register probablities, no ancilla, no mapping of qubits/bits
probs1 = ex3.probabilities0(qc1)
print(probs1)
probs2 = ex3.probabilities0(qc2)
print(probs2)
print()


###############################################################################
# (2) measured register value frequencies, no ancilla, no mapping
meas1 = ex3.measurements0(qc1,1000)
print(meas1)
meas2 = ex3.measurements0(qc2,1000)
print(meas2)
print()


###############################################################################
# (3) classical register probabilities, ancillae, mapping of qubits/bits
probs1 = ex3.probabilities(qc1,qbits1,cbits1)
print(probs1)
probs2 = ex3.probabilities(qc2,qbits2,cbits2)
print(probs2)
print()



###############################################################################
# (4) measured register value frequencies, ancillae, mapping of qubits/bits
meas1 = ex3.measurements(qc1,qbits1,cbits1,1000)
print(meas1)
meas2 = ex3.measurements(qc2,qbits2,cbits2,1000)
print(meas2)


