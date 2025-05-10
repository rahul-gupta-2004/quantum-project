import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import matplotlib.pyplot as plt
import random
import pandas as pd

def display_bits_vs_qubits():
    # st.set_page_config(page_title="Classical Bit vs Qubit", layout="wide")
    st.title("Classical Bit vs Quantum Bit (Qubit)")

    st.markdown("""
    This app demonstrates the **fundamental difference** between a classical bit and a quantum bit (qubit).

    - A **classical bit** can be in only one definite state: `0` or `1`.
    - A **qubit**, however, can exist in a **superposition** of both `0` and `1`.

    Below, we simulate measurements from both systems and explain what the results mean.
    """)

    # Slider for number of shots
    shots = st.slider("Number of Shots (Measurements)", min_value=100, max_value=10000, value=1000)

    # Run simulation button
    run_simulation = st.button("Run Simulation")

    if run_simulation:
        # --- Classical Bit Simulation ---
        classical_results = {'0': 0, '1': 0}
        for _ in range(shots):
            bit = str(random.randint(0, 1))
            classical_results[bit] += 1

        # --- Quantum Bit Simulation ---
        qc = QuantumCircuit(1, 1)
        qc.h(0)  # Apply Hadamard gate to create superposition
        qc.measure(0, 0)

        backend = Aer.get_backend('qasm_simulator')
        qc_compiled = transpile(qc, backend)

        job = backend.run(qc_compiled, shots=shots)
        result = job.result()
        qubit_counts = result.get_counts()

        # --- Display Results Side by Side ---
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Classical Bit")
            st.markdown("""
            This bar chart shows how many times the classical bit was measured as `0` or `1`.  
            Since this is a fair random choice, you should see roughly equal counts.
            """)

            fig, ax = plt.subplots()
            bars = ax.bar(classical_results.keys(), classical_results.values(), color=['#4E79A7', '#F28E2B'])
            ax.set_title("Classical Bit Measurement Outcomes")
            ax.set_xlabel("Bit Value")
            ax.set_ylabel("Frequency")

            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=10)

            st.pyplot(fig)

            st.markdown("""
            ### What does this graph mean?
            - The classical bit must choose **one definite state** before measurement.
            - In this case, we randomly pick either `0` or `1`.
            - Each measurement gives a clear result — no uncertainty after measurement.
            """)

        with col2:
            st.subheader("Quantum Bit (Qubit)")
            st.markdown("""
            This bar chart shows the outcomes when measuring a qubit in superposition.  
            The qubit has a **50% chance of collapsing to `0` or `1`** upon measurement.
            """)

            fig, ax = plt.subplots()
            bars = ax.bar(qubit_counts.keys(), qubit_counts.values(), color=['#4E79A7', '#F28E2B'])
            ax.set_title("Qubit Measurement Outcomes (Superposition)")
            ax.set_xlabel("Measured State")
            ax.set_ylabel("Frequency")

            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=10)

            st.pyplot(fig)

            st.markdown("""
            ### What does this graph mean?
            - Before measurement, the qubit is in a **superposition** of `0` and `1`.
            - When measured, it collapses probabilistically into one of the two states.
            - Unlike classical bits, the qubit can be in **multiple states at once**, until observed.
            
            > ⚠️ Note: Even though the probabilities are 50/50, the actual outcomes may vary slightly due to randomness in measurement.
            """)

        # Final Summary
        st.markdown("## Key Difference Explained")

        data = {
            "Feature": [
                "State",
                "Measurement Result",
                "Before Measurement",
                "Graph Interpretation"
            ],
            "Classical Bit": [
                "Only 0 or 1",
                "Always certain",
                "Already set",
                "Shows frequency of pre-determined values"
            ],
            "Quantum Bit (Qubit)": [
                "Can be in 0, 1, or both at once",
                "Probabilistic (unless not in superposition)",
                "In superposition (no definite value)",
                "Shows collapse of quantum state"
            ]
        }

        df = pd.DataFrame(data)
        df.index = df.index + 1
        st.table(df)
