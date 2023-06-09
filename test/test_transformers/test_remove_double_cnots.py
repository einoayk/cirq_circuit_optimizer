import unittest
import cirq

from src.generate_random_circuits.circuit_generator import add_two_cnots
from src.transformers.transformers import remove_double_cnots


class TestRemoveDoubleCnots(unittest.TestCase):

    def test_simple(self):
        qubits = cirq.LineQubit.range(2)
        circuit = cirq.Circuit()
        circuit.append([cirq.CNOT(qubits[0], qubits[1]) for i in range(2)])
        circuit = remove_double_cnots(circuit)
        empty_circuit = cirq.Circuit()
        if circuit != empty_circuit:
            self.fail("Double CNOTs not removed.")

    def test_multiple_double_cnots_on_random_qubits(self):
        qubits = cirq.LineQubit.range(5)
        circuit = cirq.Circuit()
        for i in range(10):

            circuit = add_two_cnots(circuit, qubits)
                        
        circuit = remove_double_cnots(circuit)
        empty_circuit = cirq.Circuit()
        if circuit != empty_circuit:
            self.fail("All double CNOTs not removed.")

if __name__ == '__main__':
    unittest.main()
