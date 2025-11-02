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
    print(U) 
    # extract first column directly
    col = U[:,0]
    #print(col)
    #  |amplitude|² foreach in column
    # round to precision 2 decimal places
    probU = [float(round(np.abs(amplitude)**2,2)) for amplitude in col]
    #probU = [np.abs(amplitude)**2 for amplitude in col]
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

# q[1,2] -> c[0, 1]
#         q1  q2  c0  c1  | out
# 0 000    0   0   0   0  | 00 |000> -> 00 (0, 0)
# 1 001    0   0   0   0  | 00 |001> -> 00 (1, 0)
# 2 010    1   0   1   0  | 01 |010> -> 01 (2, 1)
# 3 011    1   0   1   0  | 01 |011> -> 01 (3, 1)
# 4 100    0   1   0   1  | 10 |100> -> 10 (4, 2)
# 5 101    0   1   0   1  | 10 |101> -> 10 (5, 2)
# 6 110    1   1   1   1  | 11 |110> -> 11 (6, 3)
# 7 111    1   1   1   1  | 11 |111> -> 11 (7, 3)


# iterate through each binary string, build cbit out
def strAnd(stateBin, map):
    cbit = [0, 0]
    # print(stateBin)
    for i, bit in enumerate(stateBin[::-1]):
        if i in map:
            # print("qbit", i, "(", bit, ")" "mapping to cbit", map[i])
            cbit[map[i]] = bit
    cbit.reverse()
    # print(cbit)
    cbitStr = ''.join(cbit)
    return cbitStr

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
    # qc1 = qiskit.QuantumCircuit(qbits, cbits)
    U = qiskit.quantum_info.Operator(qc).to_matrix()
    # only measure the qbits specified from qbits
    n = qc.num_qubits
    m = len(qbits)
    rows = U[:,0]
    # Collect all mapped bits
    dictMap = dict()
    for i, bit in enumerate(qbits):
        dictMap[bit] = cbits[i]

    stateBins = []
    cbitBin = []
    mapping = {}
    probMap = {}
    for i in range(2**n):
        # convert state indices to binary
        stateBin_str = format(i, f'0{n}b')
        stateBins.append(stateBin_str)
        prob = float(round(np.abs(rows[i]**2),2 )) 
        probMap[stateBin_str] = prob 
        cbit = strAnd(stateBin_str, dictMap)
        cbitBin.append(cbit)
        mapping[stateBin_str] = cbit
    # print(mapping, '\n', probMap)
    probSum = {}
    # sum all probs of cbits that map to same qbits
    for i, qbit in enumerate(mapping):
        if mapping[qbit] not in probSum:
            probSum[mapping[qbit]] = probMap[qbit]
        elif mapping[qbit] == probSum[mapping[qbit]]:
            probSum[mapping[qbit]] += probMap[qbit]
    
    print(mapping, '\n', probMap, '\n', probSum)
    
    
    
    # Get amplitude of each probability, extracted from first column.
    # amplitude = |value|²
    probs = [float(
            round(np.abs(amplitude)**2, 2 )
        ) for amplitude in rows]

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

    qbits1 = [1,2]
    cbits1 = [0,1]
    probabilities(qc1, qbits1, cbits1)

    qc2 = qiskit.QuantumCircuit(2)
    qc2.h([0,1])
    qc2.y(0)
    qc2.cx(1,0)
    qc2.h(1)

    qbits2 = [0,1]
    cbits2 = [1,0]
    probabilities(qc2, qbits2, cbits2)

if __name__ == "__main__":
    main()