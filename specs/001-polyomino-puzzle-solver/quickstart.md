# Quickstart: Polyomino Puzzle Solver

**Feature**: Polyomino Puzzle Solver
**Date**: January 14, 2026

## Overview

This quickstart guide will help you get up and running with the Polyomino Puzzle Solver codebase. It covers setup, development workflow, and key concepts.

---

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git (for version control)

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd polyomino-jigsaw-solver
```

### 2. Create Virtual Environment

```bash
# Using venv (built-in)
python -m venv venv

# Activate on Linux/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install manually
pip install pyside6 pytest pytest-qt pytest-mock
```

### 4. Verify Installation

```bash
# Run tests to verify setup
pytest tests/ -v

# Run the application (once implemented)
python -m src.main
```

---

## Project Structure

```
polyomino-jigsaw-solver/
├── src/                    # Source code
│   ├── models/             # Data structures
│   │   ├── piece.py      # PuzzlePiece class
│   │   ├── board.py      # GameBoard class
│   │   └── puzzle_state.py # PuzzleState class
│   ├── logic/             # Business logic
│   │   ├── solver.py     # Backtracking algorithm
│   │   ├── validator.py  # Validation logic
│   │   └── rotation.py   # Rotation/flip operations
│   ├── gui/              # User interface
│   │   ├── editor_window.py  # Puzzle editor
│   │   ├── board_view.py     # Grid editor
│   │   ├── piece_widget.py   # Piece interaction
│   │   └── viz_window.py     # Solver visualization
│   ├── utils/            # Utilities
│   │   ├── file_io.py    # JSON I/O
│   │   └── formatting.py  # Formatting helpers
│   └── config.py         # Constants and config
├── tests/               # Test suite
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── fixtures/        # Test data
├── specs/              # Feature specifications
│   └── 001-polyomino-puzzle-solver/
└── requirements.txt     # Python dependencies
```

---

## Key Concepts

### Polyomino Pieces

A polyomino is a shape made by joining squares edge-to-edge. In this application:

- **Shape**: Defined as a set of (row, col) coordinates relative to origin (0,0)
- **Rotations**: Pieces can be rotated 90°, 180°, or 270°
- **Flips**: Pieces can be mirrored horizontally or vertically
- **Colors**: Each piece type has a unique color for visual distinction

```python
from models.piece import PuzzlePiece

# Create an L-tromino
piece = PuzzlePiece(
    id="l-tromino",
    shape={(0, 0), (1, 0), (1, 1)},  # Shape coordinates
    color="#FF0000"
)

# Rotate the piece
rotated = piece.rotate(90)

# Get all unique orientations
orientations = piece.get_all_orientations()
```

### Game Board

The board is a rectangular grid where pieces are placed:

- **Dimensions**: 1-50 cells in width and height
- **Cells**: Each cell can hold at most one piece
- **Placement**: Pieces must fit entirely within the board
- **Overlap**: Piece cells cannot occupy already-filled cells

```python
from models.board import GameBoard

# Create a 5x5 board
board = GameBoard(width=5, height=5)

# Check if a piece can be placed
can_place = board.can_place_piece(piece, (2, 2))

# Place the piece
if can_place:
    board.place_piece(piece, (2, 2))
```

### Backtracking Solver

The solver uses backtracking to find valid placements:

1. **Recursive**: Try placing pieces one by one
2. **Backtrack**: If dead end, remove last piece and try alternative
3. **Orientation**: Try all rotations/flips of each piece
4. **Visualization**: Emit signals to show progress in real-time

```python
from logic.solver import BacktrackingSolver
from models.puzzle_state import PuzzleState

# Create state
state = PuzzleState(board, pieces)

# Run solver with visualization delay
solver = BacktrackingSolver(callback_delay=0.1)
result = solver.solve(pieces, board)

if result:
    print("Solution found!")
else:
    print("No solution exists")
```

---

## Development Workflow

### Code Style

We follow strict code quality standards:

- **Type hints**: All function signatures must include types
- **Docstrings**: All public functions/classes must have docstrings (PEP 257)
- **Naming**: Follow PEP 8 conventions
  - Classes: `CapWords`
  - Functions/variables: `lowercase_with_underscores`
  - Constants: `UPPERCASE_WITH_UNDERSCORES`

### Code Quality Gates

Before committing code:

```bash
# Run linter
flake8 src/

# Run type checker
mypy src/ --strict

# Run formatter
black src/

# Run tests
pytest tests/ -v

# Check code complexity
radon cc src/ -a -nb
```

### File Size Limits

- **Functions**: Under 50 lines
- **Files**: Under 300 lines

If limits are exceeded, extract helper functions or split modules.

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/ -v

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_piece.py -v
```

### Writing Tests

Unit tests test individual functions without GUI dependencies:

```python
# tests/unit/test_piece.py
import pytest
from models.piece import PuzzlePiece

def test_piece_rotation():
    """Test piece rotates correctly."""
    piece = PuzzlePiece(
        id="test",
        shape={(0, 0), (0, 1)},
        color="red"
    )

    rotated = piece.rotate(90)

    # Verify rotation
    expected_shape = {(0, 0), (1, 0)}
    assert rotated.shape == expected_shape

def test_piece_contiguity_validation():
    """Test non-contiguous shapes are rejected."""
    with pytest.raises(ValueError):
        PuzzlePiece(
            id="invalid",
            shape={(0, 0), (0, 2)},  # Not connected
            color="red"
        )
```

Integration tests test multiple modules together:

```python
# tests/integration/test_puzzle_flow.py
from models.piece import PuzzlePiece
from models.board import GameBoard
from logic.solver import BacktrackingSolver

def test_simple_puzzle_solve():
    """Test end-to-end puzzle solving."""
    pieces = [
        PuzzlePiece(id="p1", shape={(0, 0), (0, 1)}, color="red"),
        PuzzlePiece(id="p2", shape={(0, 0), (1, 0)}, color="blue"),
    ]
    board = GameBoard(width=2, height=2)

    solver = BacktrackingSolver(callback_delay=0)
    result = solver.solve(pieces, board)

    assert result is True
    assert board.is_full()
```

---

## Common Tasks

### Adding a New Piece Type

```python
from models.piece import PuzzlePiece

# Define shape coordinates (relative to origin)
shape = {
    (0, 0), (0, 1), (0, 2),  # Horizontal bar
}

# Create piece
piece = PuzzlePiece(
    id="tetromino-i",
    shape=shape,
    color="#00FF00"
)

# Add to configuration
config.add_piece(piece)
```

### Creating a Puzzle Configuration

```python
from models.puzzle_config import PuzzleConfiguration

config = PuzzleConfiguration(
    name="My Puzzle",
    board_width=5,
    board_height=5,
    pieces=[piece1, piece2, piece3]
)

# Validate
errors = config.validate()
if errors:
    print("Errors:", errors)
```

### Saving/Loading Puzzles

```python
from utils.file_io import save_puzzle, load_puzzle
from pathlib import Path

# Save puzzle
save_puzzle(
    config.pieces,
    config.get_board(),
    Path("my_puzzle.json")
)

# Load puzzle
pieces, board = load_puzzle(Path("my_puzzle.json"))
```

### Running the GUI

```python
from gui.editor_window import EditorWindow
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
window = EditorWindow()
window.show()
sys.exit(app.exec())
```

---

## Troubleshooting

### Import Errors

**Problem**: `ImportError: No module named 'PySide6'`

**Solution**:
```bash
pip install pyside6
```

### Linter Errors

**Problem**: `flake8` reports missing type hints

**Solution**: Add type hints to all function signatures:
```python
# Before
def solve(pieces, board):
    pass

# After
def solve(pieces: List[PuzzlePiece], board: GameBoard) -> bool:
    pass
```

### Test Failures

**Problem**: Tests fail with "Display not found"

**Solution**: Use Xvfb on headless systems:
```bash
xvfb-run pytest
```

### GUI Not Responsive

**Problem**: GUI freezes during solving

**Solution**: Ensure solver runs in background thread:
```python
import threading

solver_thread = threading.Thread(
    target=solver.solve,
    args=(pieces, board)
)
solver_thread.start()
```

---

## Getting Help

### Documentation

- **Feature Specification**: See `specs/001-polyomino-puzzle-solver/spec.md`
- **Data Model**: See `specs/001-polyomino-puzzle-solver/data-model.md`
- **Research**: See `specs/001-polyomino-puzzle-solver/research.md`

### Resources

- **PySide6 Documentation**: https://doc.qt.io/qtforpython-6/
- **Python Documentation**: https://docs.python.org/3/
- **pytest Documentation**: https://docs.pytest.org/

### Contributing

1. Read the constitution: `.specify/memory/constitution.md`
2. Follow code style guidelines
3. Write tests for new features
4. Run all tests before committing
5. Ensure linter/type checker pass

---

## Next Steps

1. **Explore the codebase**: Read through `src/` to understand structure
2. **Run tests**: `pytest tests/ -v` to verify everything works
3. **Try the examples**: See `Usage Examples` in `data-model.md`
4. **Read the spec**: Understand user requirements in `spec.md`
5. **Start contributing**: Check `specs/001-polyomino-puzzle-solver/tasks.md` for implementation tasks

Happy coding! 🧩
