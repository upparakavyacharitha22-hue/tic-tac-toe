"""
=============================================================================
                       TIC TAC TOE - MODERN GUI
=============================================================================
A complete, modern, and interactive Tic Tac Toe game built using ONLY Python
and Tkinter.

Features:
- Two Player Mode (Local pass-and-play)
- Player vs Computer Mode (Smart AI / Minimax)
- Modern Dark-Themed UI with Purple and Blue Accents
- Live Scoreboard (Player X, Player O / Computer, Draws)
- Animated / Highlighted Winning Line Combinations
- Interactive Button Hover Effects
- Restart Round & Reset Scores functionality
=============================================================================
"""

import tkinter as tk
from tkinter import font as tkfont
import random
import time


# =============================================================================
# GAME LOGIC FUNCTIONS (Independent of GUI)
# =============================================================================

WINNING_COMBINATIONS = [
    (0, 1, 2),  # Top row
    (3, 4, 5),  # Middle row
    (6, 7, 8),  # Bottom row
    (0, 3, 6),  # Left column
    (1, 4, 7),  # Middle column
    (2, 5, 8),  # Right column
    (0, 4, 8),  # Diagonal from top-left
    (2, 4, 6),  # Diagonal from top-right
]


def check_winner(board):
    """
    Checks if there is a winner on the board.
    
    Parameters:
        board (list): A list of 9 elements representing the board cells
                      ('X', 'O', or '').
                      
    Returns:
        tuple: (winner_symbol, winning_combination) if a winner is found.
               (None, None) if there is no winner yet.
    """
    for combo in WINNING_COMBINATIONS:
        a, b, c = combo
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a], combo
    return None, None


def check_draw(board):
    """
    Checks if the game has ended in a draw (all cells filled without a winner).
    
    Parameters:
        board (list): A list of 9 elements representing the board cells.
        
    Returns:
        bool: True if the board is full and there is no winner, False otherwise.
    """
    winner, _ = check_winner(board)
    if winner is None and all(cell != "" for cell in board):
        return True
    return False


def get_available_moves(board):
    """
    Returns a list of indices (0-8) that are currently empty.
    """
    return [i for i, cell in enumerate(board) if cell == ""]


def minimax(board, depth, is_maximizing, ai_symbol, human_symbol):
    """
    Minimax algorithm to compute the optimal score for the AI.
    
    Parameters:
        board (list): Current state of the board.
        depth (int): Depth of the search tree.
        is_maximizing (bool): True if evaluating AI moves, False for human.
        ai_symbol (str): The symbol used by the AI ('O').
        human_symbol (str): The symbol used by the human ('X').
        
    Returns:
        int: Heuristic score for the board position.
    """
    winner, _ = check_winner(board)
    if winner == ai_symbol:
        return 10 - depth
    elif winner == human_symbol:
        return depth - 10
    elif check_draw(board):
        return 0

    if is_maximizing:
        best_score = -1000
        for move in get_available_moves(board):
            board[move] = ai_symbol
            score = minimax(board, depth + 1, False, ai_symbol, human_symbol)
            board[move] = ""
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = 1000
        for move in get_available_moves(board):
            board[move] = human_symbol
            score = minimax(board, depth + 1, True, ai_symbol, human_symbol)
            board[move] = ""
            best_score = min(best_score, score)
        return best_score


def get_best_ai_move(board, ai_symbol="O", human_symbol="X", difficulty="Hard"):
    """
    Computes the AI's next move based on the selected difficulty level.
    
    Parameters:
        board (list): Current board state.
        ai_symbol (str): Symbol for the AI ('O').
        human_symbol (str): Symbol for the human ('X').
        difficulty (str): 'Easy', 'Medium', or 'Hard'.
        
    Returns:
        int: The index (0-8) of the chosen move.
    """
    available_moves = get_available_moves(board)
    if not available_moves:
        return None

    # Easy Mode: Completely random move
    if difficulty == "Easy":
        return random.choice(available_moves)

    # Medium Mode: 60% chance to play optimal move, 40% random move
    if difficulty == "Medium":
        if random.random() < 0.40:
            return random.choice(available_moves)

    # Hard / Minimax Mode: Unbeatable optimal move
    # 1. Quick check if AI can win in 1 move
    for move in available_moves:
        board[move] = ai_symbol
        winner, _ = check_winner(board)
        board[move] = ""
        if winner == ai_symbol:
            return move

    # 2. Quick check if human can win in 1 move -> Block them
    for move in available_moves:
        board[move] = human_symbol
        winner, _ = check_winner(board)
        board[move] = ""
        if winner == human_symbol:
            return move

    # 3. Minimax decision for optimal strategy
    best_score = -1000
    best_move = random.choice(available_moves)

    for move in available_moves:
        board[move] = ai_symbol
        score = minimax(board, 0, False, ai_symbol, human_symbol)
        board[move] = ""
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


# =============================================================================
# GUI IMPLEMENTATION WITH TKINTER
# =============================================================================

# Theme Palette (Modern Dark Theme with Purple & Blue accents)
THEME = {
    "bg_main": "#0f111a",         # Deep midnight dark background
    "bg_card": "#1a1d2e",         # Dark slate card container
    "bg_board": "#131625",        # Board container background
    "cell_normal": "#24283b",     # Normal cell button background
    "cell_hover": "#2f354f",      # Cell button hover background
    "cell_active": "#1f2232",     # Cell button pressed background
    
    # Accent Colors
    "purple_primary": "#8b5cf6",  # Vibrant Purple
    "purple_glow": "#a78bfa",     # Soft purple
    "blue_primary": "#3b82f6",    # Electric Blue
    "blue_glow": "#60a5fa",      # Light blue
    
    # Player Symbols
    "color_x": "#38bdf8",         # Bright Sky Blue for X
    "color_o": "#ec4899",         # Bright Pink/Magenta for O
    
    # Game Outcomes
    "win_bg": "#10b981",          # Emerald Green highlight for winning cells
    "win_fg": "#0f172a",          # Dark text on win highlight
    "draw_bg": "#f59e0b",         # Warm amber highlight for draw
    "draw_fg": "#0f172a",         # Dark text on draw highlight
    
    # Text colors
    "text_primary": "#f8fafc",    # Pure white / light text
    "text_secondary": "#94a3b8",  # Slate muted text
    "text_muted": "#64748b",      # Darker muted text
}


class ModernTicTacToe:
    """
    Main Application Class for the Modern Tkinter Tic Tac Toe game.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Python Edition")
        self.root.geometry("480x700")
        self.root.resizable(False, False)
        self.root.configure(bg=THEME["bg_main"])

        # Center the window on the user's screen
        self._center_window(480, 700)

        # Game State
        self.board = [""] * 9
        self.current_player = "X"
        self.game_mode = "pvp"         # 'pvp' (Two Players) or 'ai' (vs Computer)
        self.ai_difficulty = "Hard"    # 'Easy', 'Medium', or 'Hard'
        self.game_active = True
        self.is_ai_thinking = False

        # Score Tracking
        self.scores = {
            "X": 0,
            "O": 0,
            "Draws": 0
        }

        # Button Widgets storage
        self.buttons = []

        # Setup Fonts
        self._init_fonts()

        # Build UI Sections
        self._create_header()
        self._create_mode_selector()
        self._create_scoreboard()
        self._create_turn_indicator()
        self._create_board()
        self._create_control_panel()

    def _center_window(self, width, height):
        """Centers the Tkinter window on the primary screen."""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _init_fonts(self):
        """Configures modern typography using system fonts."""
        self.font_title = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.font_subtitle = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        self.font_status = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.font_score_num = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.font_score_label = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        self.font_cell = tkfont.Font(family="Segoe UI", size=32, weight="bold")
        self.font_btn = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.font_mode = tkfont.Font(family="Segoe UI", size=9, weight="bold")

    # -------------------------------------------------------------------------
    # UI CREATION METHODS
    # -------------------------------------------------------------------------

    def _create_header(self):
        """Builds the top header with glowing title and purple accent line."""
        header_frame = tk.Frame(self.root, bg=THEME["bg_main"])
        header_frame.pack(fill="x", pady=(18, 6))

        # Title Label
        title_label = tk.Label(
            header_frame,
            text="TIC TAC TOE",
            font=self.font_title,
            fg=THEME["purple_glow"],
            bg=THEME["bg_main"],
            letter_spacing=2 if hasattr(tk.Label, "letter_spacing") else None
        )
        title_label.pack()

        # Subtitle
        sub_label = tk.Label(
            header_frame,
            text="CLASSIC STRATEGY • PYTHON TKINTER",
            font=self.font_subtitle,
            fg=THEME["text_muted"],
            bg=THEME["bg_main"]
        )
        sub_label.pack(pady=(2, 0))

    def _create_mode_selector(self):
        """Creates the modern mode switch buttons and AI difficulty selector."""
        self.mode_container = tk.Frame(self.root, bg=THEME["bg_main"])
        self.mode_container.pack(fill="x", padx=36, pady=(10, 6))

        # Card container for mode toggle
        toggle_card = tk.Frame(self.mode_container, bg=THEME["bg_card"], padx=4, pady=4)
        toggle_card.pack(fill="x")

        # Two Player Button
        self.btn_pvp = tk.Button(
            toggle_card,
            text="👥 Two Players",
            font=self.font_mode,
            bg=THEME["purple_primary"],
            fg=THEME["text_primary"],
            activebackground=THEME["purple_glow"],
            activeforeground=THEME["text_primary"],
            relief="flat",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=lambda: self.switch_mode("pvp")
        )
        self.btn_pvp.pack(side="left", expand=True, fill="x", padx=(0, 2))

        # Player vs AI Button
        self.btn_ai = tk.Button(
            toggle_card,
            text="🤖 Player vs AI",
            font=self.font_mode,
            bg=THEME["cell_normal"],
            fg=THEME["text_secondary"],
            activebackground=THEME["cell_hover"],
            activeforeground=THEME["text_primary"],
            relief="flat",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=lambda: self.switch_mode("ai")
        )
        self.btn_ai.pack(side="right", expand=True, fill="x", padx=(2, 0))

        # AI Difficulty selector frame (Initially hidden, shown when AI mode selected)
        self.diff_frame = tk.Frame(self.mode_container, bg=THEME["bg_main"])
        
        diff_label = tk.Label(
            self.diff_frame,
            text="AI Difficulty:",
            font=self.font_subtitle,
            fg=THEME["text_secondary"],
            bg=THEME["bg_main"]
        )
        diff_label.pack(side="left", padx=(4, 8))

        self.diff_buttons = {}
        for diff in ["Easy", "Medium", "Hard"]:
            btn = tk.Button(
                self.diff_frame,
                text=diff,
                font=self.font_subtitle,
                bg=THEME["purple_primary"] if diff == "Hard" else THEME["cell_normal"],
                fg=THEME["text_primary"] if diff == "Hard" else THEME["text_secondary"],
                relief="flat",
                bd=0,
                padx=8,
                pady=2,
                cursor="hand2",
                command=lambda d=diff: self.set_ai_difficulty(d)
            )
            btn.pack(side="left", padx=2)
            self.diff_buttons[diff] = btn

    def _create_scoreboard(self):
        """Creates the 3 score metric cards (X Wins, Draws, O/AI Wins)."""
        score_frame = tk.Frame(self.root, bg=THEME["bg_main"])
        score_frame.pack(fill="x", padx=36, pady=(6, 6))

        # Card 1: Player X
        card_x = tk.Frame(score_frame, bg=THEME["bg_card"], padx=10, pady=8)
        card_x.pack(side="left", expand=True, fill="x", padx=(0, 4))
        
        self.label_title_x = tk.Label(
            card_x,
            text="PLAYER X",
            font=self.font_score_label,
            fg=THEME["color_x"],
            bg=THEME["bg_card"]
        )
        self.label_title_x.pack()

        self.score_x_label = tk.Label(
            card_x,
            text="0",
            font=self.font_score_num,
            fg=THEME["text_primary"],
            bg=THEME["bg_card"]
        )
        self.score_x_label.pack()

        # Card 2: Draws
        card_draw = tk.Frame(score_frame, bg=THEME["bg_card"], padx=10, pady=8)
        card_draw.pack(side="left", expand=True, fill="x", padx=2)
        
        label_title_draw = tk.Label(
            card_draw,
            text="DRAWS",
            font=self.font_score_label,
            fg=THEME["text_secondary"],
            bg=THEME["bg_card"]
        )
        label_title_draw.pack()

        self.score_draw_label = tk.Label(
            card_draw,
            text="0",
            font=self.font_score_num,
            fg=THEME["text_primary"],
            bg=THEME["bg_card"]
        )
        self.score_draw_label.pack()

        # Card 3: Player O / Computer
        card_o = tk.Frame(score_frame, bg=THEME["bg_card"], padx=10, pady=8)
        card_o.pack(side="right", expand=True, fill="x", padx=(4, 0))
        
        self.label_title_o = tk.Label(
            card_o,
            text="PLAYER O",
            font=self.font_score_label,
            fg=THEME["color_o"],
            bg=THEME["bg_card"]
        )
        self.label_title_o.pack()

        self.score_o_label = tk.Label(
            card_o,
            text="0",
            font=self.font_score_num,
            fg=THEME["text_primary"],
            bg=THEME["bg_card"]
        )
        self.score_o_label.pack()

    def _create_turn_indicator(self):
        """Creates the active player badge and status indicator banner."""
        self.status_container = tk.Frame(self.root, bg=THEME["bg_main"])
        self.status_container.pack(fill="x", padx=36, pady=(6, 10))

        self.status_card = tk.Frame(self.status_container, bg=THEME["bg_card"], pady=6)
        self.status_card.pack(fill="x")

        self.status_label = tk.Label(
            self.status_card,
            text="Player X's Turn",
            font=self.font_status,
            fg=THEME["color_x"],
            bg=THEME["bg_card"]
        )
        self.status_label.pack()

    def _create_board(self):
        """Creates the 3x3 interactive game grid with 9 styled buttons."""
        board_container = tk.Frame(
            self.root,
            bg=THEME["bg_board"],
            padx=10,
            pady=10
        )
        board_container.pack(padx=36, pady=4)

        # Configure 3x3 uniform grid
        for i in range(3):
            board_container.grid_rowconfigure(i, weight=1, minsize=96)
            board_container.grid_columnconfigure(i, weight=1, minsize=96)

        self.buttons = []
        for index in range(9):
            row = index // 3
            col = index % 3

            btn = tk.Button(
                board_container,
                text="",
                font=self.font_cell,
                bg=THEME["cell_normal"],
                fg=THEME["text_primary"],
                activebackground=THEME["cell_active"],
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda idx=index: self.on_cell_clicked(idx)
            )
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

            # Mouse hover animations
            btn.bind("<Enter>", lambda event, idx=index: self._on_cell_enter(idx))
            btn.bind("<Leave>", lambda event, idx=index: self._on_cell_leave(idx))

            self.buttons.append(btn)

    def _create_control_panel(self):
        """Creates Restart Round and Reset Game / New Game buttons."""
        controls_frame = tk.Frame(self.root, bg=THEME["bg_main"])
        controls_frame.pack(fill="x", padx=36, pady=(16, 12))

        # Restart Game Button (Clears board for new round)
        self.btn_restart = tk.Button(
            controls_frame,
            text="🔄 Restart Round",
            font=self.font_btn,
            bg=THEME["purple_primary"],
            fg=THEME["text_primary"],
            activebackground=THEME["purple_glow"],
            activeforeground=THEME["text_primary"],
            relief="flat",
            bd=0,
            padx=14,
            pady=10,
            cursor="hand2",
            command=self.restart_round
        )
        self.btn_restart.pack(side="left", expand=True, fill="x", padx=(0, 6))

        # Reset All Button (Clears board & scores)
        self.btn_reset_all = tk.Button(
            controls_frame,
            text="✨ Reset All",
            font=self.font_btn,
            bg=THEME["cell_normal"],
            fg=THEME["text_secondary"],
            activebackground=THEME["cell_hover"],
            activeforeground=THEME["text_primary"],
            relief="flat",
            bd=0,
            padx=14,
            pady=10,
            cursor="hand2",
            command=self.reset_all
        )
        self.btn_reset_all.pack(side="right", expand=True, fill="x", padx=(6, 0))

    # -------------------------------------------------------------------------
    # INTERACTION & EVENT HANDLERS
    # -------------------------------------------------------------------------

    def _on_cell_enter(self, index):
        """Highlights cell on hover if empty and game is active."""
        if self.game_active and not self.is_ai_thinking and self.board[index] == "":
            self.buttons[index].configure(bg=THEME["cell_hover"])

    def _on_cell_leave(self, index):
        """Restores cell background when mouse leaves if cell has not won."""
        if self.buttons[index]["bg"] == THEME["cell_hover"]:
            self.buttons[index].configure(bg=THEME["cell_normal"])

    def on_cell_clicked(self, index):
        """
        Handles user click on a cell button.
        
        Parameters:
            index (int): Cell index from 0 to 8.
        """
        # Ignore clicks if game is over, occupied, or AI is processing
        if not self.game_active or self.is_ai_thinking or self.board[index] != "":
            return

        # Execute move for human player
        self.execute_move(index, self.current_player)

        # In AI mode, if game is still active, trigger the computer's turn
        if self.game_active and self.game_mode == "ai" and self.current_player == "O":
            self.is_ai_thinking = True
            self.status_label.configure(
                text="🤖 Computer is thinking...",
                fg=THEME["color_o"]
            )
            # Add a realistic small delay (350ms) for natural gameplay feel
            self.root.after(350, self.execute_ai_turn)

    def execute_move(self, index, player):
        """
        Executes a move on the board for the specified player.
        
        Parameters:
            index (int): The index of the cell (0-8).
            player (str): 'X' or 'O'.
        """
        self.board[index] = player
        color = THEME["color_x"] if player == "X" else THEME["color_o"]
        
        self.buttons[index].configure(
            text=player,
            fg=color,
            bg=THEME["cell_normal"]
        )

        # Check for victory
        winner, winning_combo = check_winner(self.board)
        if winner:
            self.handle_game_win(winner, winning_combo)
            return

        # Check for draw
        if check_draw(self.board):
            self.handle_game_draw()
            return

        # Switch Player
        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_turn_status()

    def execute_ai_turn(self):
        """Executes the AI's calculated move."""
        if not self.game_active:
            self.is_ai_thinking = False
            return

        best_move = get_best_ai_move(
            self.board,
            ai_symbol="O",
            human_symbol="X",
            difficulty=self.ai_difficulty
        )

        self.is_ai_thinking = False

        if best_move is not None:
            self.execute_move(best_move, "O")

    def handle_game_win(self, winner, winning_combo):
        """
        Handles winning state: highlights winning line, updates score and status.
        """
        self.game_active = False
        self.scores[winner] += 1
        self._refresh_scoreboard_display()

        # Highlight the 3 winning buttons
        for idx in winning_combo:
            self.buttons[idx].configure(
                bg=THEME["win_bg"],
                fg=THEME["win_fg"]
            )

        # Status message
        if self.game_mode == "ai":
            if winner == "X":
                msg = "🎉 You Won the Game!"
                col = THEME["color_x"]
            else:
                msg = "🤖 Computer Won the Game!"
                col = THEME["color_o"]
        else:
            msg = f"🎉 Player {winner} Wins!"
            col = THEME["color_x"] if winner == "X" else THEME["color_o"]

        self.status_label.configure(text=msg, fg=col)

    def handle_game_draw(self):
        """
        Handles draw state: highlights all cells in amber and updates score.
        """
        self.game_active = False
        self.scores["Draws"] += 1
        self._refresh_scoreboard_display()

        # Highlight all cells with warm draw color
        for btn in self.buttons:
            btn.configure(
                bg=THEME["draw_bg"],
                fg=THEME["draw_fg"]
            )

        self.status_label.configure(
            text="🤝 It's a Draw! Well Played!",
            fg=THEME["draw_bg"]
        )

    def update_turn_status(self):
        """Updates the status card to show whose turn it is."""
        if self.game_mode == "ai":
            if self.current_player == "X":
                text = "Player X's Turn (Your Turn)"
                fg = THEME["color_x"]
            else:
                text = "Computer's Turn (O)"
                fg = THEME["color_o"]
        else:
            text = f"Player {self.current_player}'s Turn"
            fg = THEME["color_x"] if self.current_player == "X" else THEME["color_o"]

        self.status_label.configure(text=text, fg=fg)

    def _refresh_scoreboard_display(self):
        """Updates the numeric scores displayed on the scoreboard cards."""
        self.score_x_label.configure(text=str(self.scores["X"]))
        self.score_draw_label.configure(text=str(self.scores["Draws"]))
        self.score_o_label.configure(text=str(self.scores["O"]))

    # -------------------------------------------------------------------------
    # MODE SWITCHING & GAME CONTROL
    # -------------------------------------------------------------------------

    def switch_mode(self, mode):
        """
        Switches between 'pvp' (Two Players) and 'ai' (Player vs Computer).
        """
        if self.game_mode == mode:
            return

        self.game_mode = mode

        if mode == "pvp":
            self.btn_pvp.configure(
                bg=THEME["purple_primary"],
                fg=THEME["text_primary"]
            )
            self.btn_ai.configure(
                bg=THEME["cell_normal"],
                fg=THEME["text_secondary"]
            )
            self.diff_frame.pack_forget()
            self.label_title_o.configure(text="PLAYER O")
        else:
            self.btn_ai.configure(
                bg=THEME["purple_primary"],
                fg=THEME["text_primary"]
            )
            self.btn_pvp.configure(
                bg=THEME["cell_normal"],
                fg=THEME["text_secondary"]
            )
            self.diff_frame.pack(fill="x", pady=(6, 0))
            self.label_title_o.configure(text="COMPUTER")

        # Restart round when switching modes
        self.restart_round()

    def set_ai_difficulty(self, diff):
        """Sets AI difficulty level ('Easy', 'Medium', 'Hard')."""
        self.ai_difficulty = diff
        for name, btn in self.diff_buttons.items():
            if name == diff:
                btn.configure(
                    bg=THEME["purple_primary"],
                    fg=THEME["text_primary"]
                )
            else:
                btn.configure(
                    bg=THEME["cell_normal"],
                    fg=THEME["text_secondary"]
                )

    def restart_round(self):
        """Clears the game board and starts a new round keeping scores."""
        self.board = [""] * 9
        self.current_player = "X"
        self.game_active = True
        self.is_ai_thinking = False

        for btn in self.buttons:
            btn.configure(
                text="",
                bg=THEME["cell_normal"],
                fg=THEME["text_primary"]
            )

        self.update_turn_status()

    def reset_all(self):
        """Resets the game board AND resets the scoreboard to 0."""
        self.scores = {"X": 0, "O": 0, "Draws": 0}
        self._refresh_scoreboard_display()
        self.restart_round()


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

def main():
    """Initializes and runs the Tic Tac Toe GUI application."""
    root = tk.Tk()
    app = ModernTicTacToe(root)
    root.mainloop()


if __name__ == "__main__":
    main()

