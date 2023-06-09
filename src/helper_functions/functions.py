import cirq
from itertools import groupby

def map_cnot_to_cnot_and_hadamards(op, _: int):
    if op.gate == cirq.CNOT:
        control_qubit = op.qubits[0]
        target_qubit = op.qubits[1]
        yield cirq.H(control_qubit)
        yield cirq.H(target_qubit)
        yield cirq.CNOT(target_qubit, control_qubit)
        yield cirq.H(control_qubit)
        yield cirq.H(target_qubit)
    else:
        yield op

def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def lists_share_elements(list1, list2):
    return bool([i for i in list1 if i in list2])

def is_cnot_with_multiple_targets(operation):
    if type(operation.gate) != cirq.ControlledGate:
        return False
    
    for sub_gate in operation.sub_operation.gate:
        if sub_gate != cirq.X:
            return False
        
    return True

def flat_probs_to_matrix(flatprobs):
    probs_matrix = []
    for i in range(6):
        temp_list = []
        if i > 0:
            temp_list.extend(flatprobs[i*5:i*5+i])

        temp_list.extend([0])
        if i < 5:
            temp_list.extend(flatprobs[i*5+i+1:i*5+6])

        probs_matrix.append(temp_list)

    return probs_matrix

def create_cnot_with_multiple_targets(target_qubits, control_qubit):
    op = 1
    for target_qubit in target_qubits:
        op *= cirq.X(target_qubit)

    op = op.controlled_by(control_qubit)    
    return op