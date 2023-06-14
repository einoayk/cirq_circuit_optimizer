import cirq

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