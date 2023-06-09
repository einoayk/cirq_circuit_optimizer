import unittest
import cirq

from src.generate_random_circuits.circuit_generator import add_two_hadamards
from src.transformers.transformers import remove_double_hadamards


class TestRemoveDoubleHadamards(unittest.TestCase):

    def test_simple(self):
        qubits = cirq.LineQubit.range(1)
        circuit = cirq.Circuit()
        circuit.append([cirq.H(qubits[0]) for i in range(2)])
        circuit = remove_double_hadamards(circuit)
        empty_circuit = cirq.Circuit()
        if circuit != empty_circuit:
            self.fail("Double hadamards not removed.")

    def test_multiple_double_hadamards_on_random_qubits(self):
        qubits = cirq.LineQubit.range(5)
        circuit = cirq.Circuit()
        for i in range(10):

            circuit = add_two_hadamards(circuit, qubits) 

        circuit = remove_double_hadamards(circuit)
        empty_circuit = cirq.Circuit()
        if circuit != empty_circuit:
            self.fail("All double hadamards not removed.")
            
if __name__ == '__main__':
    unittest.main()
