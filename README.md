# Quantum Tic Tac Toe & Quantum Computing Demos


A hands-on project demonstrating quantum computing principles through interactive games and simulations.


[View Live Demo](https://www.google.com)


## Features

* Quantum Tic Tac Toe: Play a quantum-inspired version of Tic Tac Toe with superposition states
* Qubit vs Classical Bit: Visualize the difference between classical and quantum bits
* Quantum Circuit Builder: Create and test quantum circuits with different gates
* Superposition & Entanglement: Interactive demonstrations of key quantum concepts
* Quantum Cryptography: Simulate the BB84 protocol for secure key exchange


## Quick Start

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/quantum-tic-tac-toe.git
    cd quantum-tic-tac-toe
    ```
    
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Run the application:
    ```
    streamlit run app.py
    ```


## Technologies Used

![Python](https://img.shields.io/badge/python-3.10.12-blue?style=flat-square)

![Streamlit](https://img.shields.io/badge/streamlit-1.38.0-FF4B4B?style=flat-square)

![Qiskit](https://img.shields.io/badge/qiskit-2.0.0-6929C4?style=flat-square)

**Framework & Libraries:**
- [NumPy](https://numpy.org/) - Scientific computing
- [Matplotlib](https://matplotlib.org/) - Visualization
- [Pandas](https://pandas.pydata.org/) - Data analysis


## Project Structure

```
quantum-tic-tac-toe/
├── app.py                     # Main application
├── game.py                    # Quantum Tic Tac Toe logic
├── game_instructions.py       # Game rules
├── game_about.py              # About the game
├── bit_vs_qubit.py            # Classical vs quantum bit demo
├── quantum_gates_circuits.py  # Quantum circuit builder
├── superpostion_entanglement.py # Quantum principles demo
├── quantum_cryptography_qkd.py # Cryptography demo
└── requirements.txt           # Dependencies
```

## Installation

1. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Run the application:

    ```
    streamlit run app.py
    ```
