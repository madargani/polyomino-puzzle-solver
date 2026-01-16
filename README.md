# Polyomino Puzzle Solver

A Python GUI application for solving polyomino puzzles using backtracking algorithm with real-time visualization.

## Features

- **Puzzle Editor**: Draw polyomino pieces and configure board dimensions
- **Backtracking Solver**: Automatic puzzle solving with step-by-step visualization
- **Real-time Visualization**: Watch the solver place and remove pieces in real-time
- **Speed Control**: Adjustable visualization speed (slow, medium, fast, or custom)
- **Puzzle Management**: Save, load, export, and import puzzle configurations

## Quick Start

### Prerequisites

- Python 3.11 or higher
- uv (ultrafast Python package manager)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd polyomino-jigsaw-solver

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up the project with all dependencies
uv sync --all-groups
```

### Running the Application

```bash
# Launch the puzzle editor
uv run python -m src.main
```

## Project Structure

```
polyomino-jigsaw-solver/
├── src/
│   ├── models/             # Data structures
│   │   ├── piece.py       # PuzzlePiece class
│   │   ├── board.py       # GameBoard class
│   │   ├── puzzle_state.py # PuzzleState class
│   │   └── puzzle_config.py # PuzzleConfiguration class
│   ├── logic/             # Business logic
│   │   ├── solver.py     # Backtracking algorithm
│   │   ├── validator.py  # Validation logic
│   │   └── rotation.py   # Rotation/flip operations
│   ├── gui/              # User interface
│   │   ├── editor_window.py  # Puzzle editor
│   │   ├── board_view.py     # Grid editor
│   │   ├── piece_widget.py   # Piece interaction
│   │   └── viz_window.py     # Solver visualization
│   └── utils/            # Utilities
│       ├── file_io.py    # JSON I/O
│       └── formatting.py  # Formatting helpers
├── tests/               # Test suite
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── fixtures/        # Test data
├── specs/              # Feature specifications
│   └── 001-polyomino-puzzle-solver/
├── pyproject.toml       # Project configuration
├── uv.lock             # Dependency lockfile
└── README.md           # This file
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_piece.py -v
```

### Code Quality

```bash
# Run linter
uv run ruff check src/

# Auto-fix linting issues
uv run ruff check --fix src/

# Run formatter
uv run black src/

# Run type checker
uv run mypy src/ --strict

# Run all quality checks
uv run ruff check src/ && uv run mypy src/ --strict && uv run pytest tests/ -v
```

## Usage

### Creating a Puzzle

1. Launch the application
2. Set board dimensions using the width/height controls
3. Click "Add Piece" to create a new piece
4. Click on grid cells to define piece shape
5. Repeat for all pieces

### Solving a Puzzle

1. Configure your puzzle with pieces and board
2. Click "Solve" to open the visualization window
3. Adjust speed using the slider or presets
4. Watch the backtracking algorithm work
5. Click "Stop" to interrupt if needed

### Saving/Loading

- **Save**: Save current puzzle to library
- **Load**: Load a saved puzzle
- **Export**: Export puzzle to JSON file
- **Import**: Import puzzle from JSON file

## Dependencies

- **PySide6**: Qt6 Python bindings for GUI
- **pytest**: Testing framework
- **pytest-qt**: Qt testing utilities
- **pytest-mock**: Mocking utilities
- **uv**: Package manager

## License

MIT License
