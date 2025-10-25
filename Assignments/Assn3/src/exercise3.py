import qiskit
from qiskit_aer import AerSimulator
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
    probU = [float(round(np.abs(amplitude)**2,2)) for amplitude in col]
    n = qc.num_qubits
    probMap = {}
    for i, prob in enumerate(probU):        
        #print("|",format(i, f'0{n}b'),">", ":",prob)
        currQbit = format(i, f'0{n}b')
        probMap[currQbit] = float(prob)
    # print(probMap)
    return probU

def measurements0(qc, N):
    """
    -- get experimental results of running a quantum circuit 
        with no ancillae
    where:
        qc = Qiskit quantum circuit with no classical bits 
        (unmeasured)
        N = number of shots
    assumes:
        qc.num_clbits == 0
    returns:
        list of measured register value frequencies, 
        indexed by register value
    """
    # Measured version of input circuit -> construct a 
    #   quantum circuit with equal classical bits to qbits
    numQbits = qc.num_qubits
    qcm = qiskit.QuantumCircuit(numQbits, numQbits)
    # copy input circuit into measured circuit
    qcm.compose(qc, range(0, numQbits), inplace= True)
    # map qubits to classical bits
    range_ = range(0, numQbits)
    # print(list(range_))
    qcm.measure(list(range_)
                , list(range_))
    job = AerSimulator().run(qcm, shots=N)
    # print(qcm.draw())
    results = job.result().data()['counts']
    return results
    print(results)




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

#def main():
#    qc1 = qiskit.QuantumCircuit(3)
#    qc1.h([0,2])
#    qc1.mcx([0,2],1)
#    measurements0(qc1, 4)
#    qbits1 = [1,2]
#    cbits1 = [0,1]
#
#if __name__ == "__main__":
#    main()