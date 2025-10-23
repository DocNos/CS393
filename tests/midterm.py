import qiskit
import numpy as np

def q1(qc):
    #qc = qiskit.QuantumCircuit(2)
    qc.h(0)
    qc.y(1)
    qc.cx(1, 0)
    # print(qc.draw())
    mtx = qiskit.quantum_info.Operator(qc).to_matrix()
    # print(mtx)
    return mtx

def makeU(qc):
    qc.h(0)
    qc.y(1)
    qc.cx(1, 0)
    return qc


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
    print("A matrix is Unitary if its transpose:\n", A.T)
    iden = np.eye(A.shape[0])
    print("Multiplied by itself:\n", A, "\n"
          , "is equal to the identity:\n", iden)
    product = adjoint(A) @ A
    product[np.abs(product) < 1e-10] = 0
    print(" A† @ A:\n", product)
    return np.allclose(product, iden, atol = 1e-10)

def main():
    qc = qiskit.QuantumCircuit(2)
    U = q1(qc)
    print("Question 1(a):\n", U)
    print("Question 1(b):\n")
    isUnitary(U)
    
    #U = q1(qc)
    probs = probMap(U, qc.num_qubits)
    prob0 = probs['00']
    print("Question 2:\n", prob0)
    prob1 = probs['10']
    print("Question 3:\n", prob1)
    
    return

if __name__ == "__main__":
    main()