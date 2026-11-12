# 🎮 Modern Tic Tac Toe Game (Python & Tkinter)

A complete, professional, interactive, and dark-themed **Tic Tac Toe** desktop game built using **Python** and **Tkinter**.

No external dependencies, web technologies, or complex frameworks required — just pure, elegant Python!

---

## 🌟 Key Features

### 1. Modern & Attractive Dark-Themed UI
- **Futuristic Palette:** Deep midnight slate background with electric blue (`#38bdf8`) and neon magenta/pink (`#ec4899`) player colors, along with royal purple (`#8b5cf6`) accents.
- **Interactive Cells:** Smooth mouse hover effects on available cells, giving visual feedback before clicking.
- **Dynamic Turn Indicators:** Status banner that clearly displays whose turn it is with matching player colors.
- **Winning Line Highlights:** When a player wins, the exact 3-in-a-row winning cells highlight in glowing emerald green (`#10b981`).
- **Draw Highlights:** If the game ends in a tie, all cells highlight in warm amber (`#f59e0b`).

### 2. Game Modes
- **👥 Two Player Mode (PvP):** Play locally with a friend on the same computer taking turns.
- **🤖 Player vs Computer Mode (PvC):** Play against an intelligent computer opponent:
  - **Easy:** AI makes random playful moves.
  - **Medium:** AI plays a balanced mix of smart and casual moves.
  - **Hard (Unbeatable Minimax):** AI uses the classic **Minimax Algorithm** with immediate win/block checks — it never loses!

### 3. Scoreboard & Game Controls
- **Live Scoreboard:** Tracks Player X wins, Player O / Computer wins, and Draws across rounds.
- **🔄 Restart Round:** Clears the 3×3 board to play another round while preserving existing scores.
- **✨ Reset All:** Completely resets the board and wipes the scoreboard to start a fresh match series.
- **Smooth Mode Switching:** Toggle seamlessly between Two Players and Player vs AI anytime.

---

## 📁 Project Structure

```text
tic tac toe/
├── main.py          # Complete game source code (GUI & Game Logic)
├── test_game.py     # Automated unit tests for logic and UI (15 test suites)
├── requirements.txt # Dependency documentation (Standard Library)
└── README.md        # Comprehensive documentation and guide
```

---

## 🚀 How to Run the Game

### Prerequisites
- Python 3.8 or higher installed on your computer.
- `tkinter` (comes pre-bundled with standard Python installations on Windows and macOS).

### Running the Game

1. Open your terminal or Command Prompt (PowerShell).
2. Navigate to this project folder:
   ```bash
   cd "c:\Users\Kavya\OneDrive\Desktop\tic tac toe"
   ```
3. Run the application:
   ```bash
   python main.py
   ```
   *(Or on Windows if using Python launcher: `py main.py`)*

---

## 🧪 Running Automated Tests

To run the automated test suite verifying all 8 winning combinations, draw conditions, AI Minimax logic, and UI button bindings:

```bash
python test_game.py
```

All 15 automated test cases run and validate:
- ✅ All 8 winning rows, columns, and diagonals for Player X
- ✅ All 8 winning rows, columns, and diagonals for Player O
- ✅ In-progress game detection
- ✅ Draw condition detection
- ✅ Full board win vs draw distinction
- ✅ Immediate AI win completion
- ✅ Immediate AI opponent block
- ✅ Unbeatable Minimax AI simulation over multiple games
- ✅ GUI button click handling, cell locking, restart, and score resetting

---

## 🧠 Code Architecture & Logic Explained

The code in `main.py` is cleanly divided into two modular sections:

### 1. Pure Game Logic (Independent of GUI)
- **`WINNING_COMBINATIONS`**: A list of all 8 possible 3-in-a-row index tuples:
  - 3 Rows: `(0, 1, 2)`, `(3, 4, 5)`, `(6, 7, 8)`
  - 3 Columns: `(0, 3, 6)`, `(1, 4, 7)`, `(2, 5, 8)`
  - 2 Diagonals: `(0, 4, 8)`, `(2, 4, 6)`
- **`check_winner(board)`**: Inspects whether any winning combination has matching non-empty symbols. Returns `(winner, combo)` or `(None, None)`.
- **`check_draw(board)`**: Verifies whether all 9 cells are filled and no winner exists.
- **`get_available_moves(board)`**: Returns a list of indices representing unoccupied cells.
- **`minimax(board, depth, is_maximizing, ai_symbol, human_symbol)`**: A recursive decision-tree algorithm calculating optimal moves for the AI.
- **`get_best_ai_move(board, ...)`**: Selects the AI's move according to difficulty ('Easy', 'Medium', 'Hard').

### 2. Graphical User Interface (`ModernTicTacToe` Class)
- **`__init__(root)`**: Sets up window dimensions (480×700), centers it on screen, defines theme colors, and initializes board state.
- **`_create_board()`**: Builds the 3×3 grid with 9 custom-styled Tkinter buttons, binding `<Enter>` and `<Leave>` events for interactive hover animations.
- **`on_cell_clicked(index)`**: Validates if the selected cell is legal and active, marks the symbol, evaluates win/draw conditions, and schedules the AI turn if in PvC mode.
- **`execute_move(index, player)`**: Places the symbol on the board, colors the button, checks for win/draw, and alternates the active player.
- **`handle_game_win(...)` & `handle_game_draw(...)`**: Highlights winning cells with glowing colors, increments scores, and displays congratulatory messages.
- **`restart_round()` & `reset_all()`**: Manages clean board resets and score resets.

---

## 🎮 How to Play

1. **Select Game Mode**: Click **👥 Two Players** to take turns with someone locally, or **🤖 Player vs AI** to test your strategy against the computer.
2. **Make a Move**: Click on any available square on the 3×3 grid to place your **X**.
3. **Winning the Game**: Be the first to place 3 of your marks in a horizontal, vertical, or diagonal row.
4. **Play Again**: Click **🔄 Restart Round** to keep playing and rack up your score!

