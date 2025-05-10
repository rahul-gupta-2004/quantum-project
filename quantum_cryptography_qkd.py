import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import random
import matplotlib.pyplot as plt

def display_quantum_cryptography():
    st.title("Quantum Cryptography: The Promise and the Reality")

    st.markdown("""
    Welcome to this interactive demo on **Quantum Key Distribution (QKD)** — one of the most promising applications of quantum computing.

    This page introduces the **BB84 protocol**, explains its **security advantages**, and shows how quantum mechanics can be used to create **unbreakable encryption keys**.
    """)

    # --- BB84 Simulation Functions ---
    def bb84_protocol(num_bits=50):
        # Alice generates random bits and bases
        alice_bits = [random.randint(0, 1) for _ in range(num_bits)]
        alice_bases = [random.randint(0, 1) for _ in range(num_bits)]  # 0 = Z-basis, 1 = X-basis

        # Alice encodes her bits into qubits
        qubits = []
        for bit, basis in zip(alice_bits, alice_bases):
            qc = QuantumCircuit(1, 1)
            if bit == 1:
                qc.x(0)
            if basis == 1:  # X-basis: apply Hadamard
                qc.h(0)
            qubits.append(qc)

        # Bob measures using his randomly chosen bases
        bob_bases = [random.randint(0, 1) for _ in range(num_bits)]
        bob_bits = []

        backend = Aer.get_backend('qasm_simulator')

        for i in range(num_bits):
            qc = qubits[i].copy()
            if bob_bases[i] == 1:
                qc.h(0)
            qc.measure(0, 0)

            # Use transpile and run instead of execute
            compiled_qc = transpile(qc, backend)
            job = backend.run(compiled_qc, shots=1)
            result = job.result()
            counts = result.get_counts()

            measured_bit = int(list(counts.keys())[0], 2)
            bob_bits.append(measured_bit)

        # Compare bases and extract matching key
        key = []
        matching_bases = []
        for i in range(num_bits):
            if alice_bases[i] == bob_bases[i]:
                key.append(alice_bits[i])
                matching_bases.append(i)

        return {
            "alice_bits": alice_bits,
            "alice_bases": alice_bases,
            "bob_bits": bob_bits,
            "bob_bases": bob_bases,
            "key": key,
            "matching_bases": matching_bases
        }

    # --- BB84 Protocol Section ---
    st.subheader("BB84 Protocol – Quantum Key Distribution")

    st.markdown("""
    ### What Is QKD?

    **Quantum Key Distribution (QKD)** is a method that uses quantum mechanics to securely exchange cryptographic keys between two parties — **Alice** and **Bob** — even in the presence of an eavesdropper — **Eve**.

    The most famous protocol is **BB84**, proposed by Charles Bennett and Gilles Brassard in 1984.

    ### How Does BB84 Work?
    1. **Alice** randomly chooses a bit (`0` or `1`) and a basis (`Z` or `X`) for each qubit.
    2. She encodes her bit using the chosen basis and sends it to Bob.
    3. **Bob** measures each qubit in his own randomly chosen basis.
    4. Alice and Bob publicly compare their bases and keep only the matching ones.
    5. They check for eavesdroppers by comparing a small portion of the key.

    This guarantees **information-theoretic security** based on the laws of physics, not computational hardness.
    """)

    # --- Side-by-Side: Sample Matching + Graph ---
    if st.button("Simulate BB84 Protocol"):
        result = bb84_protocol(num_bits=50)
        key_length = len(result['key'])
        mismatched = 50 - key_length

        st.success(f"Matched {key_length} bits out of 50 using same measurement basis.")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### Sample Matching Bases & Key Bits")
            sample = [(i, result['alice_bits'][i], result['bob_bits'][i]) for i in result['matching_bases'][:5]]
            for idx, abit, bbit in sample:
                st.write(f"Index {idx}: Alice={abit}, Bob={bbit}")

        with col2:
            # Plot histogram with reduced size
            fig, ax = plt.subplots(figsize=(5, 2.5))  # Compact figure size
            ax.bar(['Matching Basis', 'Mismatched Basis'], [key_length, mismatched], color=['#4E79A7', '#E15759'])
            ax.set_ylabel("Number of Bits")
            ax.set_title("Basis Matching in BB84 Protocol", fontsize=10)

            for p in ax.patches:
                ax.annotate(str(p.get_height()), (p.get_x() + 0.1, p.get_height() + 1), fontsize=8)

            st.pyplot(fig)

    # --- Security Section ---
    st.subheader("Why Is It Secure? Quantum Properties at Work")

    st.markdown("""
    #### Core Principles

    - **No-cloning theorem**: You cannot copy unknown quantum states → Eve can't clone qubits  
    - **Measurement collapse**: Any observation changes the state → Eve's presence is detectable  
    - **Random basis choice**: Prevents predictable interception  

    These principles make it possible to generate secure keys with **perfect secrecy**, independent of computational assumptions.
    """)

    # --- Comparison Table ---
    st.subheader("Classical vs. Quantum Cryptography")

    import pandas as pd

    comparison_data = {
        "Feature": [
            "Security Basis",
            "Key Exchange",
            "Long-Term Security",
            "Infrastructure Needs"
        ],
        "Classical Encryption": [
            "Math/Computational Hardness",
            "Vulnerable to MITM attacks",
            "At risk from future quantum computers",
            "Software-only"
        ],
        "Quantum Key Distribution": [
            "Laws of Physics",
            "Detectable eavesdropping",
            "Secure against all adversaries",
            "Requires quantum channels"
        ]
    }

    df = pd.DataFrame(comparison_data)
    st.table(df)

    # --- Practical Limitations ---
    st.subheader("Practical Limitations of QKD")

    st.markdown("""
    - **Distance limits** due to photon loss in fiber optics (~100–200 km)  
    - **Need for quantum channels** (e.g., single-photon sources)  
    - **High cost** and complexity  
    - **No authentication built-in** – must be combined with classical protocols  
    - **Limited speed** compared to classical systems
    """)

    # --- Real-World Use Cases ---
    st.subheader("Real-World Use Cases")

    st.markdown("""
    - Government and military secure communications  
    - Financial institutions  
    - Long-term archival data protection  
    - Satellite-based QKD experiments (e.g., China's Micius satellite)
    """)

    # --- Summary Section ---
    st.subheader("The Future of Quantum Cryptography")

    st.markdown("""
    Quantum Key Distribution offers a fundamentally new approach to secure communication. Unlike classical cryptography, which relies on assumptions about computational difficulty, QKD derives its security from the **laws of quantum mechanics**.

    ### Advantages
    - **Perfect forward secrecy** through fresh key generation  
    - **Eavesdropping detection** via quantum effects  
    - **Unbreakable encryption**, even against quantum computers

    ### Challenges
    - Limited distance and throughput  
    - High cost and infrastructure requirements  
    - Not yet scalable for mass internet use
    """)