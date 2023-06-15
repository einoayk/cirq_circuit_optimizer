import unittest
import cirq
from src.random_circuit_generator import add_two_cnots, random_circuit
from src.transformers import remove_double_cnots

class TestRemoveDoubleCnots(unittest.TestCase):

    def test_one_instance(self):
        qubits = cirq.LineQubit.range(2)
        circuit = cirq.Circuit()
        circuit.append([cirq.CNOT(qubits[0], qubits[1]) for i in range(2)])
        circuit = remove_double_cnots(circuit)
        empty_circuit = cirq.Circuit()
        self.assertEqual(circuit, empty_circuit)

    def test_instances(self):
        qubits = cirq.LineQubit.range(5)
        circuit = cirq.Circuit()
        for i in range(10):
            circuit = add_two_cnots(circuit, qubits)
                        
        circuit = remove_double_cnots(circuit)
        empty_circuit = cirq.Circuit()
        self.assertEqual(circuit, empty_circuit)

    def test_does_not_change_effect_of_circuit(self):
        n_qubits = 5
        n_templates = 30
        circuit = random_circuit(n_qubits, n_templates)
        expected_circuit = circuit.unfreeze(copy=True)
        circuit = remove_double_cnots(circuit)
        cirq.testing.assert_circuits_with_terminal_measurements_are_equivalent(actual=circuit, 
                                                                               reference=expected_circuit)

if __name__ == '__main__':
    unittest.main()
