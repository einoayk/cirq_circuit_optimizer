import unittest
import cirq
from cirq.circuits import InsertStrategy
from src.random_circuit_generator import random_circuit
from src.transformers import cnot_to_hadamards_and_cnot

class TestCnotToHadamardsAndCnot(unittest.TestCase):

    def test_one_instance(self):
        qubits = cirq.LineQubit.range(2)
        circuit = cirq.Circuit()
        circuit.append(cirq.CNOT(qubits[0], qubits[1]))           
        circuit = cnot_to_hadamards_and_cnot(circuit)
        expected_circuit = cirq.Circuit()
        expected_circuit.append([cirq.H(qubits[0]), cirq.H(qubits[1])])
        expected_circuit.append(cirq.CNOT(qubits[1], qubits[0]))
        expected_circuit.append([cirq.H(qubits[0]), cirq.H(qubits[1])])
        self.assertEqual(circuit, expected_circuit)

    def test_multiple_instances(self):
        qubits = cirq.LineQubit.range(5)
        circuit = cirq.Circuit()
        circuit.append([cirq.CNOT(qubits[i], qubits[i+1]) for i in range(4)])
        circuit = cnot_to_hadamards_and_cnot(circuit)
        expected_circuit = cirq.Circuit()
        for i in range(4):
            expected_circuit.append([cirq.H(qubits[i]), cirq.H(qubits[i+1])], strategy=InsertStrategy.INLINE)
            expected_circuit.append(cirq.CNOT(qubits[i+1], qubits[i]), strategy=InsertStrategy.INLINE)
            expected_circuit.append([cirq.H(qubits[i]), cirq.H(qubits[i+1])], strategy=InsertStrategy.INLINE)
            
        self.assertEqual(circuit, expected_circuit)

    def test_does_not_change_effect_of_circuit(self):
        n_qubits = 5
        n_templates = 30
        circuit = random_circuit(n_qubits, n_templates)
        expected_circuit = circuit.unfreeze(copy=True)
        circuit = cnot_to_hadamards_and_cnot(circuit)
        cirq.testing.assert_circuits_with_terminal_measurements_are_equivalent(actual=circuit, 
                                                                               reference=expected_circuit)

if __name__ == '__main__':
    unittest.main()