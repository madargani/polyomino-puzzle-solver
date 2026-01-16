<!--
SYNC IMPACT REPORT
==================
Version Change: template → 1.0.0 (initial ratification)

Modified Principles: None (initial constitution)
Added Sections:
  - Core Principles (5 new principles)
  - Code Quality Standards
  - Development Workflow

Templates Verified:
  ✅ .specify/templates/plan-template.md - Constitution Check section will reference new principles
  ✅ .specify/templates/spec-template.md - Requirements align with readability principles
  ✅ .specify/templates/tasks-template.md - Task structure supports modular implementation
  ✅ .specify/templates/checklist-template.md - Can be used for quality gate verification

Follow-up TODOs:
  - None - all placeholders filled
-->

# Polyomino Jigsaw Solver Constitution

## Core Principles

### I. Modularity & Decomposition

Code MUST be decomposed into smaller, focused units when complexity grows:

- **Function Size**: Functions should be under 50 lines. If longer, extract smaller helper functions
- **File Size**: Files should be under 300 lines. If larger, split into cohesive modules by responsibility
- **Single Responsibility**: Each function/class should have one clear purpose. If "and" is needed to describe it, it's doing too much
- **Module Cohesion**: Group related functionality together in the same file or module
- **Import Structure**: Minimize circular imports. Structure should be hierarchical, not interdependent

**Rationale**: Smaller units are easier to understand, test, debug, and maintain. Python's dynamic typing makes clear module boundaries even more critical.

### II. Readability First

Code MUST prioritize human readability over cleverness:

- **Explicit over Implicit**: Use clear, descriptive names. `calculate_piece_rotation` beats `calc_rot` or `c_r`
- **Docstrings**: All public functions and classes MUST have docstrings following PEP 257
- **Type Hints**: All function signatures MUST include type hints for parameters and return types
- **Self-Documenting**: Code should explain itself. Comments explain WHY, not WHAT
- **Pythonic Style**: Follow PEP 8 formatting and Python best practices (list comprehensions, context managers, etc.)

**Rationale**: Code is read more often than written. In a GUI project with complex state management, clarity prevents bugs and speeds up development.

### III. GUI Separation of Concerns

GUI code MUST separate presentation from business logic:

- **No Business Logic in UI Handlers**: Event handlers should only trigger operations, not implement algorithms
- **State Management**: Application state should be in separate models/classes, not embedded in UI widgets
- **Data Layer**: All data operations (file I/O, calculations) belong in separate modules
- **View Isolation**: UI code should be testable without a full GUI framework
- **Event-Driven**: Use signals/slots or observer patterns to decouple UI from logic

**Rationale**: GUI frameworks (Tkinter, PyQt, etc.) encourage tight coupling. Enforcing separation enables unit testing, reuse, and easier refactoring.

### IV. Code Quality Gates

All code changes MUST meet quality standards before merge:

- **Static Analysis**: Run linter (flake8, ruff, or similar) with no violations allowed
- **Type Checking**: Use mypy or similar type checker in strict mode
- **Formatting**: Apply auto-formatter (black or similar) with standard configuration
- **No Dead Code**: Remove commented-out code and unused imports before commit
- **Complexity Limits**: Use radon or similar to enforce cyclomatic complexity < 10 per function

**Rationale**: Automated quality gates prevent technical debt accumulation and maintain consistency across the codebase.

### V. Simplicity Over Complexity

Solutions MUST be as simple as possible, but no simpler:

- **YAGNI**: Don't implement features not needed now. Speculative complexity costs more now and later
- **No Premature Optimization**: Code clarity first. Optimize only after measuring performance problems
- **Avoid Over-Abstraction**: Don't create factories for single-instance objects. Direct instantiation is fine
- **Standard Library First**: Use Python stdlib before adding dependencies
- **Clear Code Over Clever Code**: A 5-line for loop is better than a 1-line nested comprehension that requires a comment

**Rationale**: Complexity is the enemy of maintainability. Python GUI projects already have framework complexity—adding unnecessary architectural layers compounds this.

## Code Quality Standards

### Naming Conventions

- **Modules/Files**: `lowercase_with_underscores.py` (e.g., `piece_rotator.py`, `grid_manager.py`)
- **Classes**: `CapWords` (e.g., `PuzzlePiece`, `GameBoard`)
- **Functions/Methods**: `lowercase_with_underscores` (e.g., `find_valid_positions`, `rotate_piece`)
- **Constants**: `UPPERCASE_WITH_UNDERSCORES` (e.g., `MAX_GRID_SIZE`, `DEFAULT_TIMEOUT`)
- **Private Members**: Single underscore prefix `_internal_method`

### Function Organization

- **Order Within File**: Constants → Classes → Helper Functions → Public Functions
- **Order Within Class**: `__init__` → Properties → Public Methods → Private Methods
- **Dependencies**: Import standard library → third-party → local modules, each group alphabetized

### Error Handling

- **Specific Exceptions**: Catch specific exceptions, never bare `except:` blocks
- **Exception Chaining**: Use `raise ... from ...` to preserve context when re-raising
- **Logging**: Use Python's `logging` module, never `print()` in production code
- **Fail Fast**: Validate inputs at function entry, raise `ValueError` or `TypeError` for invalid data

### Documentation Standards

```python
def solve_puzzle(pieces: List[PuzzlePiece], grid: GameBoard) -> bool:
    """
    Attempt to solve the puzzle by placing all pieces on the grid.

    Uses backtracking algorithm to explore valid piece placements.

    Args:
        pieces: List of puzzle pieces to place on the grid
        grid: The game board with dimensions and initial state

    Returns:
        True if puzzle was solved, False otherwise

    Raises:
        ValueError: If pieces list is empty or grid dimensions are invalid

    Examples:
        >>> pieces = [PuzzlePiece(...), PuzzlePiece(...)]
        >>> grid = GameBoard(width=5, height=5)
        >>> solve_puzzle(pieces, grid)
        True
    """
```

## Development Workflow

### Code Review Checklist

Before requesting review, verify:
- [ ] All functions have type hints
- [ ] All public functions/classes have docstrings
- [ ] Linter passes with zero violations
- [ ] Type checker passes with no errors
- [ ] Tests pass (if tests exist for this code)
- [ ] No commented-out code remains
- [ ] No unused imports
- [ ] No functions over 50 lines (or justification documented)
- [ ] No files over 300 lines (or split documented in PR)
- [ ] All imports are grouped correctly

### Refactoring Standards

When code complexity exceeds limits:
1. Extract helper functions from large functions
2. Split files by domain responsibility
3. Create dedicated modules for shared utilities
4. Document the refactoring strategy in the PR
5. Ensure tests still pass after refactor

### File Organization Suggestion

```
src/
├── models/           # Data structures and domain objects
│   ├── piece.py
│   ├── board.py
│   └── puzzle_state.py
├── logic/            # Business logic and algorithms
│   ├── solver.py
│   ├── validator.py
│   └── rotation.py
├── gui/              # UI components (framework-specific)
│   ├── main_window.py
│   ├── board_view.py
│   └── piece_widget.py
├── utils/            # Utility functions
│   ├── file_io.py
│   └── formatting.py
└── config.py         # Configuration and constants

tests/
├── unit/             # Isolated tests for individual functions
├── integration/      # Tests across module boundaries
└── fixtures/         # Test data
```

## Governance

### Amendment Process

1. **Proposal**: Document proposed changes with rationale
2. **Review**: Discuss with team/developer
3. **Approval**: Consensus required for principle changes
4. **Version Bump**: Increment constitution version (MAJOR/MINOR/PATCH as appropriate)
5. **Migration**: Update templates and existing code to comply with new principles
6. **Documentation**: Record change in sync impact report

### Compliance Enforcement

- **Constitution Check**: Implementation plans MUST verify compliance before Phase 0
- **Code Review**: All PRs must explicitly confirm compliance
- **Complexity Justification**: Any violation (e.g., 60-line function) must be documented in PR description
- **Quality Gates**: CI/CD pipeline should enforce linting, type checking, and formatting

### Versioning Policy

- **MAJOR** (X.0.0): Removing or fundamentally redefining principles
- **MINOR** (X.Y.0): Adding new principles or materially expanding existing ones
- **PATCH** (X.Y.Z): Clarifications, wording improvements, non-semantic changes

**Version**: 1.0.0 | **Ratified**: 2026-01-14 | **Last Amended**: 2026-01-14
