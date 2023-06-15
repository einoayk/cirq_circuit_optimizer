import unittest
import cirq
import random
from src.random_circuit_generator import random_circuit
from src.transformers import hadamards_and_cnot_to_cnot

class TestHadamardsAndCnotToCnot(unittest.TestCase):

    def test_one_instance(self):
        qubits = cirq.LineQubit.range(2)
        circuit = cirq.Circuit()
        circuit.append([cirq.H(qubits[0]), cirq.H(qubits[1])])
        circuit.append(cirq.CNOT(qubits[1], qubits[0]))
        circuit.append([cirq.H(qubits[0]), cirq.H(qubits[1])])                   
        circuit = hadamards_and_cnot_to_cnot(circuit)
        expected_circuit = cirq.Circuit()
        expected_circuit.append(cirq.CNOT(qubits[0], qubits[1]))
        self.assertEqual(circuit, expected_circuit)

    def test_multiple_instances(self):
        n_qubits = 7
        n_instances = 2
        qubits = cirq.LineQubit.range(n_qubits)
        circuit = cirq.Circuit()
        expected_circuit = cirq.Circuit()
        for i in range(n_instances):
            qubit1_ind, qubit2_ind = random.sample([j for j in range(n_qubits)], k=2)
            circuit.append([cirq.H(qubits[qubit1_ind]), cirq.H(qubits[qubit2_ind])])
            circuit.append(cirq.CNOT(qubits[qubit2_ind], qubits[qubit1_ind]))
            circuit.append([cirq.H(qubits[qubit1_ind]), cirq.H(qubits[qubit2_ind])])
            expected_circuit.append(cirq.CNOT(qubits[qubit1_ind], qubits[qubit2_ind]))
            
        circuit = hadamards_and_cnot_to_cnot(circuit)
        self.assertEqual(circuit, expected_circuit)

    def test_does_not_change_effect_of_circuit(self):
        n_qubits = 5
        n_templates = 30
        circuit = random_circuit(n_qubits, n_templates)
        expected_circuit = circuit.unfreeze(copy=True)
        circuit = hadamards_and_cnot_to_cnot(circuit)
        cirq.testing.assert_circuits_with_terminal_measurements_are_equivalent(actual=circuit, 
                                                                               reference=expected_circuit)

if __name__ == '__main__':
    unittest.main()