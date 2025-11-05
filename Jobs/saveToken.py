# Load the Qiskit Runtime service
from qiskit_ibm_runtime import QiskitRuntimeService
 
# Load the Runtime primitive and session
from qiskit_ibm_runtime import SamplerV2 as Sampler
 
# Syntax for first saving your token.  Delete these lines after 
# saving your credentials.
def newToken(_token):
    QiskitRuntimeService.save_account(
        channel='ibm_quantum_platform'
        , instance = '<YOUR_IBM_INSTANCE_CRN>'
        , token=_token
        , overwrite=True
        , set_as_default=True)
    service = QiskitRuntimeService(channel='ibm_quantum_platform')
    return service

def loadCredentials():
# Load saved credentials
    service = QiskitRuntimeService() 
# Use the least busy backend, or uncomment 
# the loading of a specific backend like "ibm_brisbane".
    backend = service.least_busy(
        operational=True
        , simulator=False
        , min_num_qubits = 127)
    # backend = service.backend("ibm_brisbane")
    print(backend.name) 
    sampler = Sampler(mode=backend)
    return sampler

def main():


    return 0


if __name__ == "main":
    main()