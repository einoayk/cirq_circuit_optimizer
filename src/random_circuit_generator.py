import cirq
import random

def add_two_hadamards(circuit, qubits):
    """Adds two Hadamard gates to a randomly chosen qubit of 
    the input circuit.

    Args:
        circuit (cirq.Circuit): circuit to which Hadamards are added
        qubits (list(cirq.LineQubit)): qubits of the circuit

    Returns:
        mutated_circuit (cirq.Circuit): circuit with added Hadamards
    """
    mutated_circuit = circuit.unfreeze(copy=True)
    random_qubit = random.choice(qubits)
    mutated_circuit.append([cirq.H(random_qubit), cirq.H(random_qubit)])
    return mutated_circuit

def add_cnot(circuit, qubits):
    """Adds a CNOT-gate to a randomly chosen pair of qubits of 
    the input circuit.

    Args:
        circuit (cirq.Circuit): circuit to which CNOT is added
        qubits (list(cirq.LineQubit)): qubits of the circuit

    Returns:
        mutated_circuit (cirq.Circuit): circuit with added CNOT
    """
    mutated_circuit = circuit.unfreeze(copy=True)
    control_qubit, target_qubit = random.sample(qubits, 2)
    mutated_circuit.append([cirq.CNOT(control_qubit, target_qubit)])
    return mutated_circuit

def add_two_cnots(circuit, qubits):
    """Adds a two CNOT-gates to a randomly chosen pair of qubits of 
    the input circuit.

    Args:
        circuit (cirq.Circuit): circuit to which 2 CNOTs are added
        qubits (list(cirq.LineQubit)): qubits of the circuit

    Returns:
        mutated_circuit (cirq.Circuit): circuit with added CNOTs
    """
    mutated_circuit = circuit.unfreeze(copy=True)
    control_qubit, target_qubit = random.sample(qubits, 2)
    mutated_circuit.append([cirq.CNOT(control_qubit, target_qubit),
                            cirq.CNOT(control_qubit, target_qubit)])
    return mutated_circuit

def add_cnots_with_different_targets(circuit, qubits):
    """Adds a randomly chosen amount of CNOT-gates with the same (random)
    control qubit and random but different target qubits.

    Args:
        circuit (cirq.Circuit): circuit to which CNOTs are added
        qubits (list(cirq.LineQubit)): qubits of the circuit

    Returns:
        mutated_circuit (cirq.Circuit): circuit with added CNOTs
    """
    mutated_circuit = circuit.unfreeze(copy=True)
    n_cnots = random.randint(2, len(qubits)-1)
    qubit_sample = random.sample(qubits, n_cnots+1)
    control_qubit = qubit_sample[0]
    target_qubits = qubit_sample[1:]
    cnot_list = [cirq.CNOT(control_qubit, target_qubit) for target_qubit in target_qubits]
    mutated_circuit.append(cnot_list)
    return mutated_circuit

def add_hadamards_and_cnot(circuit, qubits):
    """Ads Hadamard gates followed by a CNOT-gate and other pair
    of Hadamard gates to a randomly chosen pair of qubits.

    Args:
        circuit (cirq.Circuit): circuit to which gates are added
        qubits (list(cirq.LineQubit)): qubits of the circuit

    Returns:
        mutated_circuit (cirq.Circuit): circuit with added gates
    """
    mutated_circuit = circuit.unfreeze(copy=True)
    control_qubit, target_qubit = random.sample(qubits, 2)
    mutated_circuit.append([cirq.H(control_qubit), cirq.H(target_qubit)])
    mutated_circuit.append([cirq.CNOT(control_qubit, target_qubit)])
    mutated_circuit.append([cirq.H(control_qubit), cirq.H(target_qubit)])
    return mutated_circuit

def add_hadamards_and_cnots_with_different_targets(circuit, qubits):
    """Adds the left hand side of identity a) specified in the 
    problem description. The amount of CNOT-gates and the control-
    qubits are randomly chosen.

    Args:
        circuit (cirq.Circuit): circuit to which gates are added
        qubits (list(cirq.LineQubit)): qubits of the circuit

    Returns:
        mutated_circuit (cirq.Circuit): circuit with added gates
    """
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
    """Creates a Cirq circuit and adds multiple randomly chosen
    templates (left hand sides of the circuit identities) by 
    calling the functions definied above.

    Args:
        n_qubits (int): amount of qubits in the circuit
        n_templates (int): amount of templates added to the circuit

    Returns:
        circuit (cirq.Circuit): the circuit created by the function
    """
    function_list = [
        add_two_hadamards, 
        add_cnot, 
        add_two_cnots, 
        add_cnots_with_different_targets, 
        add_hadamards_and_cnot, 
        add_hadamards_and_cnots_with_different_targets
    ]
    qubits = cirq.LineQubit.range(n_qubits+1)
    circuit = cirq.Circuit()
    for i in range(n_templates):
        circuit = random.choice(function_list)(circuit, qubits)  

    return circuit