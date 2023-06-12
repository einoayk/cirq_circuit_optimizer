import unittest
import cirq

from src.generate_random_circuits.circuit_generator import add_cnots_with_different_targets
from src.transformers.transformers import combine_cnots


class TestCombineCnots(unittest.TestCase):

    def test_one_instance(self):
        qubits = cirq.LineQubit.range(5)
        circuit = cirq.Circuit()
        circuit.append([cirq.CNOT(qubits[0], qubits[i]) for i in range(1, 5)])           
        circuit = combine_cnots(circuit)
        expected_circuit = cirq.Circuit()
        op = 1
        for i in range(1,5):
            op = op * cirq.X(qubits[i])

        op = op.controlled_by(qubits[0])
        expected_circuit.append(op)
        if circuit != expected_circuit:
            self.fail("Combine CNOTs doesn't behave as expected")

    def test_multiple_instances(self):
        qubits = cirq.LineQubit.range(7)
        circuit = cirq.Circuit()
        circuit.append([cirq.CNOT(qubits[0], qubits[i]) for i in range(1, 5)])
        circuit.append(cirq.CNOT(qubits[3], qubits[0]))
        circuit.append([cirq.CNOT(qubits[3], qubits[i]) for i in range(4,7)])
        circuit.append([cirq.CNOT(qubits[6], qubits[i]) for i in range(5)])
        circuit = combine_cnots(circuit)
        expected_circuit = cirq.Circuit()
        op1 = 1
        op2 = 1
        op3 = 1
        for i in range(1,5):
            op1 = op1 * cirq.X(qubits[i])

        op1 = op1.controlled_by(qubits[0])
        op2 = op2 * cirq.X(qubits[0])
        for i in range(4, 7):
            op2 = op2 * cirq.X(qubits[i])

        op2 = op2.controlled_by(qubits[3])
        for i in range(5):
            op3 = op3 * cirq.X(qubits[i])

        op3 = op3.controlled_by(qubits[6])
        expected_circuit.append(op1)
        expected_circuit.append(op2)
        expected_circuit.append(op3)
        if circuit != expected_circuit:
            self.fail("Combine CNOTs doesn't behave as expected")   

if __name__ == '__main__':
    unittest.main()
