# Implementation Plan: Polyomino Puzzle Solver

**Branch**: `001-polyomino-puzzle-solver` | **Date**: January 14, 2026 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-polyomino-puzzle-solver/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a Python desktop GUI application for defining and visualizing polyomino puzzle solutions using **PySide6 (Qt6)**. Users can draw piece shapes on a grid editor, set board dimensions (up to 50x50 cells), and watch a backtracking algorithm solve puzzles in real-time with user-adjustable speed. The app supports saving/loading puzzles via JSON, uses unique colors for visual distinction, and enforces strict separation of concerns between GUI and business logic. Key technology decisions include:

- **GUI Framework**: PySide6 selected over Tkinter (performance) and Dear PyGui (community) for optimal 30fps+ visualization with QGraphicsScene handling 40,000+ items
- **Threading**: Thread-based solver with Qt signals for thread-safe UI updates (prevents freezing during computation)
- **Testing**: pytest + pytest-qt + pytest-mock for comprehensive unit and integration testing with GUI component mocking
- **Architecture**: Strict separation of models (data), logic (algorithms), gui (presentation), and utils (helpers) following constitution principles

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+
**Primary Dependencies**: PySide6 (Qt6), pytest, pytest-qt, pytest-mock
**Storage**: JSON files (local filesystem)
**Testing**: pytest + pytest-qt + pytest-mock
**Target Platform**: Desktop (Linux, Windows, macOS)
**Project Type**: single (desktop GUI application)
**Performance Goals**: 30fps minimum for visualization, <2 minutes solve time for typical puzzles
**Constraints**: 50x50 maximum board dimensions, offline-capable, user-adjustable visualization speed (100ms default delay)
**Scale/Scope**: Single-user desktop app, ~10-15 modules, 2 GUI windows (editor + visualization)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Modularity & Decomposition**: ✅ PASS - Will enforce <50 lines per function, <300 lines per file. File structure will follow domain responsibility (models/, logic/, gui/, utils/ as suggested in constitution)
- **Readability First**: ✅ PASS - All functions will have type hints and docstrings following PEP 257. Names will be descriptive (e.g., `calculate_piece_rotation` not `calc_rot`)
- **GUI Separation of Concerns**: ✅ PASS - Business logic (solver, validator, rotation) will be in separate modules from UI code. UI handlers will only trigger operations, not implement algorithms. State managed in separate model classes
- **Code Quality Gates**: ✅ PASS - Will configure flake8 for linting, mypy for type checking, and black for formatting. Will enforce cyclomatic complexity <10 per function using radon
- **Simplicity Over Complexity**: ✅ PASS - Will use standard library first. Only necessary dependencies (GUI framework + pytest). No premature optimization before measuring performance issues. No over-abstraction for single-instance objects

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── models/               # Data structures and domain objects
│   ├── piece.py          # PuzzlePiece class with shape, color, rotations
│   ├── board.py          # GameBoard class with dimensions, cell occupancy
│   └── puzzle_state.py   # Solution state with placed pieces, backtrack history
├── logic/                # Business logic and algorithms
│   ├── solver.py         # Backtracking solver algorithm
│   ├── validator.py      # Piece and puzzle validation logic
│   └── rotation.py       # Piece rotation and flip operations
├── gui/                  # UI components (framework-specific)
│   ├── editor_window.py  # Main editor window for defining puzzles
│   ├── board_view.py     # Grid-based board editor component
│   ├── piece_widget.py   # Piece drawing and interaction widget
│   └── viz_window.py     # Visualization window for solver animation
├── utils/                # Utility functions
│   ├── file_io.py        # JSON save/load/export/import operations
│   └── formatting.py     # Display formatting and color management
└── config.py             # Configuration and constants

tests/
├── unit/                 # Isolated tests for individual functions
│   ├── test_piece.py     # Tests for piece creation, rotation, validation
│   ├── test_board.py     # Tests for board operations, placement checks
│   ├── test_solver.py    # Tests for backtracking algorithm logic
│   └── test_rotation.py  # Tests for rotation/flip operations
├── integration/          # Tests across module boundaries
│   ├── test_puzzle_flow.py    # End-to-end puzzle setup and solve
│   └── test_file_io.py        # Save/load/export/import integration
└── fixtures/             # Test data
    └── sample_puzzles.json     # Example puzzle configurations
```

**Structure Decision**: Single desktop project following constitution's suggested structure. Separation of concerns enforced: models (data), logic (algorithms), gui (presentation), utils (helpers). Tests mirror source structure with unit and integration layers.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
