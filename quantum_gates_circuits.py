import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import matplotlib.pyplot as plt

def display_quantum_gates_circuit():
    # Set page config
    # st.set_page_config(page_title="Quantum Circuit Builder", layout="centered")
    st.title("Quantum Gates & Circuits: Building Blocks of Quantum Algorithms")

    st.markdown("""
    Welcome to this simple quantum circuit builder.  
    You can add various quantum gates to build your own circuit and visualize it below.

    **Available Gates**: Hadamard (H), Pauli-X (X), Pauli-Y (Y), Pauli-Z (Z), CNOT (CX), SWAP, Toffoli (CCNOT), Controlled Phase Shift (CZ).
    """)

    # Constants
    default_qubits = 2  # Default number of qubits

    # Initialize session state
    if 'qc' not in st.session_state:
        st.session_state.qc = QuantumCircuit(default_qubits, default_qubits)

    if 'selected_gate_name' not in st.session_state:
        st.session_state.selected_gate_name = "Hadamard (H)"

    if 'single_qubit' not in st.session_state:
        st.session_state.single_qubit = 0

    if 'control_qubit' not in st.session_state:
        st.session_state.control_qubit = 0

    if 'target_qubit' not in st.session_state:
        st.session_state.target_qubit = 1

    if 'qubit_slider' not in st.session_state:
        st.session_state.qubit_slider = default_qubits

    qc = st.session_state.qc

    # --- Number of Qubits Selector ---
    num_qubits = st.slider(
        "Select number of qubits",
        min_value=1,
        max_value=10,
        value=st.session_state.qubit_slider,
        key="qubit_slider_interact"
    )

    # Sync widget with session state
    st.session_state.qubit_slider = num_qubits

    # Reset circuit if qubit count changes
    if 'last_qubits' not in st.session_state or st.session_state.last_qubits != num_qubits:
        st.session_state.qc = QuantumCircuit(num_qubits, num_qubits)
        st.session_state.last_qubits = num_qubits

    qc = st.session_state.qc

    # --- Gate Selection UI ---
    st.subheader("Choose a gate")

    gate_options = {
        "Hadamard (H)": "h",
        "Pauli-X (X)": "x",
        "Pauli-Y (Y)": "y",
        "Pauli-Z (Z)": "z",
        "CNOT (CX)": "cx",
        "SWAP": "swap",
        "Toffoli (CCNOT)": "ccx",
        "Controlled Phase Shift (CZ)": "cz"
    }

    selected_gate_name = st.selectbox(
        "Select a gate",
        list(gate_options.keys()),
        index=list(gate_options.keys()).index(st.session_state.selected_gate_name),
        key="gate_selector"
    )

    # Input fields shown one after another (no columns)
    st.markdown("### Gate Parameters")

    if selected_gate_name in ["CNOT (CX)", "SWAP", "Toffoli (CCNOT)", "Controlled Phase Shift (CZ)"]:
        control_qubit = st.number_input(
            f"Control Qubit (0–{num_qubits - 1})",
            min_value=0,
            max_value=num_qubits - 1,
            step=1,
            value=st.session_state.control_qubit,
            key="control_gate"
        )
        target_qubit = st.number_input(
            f"Target Qubit (0–{num_qubits - 1})",
            min_value=0,
            max_value=num_qubits - 1,
            step=1,
            value=st.session_state.target_qubit,
            key="target_gate"
        )
    else:
        single_qubit = st.number_input(
            f"Target Qubit (0–{num_qubits - 1})",
            min_value=0,
            max_value=num_qubits - 1,
            step=1,
            value=st.session_state.single_qubit,
            key="single_gate"
        )

    # Apply gate on button click
    st.subheader("Add Gate to Circuit")
    if st.button("Add Gate to Circuit"):
        gate_key = gate_options[selected_gate_name]
        if gate_key == "h":
            qc.h(single_qubit)
        elif gate_key == "x":
            qc.x(single_qubit)
        elif gate_key == "y":
            qc.y(single_qubit)
        elif gate_key == "z":
            qc.z(single_qubit)
        elif gate_key == "cx":
            qc.cx(control_qubit, target_qubit)
        elif gate_key == "swap":
            qc.swap(control_qubit, target_qubit)
        elif gate_key == "ccx":
            third_qubit = (control_qubit + 1) % num_qubits if num_qubits > 2 else 0
            qc.ccx(control_qubit, target_qubit, third_qubit)
        elif gate_key == "cz":
            qc.cz(control_qubit, target_qubit)

        st.success(f"{selected_gate_name} applied to the circuit.")

    # --- Display Current Circuit ---
    st.subheader("Your Quantum Circuit")
    st.text(qc.draw(output='text'))

    # --- Measure Circuit Button ---
    st.subheader("Measure Circuit")
    if st.button("Measure Circuit"):
        # Make a copy of the circuit and measure all qubits
        qc_meas = qc.copy()
        for i in range(num_qubits):
            qc_meas.measure(i, i)

        # Run on simulator
        backend = Aer.get_backend('qasm_simulator')
        compiled_qc = transpile(qc_meas, backend)
        job = backend.run(compiled_qc, shots=1000)
        result = job.result()
        counts = result.get_counts()

        # Plot histogram
        st.subheader("Measurement Results")
        fig, ax = plt.subplots()
        bars = ax.bar(counts.keys(), counts.values(), color=['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A869'])

        ax.set_xlabel("State")
        ax.set_ylabel("Count")
        ax.set_title("Measurement Outcomes")

        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10)

        st.pyplot(fig)

    # --- Reset Circuit Button ---
    st.subheader("Reset Circuit")
    if st.button("Reset Circuit"):
        # Reset circuit
        st.session_state.qc = QuantumCircuit(default_qubits, default_qubits)

        # Reset UI inputs
        st.session_state.selected_gate_name = "Hadamard (H)"
        st.session_state.single_qubit = 0
        st.session_state.control_qubit = 0
        st.session_state.target_qubit = 1

        # Reset number of qubits slider to default
        st.session_state.qubit_slider = default_qubits
        st.session_state.last_qubits = default_qubits

        # Force rerun to reflect changes in widgets
        st.rerun()

        st.success("Circuit and inputs reset to defaults!")

    # --- Optional: Short Gate Descriptions ---
    st.subheader("About the Gates")

    gate_descriptions = {
        "Hadamard (H)": "Puts a qubit into superposition.",
        "Pauli-X (X)": "Flips the qubit from |0⟩ to |1⟩.",
        "Pauli-Y (Y)": "Rotates the qubit around Y-axis by π radians.",
        "Pauli-Z (Z)": "Flips the phase of the qubit.",
        "CNOT (CX)": "Applies X gate to target if control is |1⟩.",
        "SWAP": "Swaps the states of two qubits.",
        "Toffoli (CCNOT)": "Applies X to target if both controls are |1⟩.",
        "Controlled Phase Shift (CZ)": "Adds a phase shift if both qubits are |1⟩."
    }

    for name, desc in gate_descriptions.items():
        st.markdown(f"- **{name}**: {desc}")