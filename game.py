from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np


def quantum_superposition():
    """Generates a random |0> or |1> using quantum superposition."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    simulator = AerSimulator()
    result = simulator.run(qc).result().get_counts()
    outcome = max(result, key=result.get)  # Get most probable result
    return f"|{outcome}>"


def get_random_value():
    """Returns either |0> or |1> randomly using quantum circuit."""
    return quantum_superposition()


def validate(board):
    """
    Checks if any player has won or if it's a draw.
    Returns:
        0 if game ends (win or draw)
        1 if game continues
    """
    zero_ket = '|0>'
    one_ket = '|1>'

    # Check diagonals
    if board[0, 0] == board[1, 1] == board[2, 2] == one_ket:
        return 0, "User wins!"
    if board[0, 0] == board[1, 1] == board[2, 2] == zero_ket:
        return 0, "Computer wins!"
    if board[0, 2] == board[1, 1] == board[2, 0] == one_ket:
        return 0, "User wins!"
    if board[0, 2] == board[1, 1] == board[2, 0] == zero_ket:
        return 0, "Computer wins!"

    # Check rows
    for row in range(3):
        if all(cell == one_ket for cell in board[row]):
            return 0, "User wins!"
        if all(cell == zero_ket for cell in board[row]):
            return 0, "Computer wins!"

    # Check columns
    for col in range(3):
        if all(cell == one_ket for cell in board[:, col]):
            return 0, "User wins!"
        if all(cell == zero_ket for cell in board[:, col]):
            return 0, "Computer wins!"

    # Check draw
    if '|ψ>' not in board:
        return 0, "It is a draw!"

    return 1, ""  # Continue game