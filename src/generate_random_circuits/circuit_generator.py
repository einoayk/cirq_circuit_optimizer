import cirq
import random 

def add_two_hadamards(circuit, qubits):
    mutated_circuit = circuit.unfreeze(copy=True)
    random_qubit = random.choice(qubits)
    mutated_circuit.append([cirq.H(random_qubit), cirq.H(random_qubit)])
    return mutated_circuit

def add_cnot(circuit, qubits):
    mutated_circuit = circuit.unfreeze(copy=True)
    control_qubit, target_qubit = random.sample(qubits, 2)
    mutated_circuit.append([cirq.CNOT(control_qubit, target_qubit)])
    return mutated_circuit

def add_two_cnots(circuit, qubits):
    mutated_circuit = circuit.unfreeze(copy=True)
    control_qubit, target_qubit = random.sample(qubits, 2)
    mutated_circuit.append([cirq.CNOT(control_qubit, target_qubit),
                            cirq.CNOT(control_qubit, target_qubit)])
    return mutated_circuit

def add_cnots_with_different_targets(circuit, qubits):
    mutated_circuit = circuit.unfreeze(copy=True)
    n_cnots = random.randint(2, len(qubits)-1)
    qubit_sample = random.sample(qubits, n_cnots+1)
    control_qubit = qubit_sample[0]
    target_qubits = qubit_sample[1:]
    cnot_list = [cirq.CNOT(control_qubit, target_qubit) for target_qubit in target_qubits]
    mutated_circuit.append(cnot_list)
    return mutated_circuit

def add_hadamards_and_cnot(circuit, qubits):
    mutated_circuit = circuit.unfreeze(copy=True)
    control_qubit, target_qubit = random.sample(qubits, 2)
    mutated_circuit.append([cirq.H(control_qubit), cirq.H(target_qubit)])
    mutated_circuit.append([cirq.CNOT(control_qubit, target_qubit)])
    mutated_circuit.append([cirq.H(control_qubit), cirq.H(target_qubit)])
    return mutated_circuit

def add_hadamards_and_cnots_with_different_targets(circuit, qubits):
    mutated_circuit = circuit.unfreeze(copy=True)
    n_cnots = random.randint(2, len(qubits)-1)
    qubit_sample = random.sample(qubits, n_cnots+1)
    control_qubits = qubit_sample[1:]
    target_qubit = qubit_sample[0]
    hadamard_list = [cirq.H(qubit) for qubit in control_qubits]
    cnot_list = [cirq.CNOT(control_qubit, target_qubit) for control_qubit in control_qubits]
    mutated_circuit.append(hadamard_list)
    mutated_circuit.append(cnot_list)
    mutated_circuit.append(hadamard_list)
    return mutated_circuit

def random_circuit(n_qubits, n_templates):
    qubits = cirq.LineQubit.range(n_qubits+1)
    circuit = cirq.Circuit()
    for i in range(n_templates):

        circuit = random.choice(function_list)(circuit, qubits)  

    return circuit

function_list = [
    add_two_hadamards, 
    add_cnot, 
    add_two_cnots, 
    add_cnots_with_different_targets, 
    add_hadamards_and_cnot, 
    add_hadamards_and_cnots_with_different_targets
]




