# CS393 Quantum Algorithms - F25
# Assignment 2 - 9_26_25
# Matt Klassen, Instructor
# Nixx Varboncoeur 
import numpy
import qiskit
import math
import cmath


def Q1():
    """
    Create a 2-qubit quantum circuit that realizes the unitary transformation:
    U = H⊗I ∘ CNOT_{1,0} ∘ I⊗Y ∘ H⊗H
    - Reads right to left. (~Matrix operations)
    - If in a tensor, target wires are specific gates
        IE if on a single qubit, identity in that wire's position
        I⊗Y -> <qb.1>⊗<qb.0> -> apply Y to only qubit 0
        H⊗H -> Hadamard on both qubits
    - CNOT(control, target) -> circuit.cx (controlled X)

    returns:
    qiskit quantum circuit on 2 qubits that realizes U
    """
    U = qiskit.QuantumCircuit(2)
    # H⊗H: Puts both qubits in superposition
    # |00⟩ → (1/2)(|00⟩ + |01⟩ + |10⟩ + |11⟩)
    U.h([0, 1])
    U.barrier()
    # Rotates qubit 0 in complex plane (adds phase)
    # |0⟩ → i|1⟩, |1⟩ → -i|0⟩
    U.y(0)
    U.barrier()
    # Entangles the qubits
    # If qubit 1 is |1⟩, flips qubit 0
    U.cx(1,0)
    U.barrier()
    # Partially "unmixes" the superposition on qubit 1
    U.h(1)
# U is the mathematical representation of entire quantum circuit:
#  - It encodes how EVERY possible input state 
#       transforms to an output state
#  - "lookup table" for all possible quantum transformations
# U transforms ANY input state into a new quantum state with:
#  - Superposition: Output state is typically a mix of all 
#       basis states
#  - Entanglement: Qubits become correlated 
#       (measuring one affects the other)
#  - Phase relationships: Complex amplitudes create 
#       interference effects
    return U

import numpy as np
def Q2():
    """
     Compute the 4 × 4 unitary matrix 
     for U in the qiskit computational basis.
    - Hard-code individual matrices, not U.
    - Tensor Prodcut -> np.kron() (kronecker product)
        for qiskit convention: np.kron(a, b) -> a=q1, b=q0
    - @ for matrix multiplication (composition)
    returns:
    numpy matrix for U
    """
    # Individual gates
    had = np.array([[1, 1] , [1, -1]], dtype=complex) / np.sqrt(2)
    pY = np.array([[0, -1j], [1j, 0]], dtype=complex)
    pX = np.array([[0,1], [1, 0]], dtype=complex)
    I = np.array([[1, 0], [0,1]], dtype=complex)

    # Turn each into a 4x4 (H1 comp basis gates) ----
    # Hadamar on both qubits
    had4 = np.kron(had, had)
    # Y gate on qubit 0
    y0 = np.kron(I, pY)
    # Hadamar gate on qubit 1
    h1 = np.kron(had, I)

    # CNOT {control, target}
    # control qubit is read, changes target conditionally.
    # - control qubit does not change. 
    # - target qubit gets XOR'd with control qubit

    # CNOT {1, 0}    
    # If qubit 1 is |1>, flip qubit 0
    #  |10> -> |11>, |11> -> |10>    
    # Each row shows where each basis state goes:
    # |00> -> |00> (put 1 in row 0, col 0)
    # |01> -> |01> (put 1 in row 1, col 1)
    # |10> -> |11> (put 1 in row 3, col 2)
    # |11> -> |10> (put 1 in row 2, col 3)
    # Each qbit has 2 states -----------------------
    #   Each COLUMN represents an INPUT basis state
    #   Each ROW represents an OUTPUT basis state
    # Column 0 (|00⟩): output is |00⟩ (control qbit)
    #   decimal representation = 0
    # Column 1 (|01⟩): output is |01⟩ (control qbit)
    #   decimal representation = 1
    # Column 2 (|10>): output is |11> (target qbit)
    #   decimal representation = 2
    # Column 2 (|11>): output is |10> (target qbit)
    #   decimal representation = 3
    # Any deviation from Identity represents a change. (?)
    #   IE, if the column & row are represented the same,
    #       It is the control. 
    cnot_10 = np.array( [
    #  |00> |01> |10> |11>  <-INPUT
        [1,  0,   0,   0], # |00> 
        [0,  1,   0,   0], # |01>
        [0,  0,   0,   1], # |10>
        [0,  0,   1,   0]  # |11>
    ], dtype=complex)      # ↑ OUTPUT

    # Compose the Unitary
    # U = H⊗I ∘ CNOT_{1,0} ∘ I⊗Y ∘ H⊗H
    # Keep in mind that numpy and qiskit operations are reversed.
    U = h1 @ cnot_10 @ y0 @ had4
    return U

def Q3(A00,A01,A10,A11):
    """
    |ψ⟩ = A00 |00⟩ + A01 |01⟩ + A10 |10⟩ + A11 |11⟩
    Quantum state: |ψ⟩ = A₀₀|00⟩ + A₀₁|01⟩ + A₁₀|10⟩ + A₁₁|11⟩
    As vector: ψ = [A₀₀, A₀₁, A₁₀, A₁₁]ᵀ (Born Rule) {?}
    - each input index called "amplitude" - quantum state
    - quantum amplitudes can interfere / change
        probabilities are real positive numbers.
    - Therefore, take complex magnitude²
        complex magnitude -> abs

    where:
    A00,A01,A10,A11 : complex amplitudes of initial qubit 
    register state    
    returns:
    list [prob00,prob01,prob10,prob11] where probXY 
    is the probability
    that the final state is |XY> (X,Y=0,1)
    """
    valIn = np. array( [A00, A01, A10, A11], dtype=complex)
    U = Q2()
    # apply U to input, creating a new quantum state
    psi = U @ valIn
    # double star - square
    # absolute value - complex magnitude
    res00 = abs(psi[0])** 2
    res01 = abs(psi[1])** 2
    res10 = abs(psi[2])** 2
    res11 = abs(psi[3])** 2
    return [res00, res01, res10, res11]
    



