import streamlit as st

def show_about():
    st.subheader("About Quantum Tic Tac Toe")

    st.markdown("""
    This game is designed to introduce players to the concept of **Quantum Superposition** in an engaging way.

    Built with:
    - Python
    - Qiskit (for quantum simulation)
    - Streamlit (for UI)

    ### How It Works

    Each move starts in a **superposition state**: `|ψ>`. When you choose a square, it collapses into either `|0>` or `|1>` randomly.

    This mimics how quantum bits behave in real quantum computing systems.

    ### Quantum Superposition Formula

    $$
    |\psi\\rangle = \\alpha |0\\rangle + \\beta |1\\rangle
    $$
    """)