import qiskit
from qiskit_aer import AerSimulator
import numpy as np

def q4(qc):
    iden4 = np.eye(4)
    iden2 = np.eye(2)
    had2 = np.array([[1,1],[1, -1]])
    had2 = 1 / np.sqrt(2) * had2
    had8 = np.kron(had2, iden4)

    py2 = np.array([[0, -1j],[1j, 0]])
    # Y⊗I
    py4 = np.kron(py2, iden2)
    py8 = np.kron(iden4, py2)

    cx4 = np.array([[1,0,0,0]
                   ,[0,1,0,0]
                   ,[0,0,0,1]
                   ,[0,0,1,0]])
    cx8 = np.kron(cx4, iden2)
    # print(py8, "\n=======\n", had8, "\n======\n", cx8)

    ccx = np.array([ [1,0,0,0,0,0,0,0]
                    ,[0,1,0,0,0,0,0,0]
                    ,[0,0,1,0,0,0,0,0]
                    ,[0,0,0,1,0,0,0,0]
                    ,[0,0,0,0,1,0,0,0]
                    ,[0,0,0,0,0,1,0,0]
                    ,[0,0,0,0,0,0,0,1]
                    ,[0,0,0,0,0,0,1,0]])

   
    backwards = False
    if(backwards):
        qc.ccx(0,1,2)   
        qc.cx(0,1)
        qc.y(1)
        qc.h(0)            
    else:
        qc.h(2)
        qc.y(1)
        qc.cx(2, 1)
        qc.ccx(2, 1, 0)
    print(qc.draw())
    U = qiskit.quantum_info.Operator(qc).to_matrix()
    # print(U)
    return U

def q1(qc):
    """
    
    - Reads right to left. (~Matrix operations)
    - If in a tensor, target wires are specific gates
        IE if on a single qubit, identity in that wire's position
        I⊗Y -> <qb.1>⊗<qb.0> -> apply Y to only qubit 0
        H⊗H -> Hadamard on both qubits
    - CNOT(control, target) -> circuit.cx (controlled X)

    returns:
    qiskit quantum circuit on 2 qubits that realizes U
    """
    # U = CNOT_{0,1} ∘ Y⊗I ∘ I⊗H
    
    had = np.array([[1,1],[1, -1]])
    had = 1 / np.sqrt(2) * had
    iden = np.eye(2)
    # I⊗H
    had4 = np.kron(iden, had)
    py = np.array([[0, -1j],[1j, 0]])
    # Y⊗I
    py4 = np.kron(py, iden)
    cx = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    
    print(had4 @ py4 @ cx)
    print("=============")
    print(cx @ py4 @ had4)
    # print("=============")
    #print(qiskit.quantum_info.Operator(qc0).to_matrix())
    if(False):
        qc.cx(1, 0)
        qc.y(0)
        qc.h(1)
    else:
        qc.h(1)
        qc.y(0)
        qc.cx(1, 0)
    
    # qc.h(0)
    # qc.y(1)
    # qc.cx(0, 1)
    
    # print(measure(qc, 10))
    
    print(qc.draw())
    factor = 1j/ np.sqrt(2)
    mtx = qiskit.quantum_info.Operator(qc).to_matrix()
    # print(mtx)
    # print(factor, "*\n", mtx)

    # print(mtx)
    return mtx


def measure(qc, N):
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
    # print(qcm.draw())
    return results

def probMap(U, numQbits):
    # U = q1(qc)
    # print(U)
    # col index 0, input |0>
    col = U[:, 0]
    # print("\n",col)
    #print(col)
    #  |amplitude|² foreach in column
    probU = [float(round(np.abs(amplitude)**2,2)) for amplitude in col]
    n = numQbits
    probMap = {}
    for i, prob in enumerate(probU):        
        #print("|",format(i, f'0{n}b'),">", ":",prob)
        currQbit = format(i, f'0{n}b')
        probMap[currQbit] = float(prob)
        # print(probMap[currQbit])
    #print(probMap)
    return probMap

def isUnitary(A):
    '''
    A matrix is unitary if multiplying by its adjoint equals 
    the identity 
'''
    def adjoint(M):   
        '''
        Adjoint is the complex conjugate of its transpose
    ''' 
        result = np.conj(M.T)   
        # floating point tolerance            
        result[np.abs(result) < 1e-20] = 0
        return result
    with open("output_q1.txt", "a") as f:
        print("A matrix is Unitary if its transpose:\n", A.T, file=f)
        iden = np.eye(A.shape[0])
        print("Multiplied by itself:\n", A, "\n"
          , "is equal to the identity:\n", iden, file=f)
        product = adjoint(A) @ A
        product[np.abs(product) < 1e-10] = 0
        print(" A† @ A:\n", product, file=f)
    return np.allclose(product, iden, atol = 1e-10)

def main():
    if(True):
        qc = qiskit.QuantumCircuit(2)
        U = q1(qc)
        with open("output_q1.txt", "a") as f:
            print("Question 1(a):\n", U, file=f)
            print("Question 1(b):\n")
        
        isUnitary(U)

        #U = q1(qc)
        probs = probMap(U, qc.num_qubits)
        print("Probability for each state:", probs)
        prob0 = probs['00']
        print("Question 2:\n", prob0)
        prob1 = probs['10']
        print("Question 3:\n", prob1)
    else:
        qc = qiskit.QuantumCircuit(3)
        U = q4(qc)
        with open("output_q4.txt", "a") as f:
            probs = probMap(U, qc.num_qubits)
            print("Probabilities for input |000>:", probs, file=f)
        isUnitary(U)
        
        
        
    return

if __name__ == "__main__":
    main()