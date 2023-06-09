import cirq
from itertools import groupby
import sys
sys.path.append('../')
from src.functions import (
    is_cnot_with_multiple_targets,
    create_cnot_with_multiple_targets
)

def _all_equal(iterable):
    """Checks if all values of an iterable are the same"""
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def _lists_share_elements(list1, list2):
    """Checks if two lists share any elements"""
    return bool([i for i in list1 if i in list2])

def _map_cnot_to_cnot_and_hadamards(op, _: int):
    """Inverts CNOT-gate and adds Hadamard- 
    gates on both qubits before and after 
    the CNOT (identity e of project description)
    """
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

@cirq.transformer
def combine_cnots_with_controls_surrounded_by_hadamards(circuit, context=None):
    """Applies circuit identity a) to all locations of the circuit that permit it

    Args:
        circuit (cirq.Circuit): original circuit
    
    Returns:
        mutated_circuit (cirq.Circuit): circuit gotten by applying the identity
    """
    mutated_circuit = circuit.unfreeze(copy=True)
    insertions = []
    removals = []    
    for first_cnot_ind in range(1, len(mutated_circuit)-1):        
        for operation in mutated_circuit[first_cnot_ind].operations:
            if operation.gate != cirq.CNOT or (first_cnot_ind, operation) in removals:
                continue

            control_qubit, target_qubit = operation.qubits
            first_h_ind = mutated_circuit.prev_moment_operating_on(qubits=[control_qubit],
                                                                   end_moment_index=first_cnot_ind)
            h_operation = cirq.H(control_qubit)            
            if (first_h_ind is None or 
                h_operation not in mutated_circuit[first_h_ind].operations or 
                (first_h_ind, h_operation) in removals):
                continue

            next_h_ind = mutated_circuit.next_moment_operating_on(qubits=[control_qubit],
                                                                  start_moment_index=first_cnot_ind+1)
            if (next_h_ind is None or 
                h_operation not in mutated_circuit[next_h_ind].operations or 
                (next_h_ind, h_operation) in removals):
                continue

            control_qubits = []
            potential_removals = []
            potential_removals.extend([(first_h_ind, h_operation), (next_h_ind, h_operation)])
            potential_removals.append((first_cnot_ind, operation))
            control_qubits.append(control_qubit)
            new_removable_cnot_found = False
            cnot_ind = first_cnot_ind
            for i in range(len(mutated_circuit) - first_h_ind):                
                if i > 0 and new_removable_cnot_found == False:
                    break

                new_removable_cnot_found = False
                cnot_ind = mutated_circuit.next_moment_operating_on(qubits=[target_qubit],
                                                                    start_moment_index=cnot_ind+1)
                if cnot_ind is None:
                    continue

                for operation2 in mutated_circuit[cnot_ind].operations:                    
                    if (operation2.gate != cirq.CNOT or 
                        operation2.qubits[0] in control_qubits or 
                        operation2.qubits[1] != target_qubit or 
                        (cnot_ind, operation2) in removals):
                        continue

                    control_qubit = operation2.qubits[0]
                    prev_h_ind = mutated_circuit.prev_moment_operating_on(qubits=[control_qubit], 
                                                                          end_moment_index=cnot_ind)
                    new_h_operation = cirq.H(control_qubit)
                    if (prev_h_ind is None or 
                        new_h_operation not in mutated_circuit[prev_h_ind].operations or 
                        (prev_h_ind, new_h_operation) in removals or
                        prev_h_ind > first_cnot_ind):
                        continue

                    next_h_ind = mutated_circuit.next_moment_operating_on(qubits=[control_qubit],
                                                                          start_moment_index=cnot_ind+1)
                    if (next_h_ind is None or 
                        new_h_operation not in mutated_circuit[next_h_ind].operations or 
                        (next_h_ind, new_h_operation) in removals):
                        continue

                    control_qubits.append(control_qubit)
                    potential_removals.extend([(prev_h_ind, new_h_operation), (next_h_ind, new_h_operation)])
                    potential_removals.append((cnot_ind, operation2))
                    new_removable_cnot_found = True
                    break
                
            if len(control_qubits) < 2:
                continue

            cnot_with_multiple_targets = create_cnot_with_multiple_targets(target_qubits=control_qubits,
                                                                      control_qubit=target_qubit)
            insertable_sub_circuit = cirq.Circuit()
            insertable_sub_circuit.append(cirq.H(target_qubit))
            insertable_sub_circuit.append(cnot_with_multiple_targets)
            insertable_sub_circuit.append(cirq.H(target_qubit))
            insertions.append((first_cnot_ind, insertable_sub_circuit))
            removals.extend(potential_removals)
            
    if len(insertions) != 0:
        insertions.reverse()
        mutated_circuit.batch_remove(removals)
        mutated_circuit.batch_insert(insertions)

    mutated_circuit = cirq.drop_empty_moments(mutated_circuit)
    return mutated_circuit

@cirq.transformer
def remove_double_hadamards(circuit, context=None):
    """Applies circuit identity b) to all locations of the circuit that permit it

    Args:
        circuit (cirq.Circuit): original circuit
    
    Returns:
        mutated_circuit (cirq.Circuit): circuit gotten by applying the identity
    """
    mutated_circuit = circuit.unfreeze(copy=True)
    removals = []    
    for moment_ind in range(len(mutated_circuit)-1):        
        for operation in mutated_circuit[moment_ind].operations:            
            if (operation.gate != cirq.H or 
               (moment_ind, operation) in removals):
                continue
                
            qubit = operation.qubits[0]
            moment_ind_2 = mutated_circuit.next_moment_operating_on(qubits=[qubit],
                                                                    start_moment_index=moment_ind+1)                
            if (moment_ind_2 is not None and 
                operation in mutated_circuit[moment_ind_2] and
                (moment_ind_2, operation) not in removals):
                removals.extend([(moment_ind, operation), (moment_ind_2, operation)])
                    
    mutated_circuit.batch_remove(removals)
    mutated_circuit = cirq.drop_empty_moments(mutated_circuit)                        
    return mutated_circuit

@cirq.transformer
def remove_double_cnots(circuit, context=None): 
    """Applies circuit identity c) to all locations of the circuit that permit it

    Args:
        circuit (cirq.Circuit): original circuit
    
    Returns:
        mutated_circuit (cirq.Circuit): circuit gotten by applying the identity
    """ 
    mutated_circuit = circuit.unfreeze(copy=True)
    removals = []    
    for moment_ind in range(len(mutated_circuit)-1):
        for operation in mutated_circuit[moment_ind].operations:
            if ((operation.gate != cirq.CNOT 
                and is_cnot_with_multiple_targets(operation) == False) or
                (moment_ind, operation) in removals):
                continue
                
            control_qubit = operation.qubits[0]
            moment_inds_2 = mutated_circuit.next_moments_operating_on(qubits=operation.qubits,
                                                                      start_moment_index=moment_ind+1)            
            if (_all_equal(moment_inds_2.values()) and 
                moment_inds_2[control_qubit] != len(mutated_circuit) and 
                operation in mutated_circuit[moment_inds_2[control_qubit]] and
                (moment_inds_2[control_qubit], operation) not in removals):
                removals.extend([(moment_ind, operation), (moment_inds_2[control_qubit], operation)])
                
    mutated_circuit.batch_remove(removals)                
    mutated_circuit = cirq.drop_empty_moments(mutated_circuit)                        
    return mutated_circuit

@cirq.transformer
def combine_cnots(circuit, context=None):
    """Applies circuit identity d) to all locations of the circuit that permit it

    Args:
        circuit (cirq.Circuit): original circuit
    
    Returns:
        mutated_circuit (cirq.Circuit): circuit gotten by applying the identity
    """
    mutated_circuit = circuit.unfreeze(copy=True)
    insertions = []
    removals = []    
    for moment_ind in range(len(mutated_circuit)-1):
        for operation in mutated_circuit[moment_ind].operations:
                        
            if ((operation.gate != cirq.CNOT and 
                is_cnot_with_multiple_targets(operation) == False) or
                (moment_ind, operation) in removals):
                continue

            potential_removals = []
            potential_target_qubits = []
            control_qubit = operation.qubits[0]
            current_target_qubits = operation.qubits[1:]
            potential_target_qubits.extend(current_target_qubits)            
            potential_removals.append((moment_ind, operation))
            new_removable_cnot_found = False
            cnot_ind = moment_ind   
            for i in range(len(mutated_circuit) - moment_ind):
                if i > 0 and new_removable_cnot_found == False:
                    break

                new_removable_cnot_found = False
                cnot_ind = mutated_circuit.next_moment_operating_on(qubits=[control_qubit],
                                                                    start_moment_index=cnot_ind+1)
                if cnot_ind is None:
                    continue

                for operation2 in mutated_circuit[cnot_ind].operations:
                    if ((operation2.gate != cirq.CNOT and 
                        is_cnot_with_multiple_targets(operation2) == False) or
                        (cnot_ind, operation2) in removals or
                        (cnot_ind, operation2) in potential_removals):
                        continue                    
                    
                    control_qubit_2 = operation2.qubits[0]
                    target_qubits_2 = operation2.qubits[1:]
                    if (control_qubit_2 != control_qubit or 
                        _lists_share_elements(target_qubits_2, potential_target_qubits)):
                        continue

                    prev_moment_ind = mutated_circuit.prev_moment_operating_on(qubits=target_qubits_2, 
                                                                               end_moment_index=cnot_ind)
                    if prev_moment_ind is not None and prev_moment_ind >= moment_ind:
                        continue

                    new_removable_cnot_found = True
                    potential_target_qubits.extend(target_qubits_2)
                    potential_removals.append((cnot_ind, operation2))
                    break

            if len(potential_removals) <= 1:
                break           

            removals.extend(potential_removals)
            cnot_with_multiple_targets = create_cnot_with_multiple_targets(target_qubits=potential_target_qubits,
                                                                                control_qubit=control_qubit)
            insertions.append((moment_ind, cnot_with_multiple_targets))

    if len(removals) != 0:
        insertions.reverse()
        mutated_circuit.batch_remove(removals)
        mutated_circuit.batch_insert(insertions)
        mutated_circuit = cirq.drop_empty_moments(mutated_circuit)                    
    return mutated_circuit

@cirq.transformer
def cnot_to_hadamards_and_cnot(circuit, context=None):
    """Applies circuit identity e) to all locations of the circuit that permit it

    Args:
        circuit (cirq.Circuit): original circuit
    
    Returns:
        mutated_circuit (cirq.Circuit): circuit gotten by applying the identity
    """
    return cirq.map_operations_and_unroll(circuit, _map_cnot_to_cnot_and_hadamards)

@cirq.transformer
def hadamards_and_cnot_to_cnot(circuit, context=None):
    """Applies circuit identity f) to all locations of the circuit that permit it

    Args:
        circuit (cirq.Circuit): original circuit
    
    Returns:
        mutated_circuit (cirq.Circuit): circuit gotten by applying the identity
    """
    mutated_circuit = circuit.unfreeze(copy=True)
    removals = [] 
    replacements = []   
    for moment_ind in range(len(mutated_circuit)-2):
        for operation in mutated_circuit[moment_ind].operations:
            if operation.gate != cirq.H or (moment_ind, operation) in removals:
                continue
                
            qubit1 = operation.qubits[0]
            moment_ind_2 = mutated_circuit.next_moment_operating_on(qubits=[qubit1], 
                                                                    start_moment_index=moment_ind+1)
            if moment_ind_2 is None:
                continue

            for operation2 in mutated_circuit[moment_ind_2].operations:
                if operation2.gate != cirq.CNOT: 
                    continue

                if operation2.qubits[0] != qubit1 and operation2.qubits[1] != qubit1:
                    continue

                control_qubit = operation2.qubits[0]
                target_qubit = operation2.qubits[1]
                if qubit1 == control_qubit:
                    qubit2 = target_qubit
                else:
                    qubit2 = control_qubit

                prev_moment_ind = mutated_circuit.prev_moment_operating_on(qubits=[qubit2], 
                                                                           end_moment_index=moment_ind_2)
                second_H = cirq.H(qubit2)                
                if (prev_moment_ind is None or 
                    second_H not in mutated_circuit[prev_moment_ind] or 
                    (prev_moment_ind, second_H) in removals):
                    continue
                
                moment_inds_3 = mutated_circuit.next_moments_operating_on(qubits=[qubit1, qubit2],
                                                                          start_moment_index=moment_ind_2+1)
                if (moment_inds_3[qubit1] == len(mutated_circuit) or 
                    moment_inds_3[qubit2] == len(mutated_circuit)):
                    continue
                
                if (operation in mutated_circuit[moment_inds_3[qubit1]] and 
                    second_H in mutated_circuit[moment_inds_3[qubit2]] and 
                    (moment_inds_3[qubit1], operation) not in removals and 
                    (moment_inds_3[qubit2], second_H) not in removals):
                    removals.extend([(moment_ind, operation), 
                                     (prev_moment_ind, second_H), 
                                     (moment_inds_3[qubit1], operation), 
                                     (moment_inds_3[qubit2], second_H)])                    
                    replacements.append((moment_ind_2, 
                                        cirq.CNOT(control_qubit, target_qubit), 
                                        cirq.CNOT(target_qubit, control_qubit)))
                    
    mutated_circuit.batch_remove(removals)
    mutated_circuit.batch_replace(replacements)                                   
    mutated_circuit = cirq.drop_empty_moments(mutated_circuit)                                        
    return mutated_circuit