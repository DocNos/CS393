from qiskit import QuantumCircuit
import numpy as np

def dj_standard(numQubits):
    qc_dj = QuantumCircuit(numQubits +1)
    if np.random.randint(0, 2):
        # Flip output qubits with 50% chance
        qc_dj.x(numQubits)
    if np.random.randint(0, 2):
        # return constant circuit with 50% chance.
        return qc_dj
 
    # If the "if" statement above was "TRUE" then we've 
    # returned the constant
    # function and the function is complete. 
    # If not, we proceed in creating our
    # balanced function. Everything below is to produce the balanced function:
 
    # select half of all possible states at random:
    on_states = np.random.choice(
        range(2**numQubits),  # numbers to sample from
        2**numQubits // 2,  # number of samples
        replace=False,  # makes sure states are only sampled once
    )
 
    def add_cx(qc_dj, bit_string):
        for qubit, bit in enumerate(reversed(bit_string)):
            if bit == "1":
                qc_dj.x(qubit)
        return qc_dj
 
    for state in on_states:
     #   qc_dj.barrier()  # Barriers are added to help visualize how the functions are created. They can safely be removed.
        qc_dj = add_cx(qc_dj, f"{state:0b}")
        qc_dj.mcx(list(range(numQubits)), numQubits)
        qc_dj = add_cx(qc_dj, f"{state:0b}")
 
    #qc_dj.barrier()
    #qc_dj.draw()
    return qc_dj

''' 
Oracle function: random circuit guaranteed to be either 
constant or balanced

input string should be length 2^numQbits
    this is because the string needs to represent all possible
    states for each qbit, each which needs 2 bits of 
    either 0 or 1:
    2 qubits → 2² = 4 possible inputs: |00⟩, |01⟩, |10⟩, |11⟩

    this string represents the "truth table" of the oracle.
'''
def binaryOracle(binaryString, numQbits):
    # input hardcoded, unecessary checks added to practice py syntax.
    if not all(bit in '01' for bit in binaryString): 
        print("binary string must contain only binary digits")
        return    
    if len(binaryString) != 2**numQbits:
        print("binary string incorrect size for qbit input")
        return
    # Extra qbit added for storing output
    qc = QuantumCircuit(numQbits + 1)
    
    def onCX(qc_in, binaryString_in):
        '''
    "OR Mask", sets the inputs (which default all start at 0)
    to match the binary input truth table
    Creates the control pattern of input binary string
    flips each qbit according to the input string.
        Enumerate     -> convert string input index to binary
        Reversed      -> place in qskit computational basis (right to left)
        Pauli X (NOT) -> flip qbit to match input string state
    '''
        for i, bit in enumerate(reversed(binaryString_in)):
            if bit == '0':  # Flip zeros so all controls become |1⟩
                qc.x(i)
        return qc_in

    def onMultiControl(qc_in, qbits_in, truthTable, barrier):
        '''
    Entangle input bits with output bit using mcx gate
        - Iterating through each position in 
        the input string (truth table)
        - Only apply gates where function outputs 1. 
        - Binary string represents desired output of the oracle. 
        - Index parameter of onCX should be in a binary string 
        with proper padding
    
    Multi-Control X gate -> Flips target only if all controls
                                are 1. This is why we apply X to inputs.
    List                 -> creates an iterable list
    Range                -> iterates from 0 to n-1

    In summation: 
    - binaryString (truth table) has 1, set qbits
        so that total circuit outputs 1. when passing to onCX,
        mask the 0 outputs so they will flip target. 
    - Two calls to cx because the circuit is only determining 
        whether the multi-control should be set for the desired
        output.

    '''   
        # print("truth table: ", truthTable)     
        for index, output_bit in enumerate(truthTable):
            if barrier: qc_in.barrier()
            if output_bit == '1':                  
                stateBinary = f"{index:0{qbits_in}b}"        
                onCX(qc_in, stateBinary)
                qc_in.mcx(list(range(qbits_in)), qbits_in)
                onCX(qc_in, stateBinary)
        return qc_in

    onMultiControl(qc, numQbits, binaryString, True)
    qc.draw()
    qc.draw(output='mpl', filename=f'n{numQbits}_compressed.png')
    qc.decompose().draw(output='mpl', filename=f'n{numQbits}_uncompressed.png')


def main():
    binaryOracle("11001100", 3)
    #print(dj_standard(4))
    binaryOracle("1100110011001100", 4)

if __name__ == "__main__":
    main()
