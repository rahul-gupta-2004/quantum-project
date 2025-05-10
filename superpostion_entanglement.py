import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def display_superposition_entanglement():
    # st.set_page_config(page_title="Superposition & Entanglement", layout="wide")
    st.title("The Role of Superposition and Entanglement in Quantum Computing")

    st.markdown("""
    This interactive demo explains two fundamental quantum phenomena — **superposition** and **entanglement**, and shows how they enable **quantum parallelism**.

    Use the buttons below to simulate each concept and see how they differ from classical behavior.
    """)

    # --- Helper Function to Run Circuit ---
    def run_circuit(qc, shots=1000):
        backend = Aer.get_backend('qasm_simulator')
        compiled_qc = transpile(qc, backend)
        job = backend.run(compiled_qc, shots=shots)
        result = job.result()
        counts = result.get_counts()
        return counts


    # --- Superposition Section ---
    st.subheader("1. Superposition: One Qubit in Two States at Once")

    st.markdown("""
    In classical computing, a bit is either 0 or 1.  
    A **qubit in superposition** can be in both states at once:

    $$
    |\\psi\\rangle = \\frac{|0\\rangle + |1\\rangle}{\\sqrt{2}}
    $$

    This allows **parallel computation** on multiple inputs simultaneously.
    """)

    if st.button("Simulate Superposition"):
        qc_super = QuantumCircuit(1, 1)
        qc_super.h(0)
        qc_super.measure(0, 0)

        counts = run_circuit(qc_super)
        fig, ax = plt.subplots()
        bars = ax.bar(counts.keys(), counts.values(), color=['#4E79A7', '#F28E2B'])
        ax.set_title("Measurement Outcomes (Superposition)")
        ax.set_xlabel("State")
        ax.set_ylabel("Count")

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10)

        st.pyplot(fig)
        st.code(qc_super.draw(output='text'))


    # --- Entanglement Section ---
    st.subheader("2. Entanglement: Spooky Action at a Distance")

    st.markdown("""
    **Entanglement** links two or more qubits so their states are correlated — even across large distances.

    We create entanglement using a **Bell state**:

    $$
    |\\Phi^+\\rangle = \\frac{|00\\rangle + |11\\rangle}{\\sqrt{2}}
    $$

    Measuring one qubit instantly determines the other’s state.
    """)

    if st.button("Simulate Entanglement"):
        qc_entangle = QuantumCircuit(2, 2)
        qc_entangle.h(0)
        qc_entangle.cx(0, 1)
        qc_entangle.measure([0, 1], [0, 1])

        counts = run_circuit(qc_entangle)
        fig, ax = plt.subplots()
        bars = ax.bar(counts.keys(), counts.values(), color=['#4E79A7', '#F28E2B', '#E15759', '#76B7B2'])
        ax.set_title("Measurement Outcomes (Entanglement)")
        ax.set_xlabel("State")
        ax.set_ylabel("Count")

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10)

        st.pyplot(fig)
        st.code(qc_entangle.draw(output='text'))


    # --- Enhanced Summary Section ---
    st.subheader("Superposition + Entanglement = Quantum Power")

    st.markdown("""
    Quantum computing derives its power from two uniquely quantum phenomena: **superposition** and **entanglement**.

    ### 1. Superposition – Computing in Parallel Universes

    | Classical | Quantum |
    |----------|---------|
    | A bit is either `0` or `1` | A qubit can be both `|0⟩` and `|1⟩` at the same time |

    This allows a quantum computer to process **all possible inputs simultaneously**, enabling **massive parallelism**.

    For example:
    - With **2 qubits**, you can represent: `|00⟩`, `|01⟩`, `|10⟩`, `|11⟩` all at once.
    - With **n qubits**, you can represent **$2^n$** states — exponentially more than classical bits!

    ---

    ### 2. Entanglement – Connected Qubits Across Space

    When qubits are entangled, their states become **correlated**, no matter how far apart they are.

    Example:
    $$
    |\\Phi^+\\rangle = \\frac{|00\\rangle + |11\\rangle}{\\sqrt{2}}
    $$

    Measuring one qubit instantly determines the other's state — even if it's on the other side of the universe!

    Entanglement enables:
    - **Quantum teleportation**
    - **Secure communication**
    - **Highly efficient algorithms**
    """)