import streamlit as st
import numpy as np


def show_instructions():
    st.subheader("Instructions")

    psi = "|ψ>"
    board = np.array([[psi]*3 for _ in range(3)])
    st.write("Initial Board:")
    st.dataframe(board)

    st.markdown("""
    This is a **Quantum Tic Tac Toe** game where each move can collapse into either `|0>` or `|1>` due to **Quantum Superposition**!

    - You are `|1>`
    - Computer is `|0>`
    - The square numbers correspond to positions like this:
    """)

    numbering = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    st.dataframe(numbering)

    st.markdown("""
    When you select a position, it collapses into either `|0>` or `|1>`. 
    The first to align three of their collapsed states wins!
    """)