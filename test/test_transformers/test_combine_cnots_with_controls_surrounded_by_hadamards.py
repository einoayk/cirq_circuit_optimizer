import unittest
import cirq
from cirq.circuits import InsertStrategy
import random
from src.transformers.transformers import combine_cnots_with_controls_surrounded_by_hadamards


class TestCombineCnotsWithControlsSurroundedByHadamards(unittest.TestCase):

    def test_one_instance(self):
        qubits = cirq.LineQubit.range(5)
        circuit = cirq.Circuit()
        circuit.append([cirq.H(qubits[i]) for i in range(4)])
        circuit.append([cirq.CNOT(qubits[i], qubits[4]) for i in range(4)])
        circuit.append([cirq.H(qubits[i]) for i in range(4)])     
        circuit = combine_cnots_with_controls_surrounded_by_hadamards(circuit)
        expected_circuit = cirq.Circuit()
        expected_circuit.append(cirq.H(qubits[4]))
        op = 1
        for i in range(4):
            op = op * cirq.X(qubits[i])

        op = op.controlled_by(qubits[4])
        expected_circuit.append(op)
        expected_circuit.append(cirq.H(qubits[4]))
        if circuit != expected_circuit:
            self.fail("combine_cnots_with_controls_surrounded_by_hadamards doesn't behave as expected")

    def test_multiple_instances(self):
        n_qubits = 7
        n_instances = 4 # should be smaller than n_qubits
        assert n_qubits >= n_instances
        qubits = cirq.LineQubit.range(n_qubits)
        circuit = cirq.Circuit()
        expected_circuit = cirq.Circuit()        
        target_qubit_inds = random.sample([i for i in range(n_qubits)], n_instances)
        for target_qubit_ind in target_qubit_inds:
            n_control_qubits = random.randint(2, n_qubits-1)
            sampled_qubit_inds = [j for j in range(n_qubits) if j != target_qubit_ind]
            control_qubit_inds = random.sample(sampled_qubit_inds, k=n_control_qubits)
            circuit.append([cirq.H(qubits[j]) for j in control_qubit_inds], strategy=InsertStrategy.NEW_THEN_INLINE)
            circuit.append([cirq.CNOT(qubits[j], qubits[target_qubit_ind]) for j in control_qubit_inds], strategy=InsertStrategy.NEW_THEN_INLINE)
            circuit.append([cirq.H(qubits[j]) for j in control_qubit_inds], strategy=InsertStrategy.NEW_THEN_INLINE)
            op = 1
            for j in control_qubit_inds:
                op = op * cirq.X(qubits[j])

            op = op.controlled_by(qubits[target_qubit_ind])
            expected_circuit.append(cirq.H(qubits[target_qubit_ind]), strategy=InsertStrategy.NEW_THEN_INLINE)
            expected_circuit.append(op, strategy=InsertStrategy.NEW_THEN_INLINE)
            expected_circuit.append(cirq.H(qubits[target_qubit_ind]), strategy=InsertStrategy.NEW_THEN_INLINE)
            
        circuit = combine_cnots_with_controls_surrounded_by_hadamards(circuit)
        if circuit != expected_circuit:
            self.fail("combine_cnots_with_controls_surrounded_by_hadamards doesn't behave as expected")

if __name__ == '__main__':
    unittest.main()