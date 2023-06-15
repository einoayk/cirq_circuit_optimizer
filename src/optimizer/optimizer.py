import random
import sys
sys.path.append('../..')
from src.transformers.transformers import (
    remove_double_hadamards,
    combine_cnots, 
    remove_double_cnots,
    hadamards_and_cnot_to_cnot, 
    cnot_to_hadamards_and_cnot, 
    combine_cnots_with_controls_surrounded_by_hadamards
)

_FUNCTION_LIST = [
    remove_double_hadamards, 
    combine_cnots, 
    remove_double_cnots,
    hadamards_and_cnot_to_cnot, 
    cnot_to_hadamards_and_cnot, 
    combine_cnots_with_controls_surrounded_by_hadamards
]

def optimize(circuit, initial_probs, transition_probs, n_iter=50, n_opt_circuits=20):
    """Cirq circuit optimizer. Makes multiple copies of the original circuit, randomly 
    applies the circuit identities specified in the problem description on the circuits
    and outputs the shortest one.

    Args:
        cirucit (cirq.Circuit): circuit that is optimized
        initial_probs (lis(float)): probability distribution for choosing the first transformer
        transition_probs (lis(lis(float))): probability distribution for choosing next transformer
                                            depending on which transformer was previously applied.
        n_iter (int): how many transformers are applied to a single circuit
        n_opt_circuits (int): how many copies of the original circuit are optimized.

    Returns:
        best_opt_circuit (cirq.Circuit): the shortest optimized circuit
    """
    opt_circuits = [None] * n_opt_circuits
    for circ_ind in range(n_opt_circuits):
        opt_circuit = circuit.unfreeze(copy=True)
        function_ind = random.choices([i for i in range(len(_FUNCTION_LIST))],  weights=initial_probs)[0]
        opt_circuit = _FUNCTION_LIST[function_ind](opt_circuit)
        for i in range(n_iter):
            function_inds_list = [j for j in range(len(_FUNCTION_LIST))]              
            function_ind = random.choices(function_inds_list,  weights=transition_probs[function_ind])[0]
            opt_circuit = _FUNCTION_LIST[function_ind](opt_circuit)

        opt_circuits[circ_ind] = opt_circuit

    opt_circuit_lens =[len(circuit) for circuit in opt_circuits]
    best_opt_circuit_ind = opt_circuit_lens.index(min(opt_circuit_lens))
    best_opt_circuit = opt_circuits[best_opt_circuit_ind]        
    return best_opt_circuit

    
            
