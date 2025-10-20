import qiskit
import qiskit_aer
import math
import cmath
import numpy as np

'''
<run> = qiskit_aer.AerSimulator().run(<circuit>,shots=<N>)
 where <N> is the number of times the circuit should be run. 
 The experimental data can be
 extracted from the run via
 <data> = <run>.result().data()[’counts’]

 The probability that the 3–bit classical register has a 
 value of (c2c1c0)2 is given by the square
 of the complex modulus of the coefficient of 
 |c2c1c0⟩ in |ψ⟩.
 So if we measure all three qubits in the circuit as 
 in the 
'''


def probabilities0(qc):
    """
    -- probabilities of classical register values, assuming no ancillae
    where:
        qc = Qiskit quantum circuit with no classical bits (unmeasured)
    assumes:
        qc.num_clbits == 0
    returns:
        list of register probabilities, indexed by register 
        value
    """
    U = qiskit.quantum_info.Operator(qc).to_matrix()    
    # extract first column directly
    col = U[:,0]
    #print(col)
    #  |amplitude|² foreach in column
    probU = [np.abs(amplitude)**2 for amplitude in col]
    #print(probU)
    return probU

def measurements0(qc, N):
    """
    -- get experimental results of running a quantum circuit with no ancillae
    where:
        qc = Qiskit quantum circuit with no classical bits (unmeasured)
        N = number of shots
    assumes:
        qc.num_clbits == 0
    returns:
        list of measured register value frequencies, indexed by register value
    """

def probabilities(qc, qbits, cbits):
    """
-- probabilities of classical register values, with ancillae
where:
    qc = Qiskit quantum circuit with no classical bits 
    (unmeasured)
    qbits = list of qubit wire numbers to measure
    cbits = list of classical bits the qubits are mapped to
assumes:
    qc.num_clbits == 0
    len(qbits) == len(cbits) == m
    cbits is a permutation of range(0,m)
returns:
    list of measured register value frequencies, 
    indexed by register value
"""

def measurements(qc, qbits, cbits, N):
    """
-- get experimental results of running a quantum circuit with ancillae
where:
    qc = Qiskit quantum circuit with no classical bits (unmeasured)
    qbits = list of qubit wire numbers to measure
    cbits = list of classical bits qubits are mapped to
    N = number of shots
assumes:
    qc.num_clbits == 0
    len(qbits) == len(cbits) == m
    cbits is a permutation of range(0,m)
returns:
    list of measured register value frequencies, indexed by register value
"""

def main():
    qc1 = qiskit.QuantumCircuit(3)
    qc1.h([0,2])
    qc1.mcx([0,2],1)
    probabilities0(qc1)
    qbits1 = [1,2]
    cbits1 = [0,1]

if __name__ == "__main__":
    main()