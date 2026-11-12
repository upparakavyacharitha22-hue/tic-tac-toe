"""
Comprehensive automated unit tests for Tic Tac Toe game logic and GUI components.
"""

import unittest
import tkinter as tk
from main import (
    WINNING_COMBINATIONS,
    check_winner,
    check_draw,
    get_available_moves,
    minimax,
    get_best_ai_move,
    ModernTicTacToe,
)


class TestTicTacToeGameLogic(unittest.TestCase):
    """Tests all game logic functions."""

    def test_all_eight_winning_combinations_for_x(self):
        """Verifies that all 8 winning combinations are correctly recognized for X."""
        for combo in WINNING_COMBINATIONS:
            board = [""] * 9
            for idx in combo:
                board[idx] = "X"
            winner, winning_combo = check_winner(board)
            self.assertEqual(winner, "X", f"Failed for combo {combo}")
            self.assertEqual(winning_combo, combo, f"Wrong combo returned for {combo}")

    def test_all_eight_winning_combinations_for_o(self):
        """Verifies that all 8 winning combinations are correctly recognized for O."""
        for combo in WINNING_COMBINATIONS:
            board = [""] * 9
            for idx in combo:
                board[idx] = "O"
            winner, winning_combo = check_winner(board)
            self.assertEqual(winner, "O", f"Failed for combo {combo}")
            self.assertEqual(winning_combo, combo, f"Wrong combo returned for {combo}")

    def test_in_progress_game_has_no_winner(self):
        """Verifies that an in-progress board returns None, None."""
        board = [
            "X", "O", "X",
            "O", "X", "",
            "",  "",  ""
        ]
        winner, combo = check_winner(board)
        self.assertIsNone(winner)
        self.assertIsNone(combo)
        self.assertFalse(check_draw(board))

    def test_draw_condition_detected(self):
        """Verifies that a full board without 3-in-a-row is detected as a draw."""
        # Standard draw board:
        # X O X
        # X X O
        # O X O
        board = [
            "X", "O", "X",
            "X", "X", "O",
            "O", "X", "O"
        ]
        winner, combo = check_winner(board)
        self.assertIsNone(winner)
        self.assertTrue(check_draw(board))

    def test_full_board_with_winner_is_not_draw(self):
        """If 9 cells are filled but there is a 3-in-a-row, it is a WIN, not a draw."""
        board = [
            "X", "X", "X",
            "O", "O", "X",
            "X", "O", "O"
        ]
        winner, combo = check_winner(board)
        self.assertEqual(winner, "X")
        self.assertFalse(check_draw(board))

    def test_available_moves(self):
        """Verifies available move indices."""
        board = ["X", "", "O", "", "X", "O", "", "", ""]
        expected = [1, 3, 6, 7, 8]
        self.assertEqual(get_available_moves(board), expected)

    def test_ai_takes_immediate_winning_move(self):
        """AI should immediately complete its 3-in-a-row to win."""
        # AI is 'O'. Top row has 'O' at 0 and 1. Index 2 gives immediate win.
        board = [
            "O", "O", "",
            "X", "X", "",
            "",  "",  ""
        ]
        move = get_best_ai_move(board, ai_symbol="O", human_symbol="X", difficulty="Hard")
        self.assertEqual(move, 2)

    def test_ai_blocks_opponent_immediate_win(self):
        """AI should block the human from winning when human has 2-in-a-row."""
        # Human is 'X'. Left col has 'X' at 0 and 3. AI must block at 6.
        board = [
            "X", "O", "",
            "X", "",  "",
            "",  "",  ""
        ]
        move = get_best_ai_move(board, ai_symbol="O", human_symbol="X", difficulty="Hard")
        self.assertEqual(move, 6)

    def test_ai_unbeatable_minimax_never_loses(self):
        """
        Simulate games where Minimax AI plays against random moves.
        The AI ('O') must NEVER lose a single game.
        """
        import random
        for _ in range(25):
            board = [""] * 9
            current_turn = "X"
            while True:
                winner, _ = check_winner(board)
                if winner or check_draw(board):
                    break
                
                if current_turn == "X":
                    # Random human move
                    move = random.choice(get_available_moves(board))
                    board[move] = "X"
                    current_turn = "O"
                else:
                    move = get_best_ai_move(board, ai_symbol="O", human_symbol="X", difficulty="Hard")
                    board[move] = "O"
                    current_turn = "X"

            winner, _ = check_winner(board)
            self.assertNotEqual(winner, "X", "Minimax AI should never lose!")


class TestTicTacToeGUI(unittest.TestCase):
    """Tests Tkinter GUI creation, button clicks, restart and reset."""

    @classmethod
    def setUpClass(cls):
        # Create root window
        cls.root = tk.Tk()
        cls.root.withdraw()  # Hide window during test
        cls.app = ModernTicTacToe(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def setUp(self):
        self.app.reset_all()

    def test_initial_state(self):
        """Verifies initial game state and board layout."""
        self.assertEqual(len(self.app.buttons), 9)
        self.assertEqual(self.app.board, [""] * 9)
        self.assertEqual(self.app.current_player, "X")
        self.assertTrue(self.app.game_active)
        self.assertEqual(self.app.scores, {"X": 0, "O": 0, "Draws": 0})

    def test_clicking_cell_updates_state(self):
        """Clicking an empty cell marks it and switches turns."""
        self.app.on_cell_clicked(4)  # Click center
        self.assertEqual(self.app.board[4], "X")
        self.assertEqual(self.app.buttons[4]["text"], "X")
        self.assertEqual(self.app.current_player, "O")

    def test_clicking_occupied_cell_does_nothing(self):
        """Clicking an already occupied cell does not overwrite or change player."""
        self.app.on_cell_clicked(0)  # X marks 0
        self.assertEqual(self.app.current_player, "O")
        self.app.on_cell_clicked(0)  # Try to click 0 again
        self.assertEqual(self.app.board[0], "X")  # Still X
        self.assertEqual(self.app.current_player, "O")  # Still O's turn

    def test_two_player_win_detection_and_score(self):
        """Simulate a winning game for Player X in 2-player mode."""
        self.app.switch_mode("pvp")
        # Moves: X at 0, O at 3, X at 1, O at 4, X at 2 (Top row win for X)
        self.app.on_cell_clicked(0)  # X
        self.app.on_cell_clicked(3)  # O
        self.app.on_cell_clicked(1)  # X
        self.app.on_cell_clicked(4)  # O
        self.app.on_cell_clicked(2)  # X wins
        
        self.assertFalse(self.app.game_active)
        self.assertEqual(self.app.scores["X"], 1)
        self.assertEqual(self.app.scores["O"], 0)
        self.assertEqual(self.app.scores["Draws"], 0)

    def test_restart_round_keeps_scores(self):
        """Restart round clears the board but preserves the scoreboard."""
        self.app.scores["X"] = 3
        self.app.board[0] = "X"
        self.app.restart_round()
        
        self.assertEqual(self.app.board, [""] * 9)
        self.assertEqual(self.app.scores["X"], 3)
        self.assertTrue(self.app.game_active)
        self.assertEqual(self.app.current_player, "X")

    def test_reset_all_resets_scores_and_board(self):
        """Reset All zeroes out scores and clears the board."""
        self.app.scores = {"X": 5, "O": 2, "Draws": 3}
        self.app.board[0] = "X"
        self.app.reset_all()

        self.assertEqual(self.app.scores, {"X": 0, "O": 0, "Draws": 0})
        self.assertEqual(self.app.board, [""] * 9)
        self.assertTrue(self.app.game_active)


if __name__ == "__main__":
    unittest.main()

