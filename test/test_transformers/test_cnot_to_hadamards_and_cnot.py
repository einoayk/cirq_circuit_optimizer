import unittest
import cirq
from cirq.circuits import InsertStrategy

from src.generate_random_circuits.circuit_generator import add_cnots_with_different_targets
from src.transformers.transformers import cnot_to_hadamards_and_cnot

class TestCnotToHadamardsAndCnot(unittest.TestCase):

    def test_simple(self):
        qubits = cirq.LineQubit.range(2)
        circuit = cirq.Circuit()
        circuit.append(cirq.CNOT(qubits[0], qubits[1]))           
        circuit = cnot_to_hadamards_and_cnot(circuit)
        expected_circuit = cirq.Circuit()
        expected_circuit.append([cirq.H(qubits[0]), cirq.H(qubits[1])])
        expected_circuit.append(cirq.CNOT(qubits[1], qubits[0]))
        expected_circuit.append([cirq.H(qubits[0]), cirq.H(qubits[1])])
        if circuit != expected_circuit:
            self.fail("cnot_to_hadamards_and_cnot doesn't behave as expected")

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
            
        if circuit != expected_circuit:
            self.fail("cnot_to_hadamards_and_cnot doesn't behave as expected")

if __name__ == '__main__':
    unittest.main()