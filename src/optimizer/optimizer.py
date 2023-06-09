import random
import sys
sys.path.append('../..')
from src.transformers.transformers import (
    remove_double_hadamards,
    combine_cnots, remove_double_cnots,
    hadamards_and_cnot_to_cnot, cnot_to_hadamards_and_cnot, 
    combine_cnots_with_controls_surrounded_by_hadamards
)

function_list = [
    remove_double_hadamards, 
    combine_cnots, 
    remove_double_cnots,
    hadamards_and_cnot_to_cnot, 
    cnot_to_hadamards_and_cnot, 
    combine_cnots_with_controls_surrounded_by_hadamards
]

def optimize(circuit, initial_probs, transition_probs, n_iter=50, n_opt_circuits=20):
    """
    Cirq circuit optimizer
    """
    opt_circuits = [None] * n_opt_circuits
    for circ_ind in range(n_opt_circuits):
        opt_circuit = circuit.unfreeze(copy=True)
        function_ind = random.choices([i for i in range(6)],  weights=initial_probs)[0]
        opt_circuit = function_list[function_ind](opt_circuit)
        for i in range(n_iter):
            function_inds_list = [j for j in range(6)]              
            function_ind = random.choices(function_inds_list,  weights=transition_probs[function_ind])[0]
            opt_circuit = function_list[function_ind](opt_circuit)

        opt_circuits[circ_ind] = opt_circuit

    opt_circuit_lens =[len(circuit) for circuit in opt_circuits]
    best_opt_circuit_ind = opt_circuit_lens.index(min(opt_circuit_lens))
    best_opt_circuit = opt_circuits[best_opt_circuit_ind]        
    return best_opt_circuit

    
            
