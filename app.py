import streamlit as st
import numpy as np
from game import get_random_value, validate
import game_instructions
import game_about
import bit_vs_qubit
import quantum_cryptography_qkd
import quantum_gates_circuits
import superpostion_entanglement

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = np.full((3, 3), '|ψ>')
    st.session_state.available_moves = list(range(1, 10))
    st.session_state.game_over = False
    st.session_state.player_moves = []
    st.session_state.computer_moves = []

psi = '|ψ>'

# Sidebar menu
menu = [
        "Play Game", "Game Instructions", "About Game",
        "Classical Bit vs Qubit", "Quantum Gates and Circuits",
        "Superposition and Entanglement", "Quantum Cryptography"
        ]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Play Game":
    st.title("Quantum Tic Tac Toe")

    if st.session_state.game_over:
        st.warning("Game Over! Refresh to play again.")
        st.dataframe(st.session_state.board)
        st.stop()

    st.markdown("You: ``|1>`` | Computer: ``|0>``")

    move = st.selectbox("Choose your move (1–9):", st.session_state.available_moves)

    if st.button("Submit Move"):
        row = (move - 1) // 3
        col = (move - 1) % 3

        if st.session_state.board[row][col] == psi:
            # User's move
            user_value = get_random_value()
            st.session_state.board[row][col] = user_value
            st.session_state.player_moves.append(move)

            status, message = validate(st.session_state.board)
            if status == 0:
                st.success(message)
                st.session_state.game_over = True
                st.dataframe(st.session_state.board)
                st.stop()

            # Computer's move
            comp_move = None
            comp_row = comp_col = -1

            while True:
                comp_move = np.random.randint(1, 10)
                comp_row = (comp_move - 1) // 3
                comp_col = (comp_move - 1) % 3
                if st.session_state.board[comp_row][comp_col] == psi:
                    comp_value = get_random_value()
                    st.session_state.board[comp_row][comp_col] = comp_value
                    st.session_state.computer_moves.append(comp_move)
                    break

            status, message = validate(st.session_state.board)
            if status == 0:
                st.success(message)
                st.session_state.game_over = True

            # Remove used move
            st.session_state.available_moves.remove(move)

            # Rerun to reflect changes
            st.rerun()
        else:
            st.error("Position already taken. Choose another.")

    # Always display current board
    st.dataframe(st.session_state.board)

    # Display last move
    if st.session_state.player_moves:
        last_player_move = st.session_state.player_moves[-1]
        st.markdown(f"You: ``|1>`` chose position → ``{last_player_move}``")

    if st.session_state.computer_moves:
        last_comp_move = st.session_state.computer_moves[-1]
        st.markdown(f"Computer: ``|0>`` placed at → ``{last_comp_move}``")

    # Display full move history
    if st.session_state.player_moves or st.session_state.computer_moves:
        st.markdown("### Move History")
        for i in range(max(len(st.session_state.player_moves), len(st.session_state.computer_moves))):
            p_move = st.session_state.player_moves[i] if i < len(st.session_state.player_moves) else "---"
            c_move = st.session_state.computer_moves[i] if i < len(st.session_state.computer_moves) else "---"
            st.markdown(f"Player: ``{p_move}`` | Computer: ``{c_move}``")

elif choice == "Game Instructions":
    game_instructions.show_instructions()

elif choice == "About Game":
    game_about.show_about()

elif choice == "Classical Bit vs Qubit":
    bit_vs_qubit.display_bits_vs_qubits()

elif choice == "Quantum Gates and Circuits":
    quantum_gates_circuits.display_quantum_gates_circuit()

elif choice == "Superposition and Entanglement":
    superpostion_entanglement.display_superposition_entanglement()

elif choice == "Quantum Cryptography":
    quantum_cryptography_qkd.display_quantum_cryptography()