# Data Model: Polyomino Puzzle Solver

**Feature**: Polyomino Puzzle Solver
**Date**: January 14, 2026

## Table of Contents

1. [Entity Overview](#entity-overview)
2. [Core Entities](#core-entities)
3. [Entity Relationships](#entity-relationships)
4. [Validation Rules](#validation-rules)
5. [State Management](#state-management)

---

## Entity Overview

| Entity | Description | Module | Key Attributes |
|--------|-------------|--------|----------------|
| **PuzzlePiece** | Represents a connected shape made of square grid cells | `models/piece.py` | shape, color, id |
| **GameBoard** | Represents the rectangular grid area where pieces must be placed | `models/board.py` | width, height, cells |
| **PuzzleState** | Represents the current state of the solving process | `models/puzzle_state.py` | board, placed_pieces, backtrack_history |
| **PuzzleConfiguration** | Represents a complete puzzle definition | `models/puzzle_config.py` | board_dimensions, pieces |

---

## Core Entities

### PuzzlePiece

**Purpose**: Represents a single polyomino piece with its shape, color, and unique identifier.

**Location**: `src/models/piece.py`

#### Attributes

| Attribute | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| `id` | `str` | Unique identifier for the piece | Required, format: `piece-{n}` or custom name |
| `shape` | `Set[Tuple[int, int]]` | Set of (row, col) coordinates defining the piece shape | Required, non-empty, coordinates relative to origin (0,0) |
| `color` | `str` | Display color for the piece | Required, hex format or named color |
| `area` | `int` | Number of cells in the piece (calculated) | Computed from `len(shape)`, ≥ 1 |

#### Methods

```python
class PuzzlePiece:
    def __init__(self, id: str, shape: Set[Tuple[int, int]], color: str) -> None:
        """Initialize a puzzle piece.

        Args:
            id: Unique identifier for the piece
            shape: Set of (row, col) coordinates defining the piece shape
            color: Display color (hex or named)

        Raises:
            ValueError: If shape is empty or not contiguous
        """

    def rotate(self, degrees: int = 90) -> 'PuzzlePiece':
        """Rotate the piece by specified degrees (90, 180, 270).

        Args:
            degrees: Rotation angle in degrees

        Returns:
            New PuzzlePiece with rotated shape

        Raises:
            ValueError: If degrees is not a multiple of 90
        """

    def flip(self, axis: str = 'horizontal') -> 'PuzzlePiece':
        """Flip (mirror) the piece along specified axis.

        Args:
            axis: 'horizontal' or 'vertical'

        Returns:
            New PuzzlePiece with flipped shape

        Raises:
            ValueError: If axis is not 'horizontal' or 'vertical'
        """

    def get_normalized_shape(self) -> Set[Tuple[int, int]]:
        """Return shape normalized to origin (min row/col = 0,0).

        Returns:
            Normalized shape coordinates
        """

    def get_rotations(self) -> List['PuzzlePiece']:
        """Generate all unique rotations of this piece.

        Returns:
            List of unique PuzzlePiece rotations (deduplicated)
        """

    def get_all_orientations(self) -> List['PuzzlePiece']:
        """Generate all unique rotations and flips of this piece.

        Returns:
            List of unique PuzzlePiece orientations (deduplicated)
        """

    def get_bounding_box(self) -> Tuple[int, int, int, int]:
        """Get bounding box (min_row, max_row, min_col, max_col).

        Returns:
            Tuple of bounding box coordinates
        """

    @property
    def width(self) -> int:
        """Get piece width (max_col - min_col + 1)."""

    @property
    def height(self) -> int:
        """Get piece height (max_row - min_row + 1)."""
```

#### Validation Rules

1. **Non-empty shape**: Shape must contain at least one cell
2. **Contiguous**: All cells must be connected (4-directional adjacency)
3. **Origin relative**: Shape should be normalized (min row/col = 0,0)
4. **Unique rotations**: `get_rotations()` must return deduplicated orientations
5. **Color format**: Color must be valid hex or named color (e.g., "#FF0000" or "red")

#### State Transitions

```
[Created Piece]
     │
     ├─ rotate(90) ──► [Rotated Piece] (new instance)
     │
     ├─ rotate(180) ─► [Rotated Piece] (new instance)
     │
     ├─ rotate(270) ─► [Rotated Piece] (new instance)
     │
     └─ flip('horizontal') ─► [Flipped Piece] (new instance)
```

**Note**: All transformation methods return new instances, preserving immutability.

---

### GameBoard

**Purpose**: Represents the rectangular grid area where pieces must be placed without overlap.

**Location**: `src/models/board.py`

#### Attributes

| Attribute | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| `width` | `int` | Number of columns in the board | Required, 1 ≤ width ≤ 50 |
| `height` | `int` | Number of rows in the board | Required, 1 ≤ height ≤ 50 |
| `cells` | `Dict[Tuple[int, int], Optional[str]]` | Grid cells mapping (row,col) → piece_id | Required, initialized to None |
| `total_area` | `int` | Total number of cells (calculated) | Computed from width × height |

#### Methods

```python
class GameBoard:
    def __init__(self, width: int, height: int) -> None:
        """Initialize a game board with specified dimensions.

        Args:
            width: Number of columns (1-50)
            height: Number of rows (1-50)

        Raises:
            ValueError: If dimensions are out of valid range
        """

    def can_place_piece(self, piece: PuzzlePiece, position: Tuple[int, int]) -> bool:
        """Check if a piece can be placed at the specified position.

        Args:
            piece: The puzzle piece to place
            position: (row, col) position to place piece origin

        Returns:
            True if piece fits without overlapping or going out of bounds
        """

    def place_piece(self, piece: PuzzlePiece, position: Tuple[int, int]) -> bool:
        """Place a piece at the specified position.

        Args:
            piece: The puzzle piece to place
            position: (row, col) position to place piece origin

        Returns:
            True if piece was placed successfully

        Raises:
            ValueError: If piece cannot be placed at position
        """

    def remove_piece(self, piece: PuzzlePiece, position: Tuple[int, int]) -> None:
        """Remove a piece from the board.

        Args:
            piece: The puzzle piece to remove
            position: (row, col) position where piece is placed

        Raises:
            ValueError: If piece is not found at position
        """

    def get_occupied_cells(self) -> Set[Tuple[int, int]]:
        """Get set of all occupied cell positions.

        Returns:
            Set of (row, col) tuples with pieces placed
        """

    def get_empty_cells(self) -> Set[Tuple[int, int]]:
        """Get set of all empty cell positions.

        Returns:
            Set of (row, col) tuples without pieces
        """

    def is_full(self) -> bool:
        """Check if board is completely filled.

        Returns:
            True if all cells are occupied
        """

    def is_empty(self) -> bool:
        """Check if board is completely empty.

        Returns:
            True if no pieces are placed
        """

    def get_piece_at(self, position: Tuple[int, int]) -> Optional[str]:
        """Get the piece ID at the specified position.

        Args:
            position: (row, col) position to query

        Returns:
            Piece ID if cell is occupied, None otherwise
        """

    def clear(self) -> None:
        """Clear all pieces from the board."""

    def copy(self) -> 'GameBoard':
        """Create a deep copy of the board.

        Returns:
            New GameBoard with identical state
        """

    @property
    def filled_area(self) -> int:
        """Get number of occupied cells."""

    @property
    def empty_area(self) -> int:
        """Get number of empty cells."""
```

#### Validation Rules

1. **Dimension limits**: 1 ≤ width ≤ 50, 1 ≤ height ≤ 50
2. **In-bounds placement**: All piece cells must be within board boundaries
3. **No overlap**: Piece cells cannot occupy already-filled cells
4. **Valid piece ID**: Piece must exist before placement/removal

#### State Transitions

```
[Empty Board]
     │
     ├─ place_piece(piece, pos) ──► [Piece Added]
     │                              │
     │                              ├─ place_piece(piece2, pos2) ──► [Multiple Pieces]
     │                              │
     │                              └─ remove_piece(piece, pos) ───► [Empty Board]
     │
     └─ clear() ──────────────────► [Empty Board]
```

---

### PuzzleState

**Purpose**: Represents the current state of the solving process, including board configuration, placed pieces, and backtrack history.

**Location**: `src/models/puzzle_state.py`

#### Attributes

| Attribute | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| `board` | `GameBoard` | Current board configuration | Required |
| `placed_pieces` | `List[Tuple[PuzzlePiece, Tuple[int, int]]]` | List of (piece, position) tuples | Required, ordered by placement |
| `available_pieces` | `List[PuzzlePiece]` | Pieces not yet placed | Required |
| `backtrack_history` | `List[Dict[str, Any]]` | History of solver operations | Required, append-only |
| `current_index` | `int` | Index of piece being placed | Required, 0 ≤ current_index < len(pieces) |

#### Methods

```python
class PuzzleState:
    def __init__(
        self,
        board: GameBoard,
        pieces: List[PuzzlePiece]
    ) -> None:
        """Initialize puzzle state with board and pieces.

        Args:
            board: The game board
            pieces: List of puzzle pieces to place
        """

    def place_piece(
        self,
        piece: PuzzlePiece,
        position: Tuple[int, int]
    ) -> None:
        """Place a piece and record in state.

        Args:
            piece: The puzzle piece to place
            position: (row, col) position to place piece

        Raises:
            ValueError: If piece cannot be placed
        """

    def remove_piece(self, position: Tuple[int, int]) -> None:
        """Remove a piece (backtrack).

        Args:
            position: (row, col) position to remove piece from
        """

    def record_operation(
        self,
        operation: str,
        piece_id: str,
        position: Tuple[int, int],
        orientation: Optional[PuzzlePiece] = None
    ) -> None:
        """Record a solver operation for history/visualization.

        Args:
            operation: 'place' or 'remove'
            piece_id: ID of the piece
            position: (row, col) position
            orientation: Piece orientation (for placement)
        """

    def get_last_operation(self) -> Optional[Dict[str, Any]]:
        """Get the most recent operation.

        Returns:
            Operation dict or None if no operations recorded
        """

    def is_solved(self) -> bool:
        """Check if puzzle is solved.

        Returns:
            True if all pieces are placed and board is full
        """

    def can_proceed(self) -> bool:
        """Check if solving can proceed.

        Returns:
            True if there are pieces left to place
        """

    def copy(self) -> 'PuzzleState':
        """Create a deep copy of the puzzle state.

        Returns:
            New PuzzleState with identical state
        """

    def get_statistics(self) -> Dict[str, Any]:
        """Get solver statistics.

        Returns:
            Dict with 'placements', 'removals', 'backtracks', etc.
        """
```

#### Validation Rules

1. **Piece exists**: Piece must be in available_pieces before placement
2. **Valid index**: current_index must track actual progress
3. **History consistency**: Backtrack history must match placed pieces
4. **State consistency**: board must reflect all placed pieces

#### State Transitions

```
[Initial State]
     │
     ├─ place_piece(piece, pos) ──► [Piece Placed]
     │                               │
     │                               ├─ place_piece(piece2, pos2) ──► [More Pieces]
     │                               │
     │                               └─ remove_piece(pos) ───────────► [Backtrack]
     │                                                            │
     │                                                            └─ place_piece(...) ──► [Retry]
     │
     └─ [is_solved() = True] ────────► [Solved State]
```

---

### PuzzleConfiguration

**Purpose**: Represents a complete puzzle definition containing board dimensions and the set of polyomino pieces.

**Location**: `src/models/puzzle_config.py`

#### Attributes

| Attribute | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| `name` | `str` | User-defined puzzle name | Required, unique within puzzles |
| `board_width` | `int` | Board width in cells | Required, 1 ≤ width ≤ 50 |
| `board_height` | `int` | Board height in cells | Required, 1 ≤ height ≤ 50 |
| `pieces` | `List[PuzzlePiece]` | List of puzzle pieces | Required, non-empty |
| `created_at` | `datetime` | Timestamp when configuration was created | Required |
| `modified_at` | `datetime` | Timestamp of last modification | Required |

#### Methods

```python
class PuzzleConfiguration:
    def __init__(
        self,
        name: str,
        board_width: int,
        board_height: int,
        pieces: List[PuzzlePiece]
    ) -> None:
        """Initialize a puzzle configuration.

        Args:
            name: User-defined puzzle name
            board_width: Board width in cells (1-50)
            board_height: Board height in cells (1-50)
            pieces: List of puzzle pieces

        Raises:
            ValueError: If constraints are violated
        """

    def validate(self) -> List[str]:
        """Validate the configuration.

        Returns:
            List of validation errors (empty if valid)
        """

    def add_piece(self, piece: PuzzlePiece) -> None:
        """Add a piece to the configuration.

        Args:
            piece: Puzzle piece to add

        Raises:
            ValueError: If piece is invalid or duplicate ID
        """

    def remove_piece(self, piece_id: str) -> None:
        """Remove a piece from the configuration.

        Args:
            piece_id: ID of the piece to remove

        Raises:
            ValueError: If piece_id not found
        """

    def get_board(self) -> GameBoard:
        """Create a GameBoard from configuration.

        Returns:
            New GameBoard instance
        """

    def get_piece_area(self) -> int:
        """Get total area of all pieces.

        Returns:
            Sum of all piece areas
        """

    def get_board_area(self) -> int:
        """Get total board area.

        Returns:
            board_width × board_height
        """

    def is_solvable_area(self) -> bool:
        """Check if piece area matches board area.

        Returns:
            True if total piece area equals board area
        """

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary for serialization.

        Returns:
            Dictionary representation
        """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PuzzleConfiguration':
        """Create configuration from dictionary.

        Args:
            data: Dictionary representation

        Returns:
            New PuzzleConfiguration instance

        Raises:
            ValueError: If data is invalid
        """

    def copy(self) -> 'PuzzleConfiguration':
        """Create a deep copy of the configuration.

        Returns:
            New PuzzleConfiguration with identical state
        """
```

#### Validation Rules

1. **Non-empty pieces**: At least one piece must be defined
2. **Unique piece IDs**: All piece IDs must be unique
3. **Valid dimensions**: Board dimensions must be 1-50
4. **Area check**: Total piece area must equal board area (optional warning, not error)
5. **Unique name**: Puzzle name must be unique within saved puzzles

#### State Transitions

```
[New Configuration]
     │
     ├─ add_piece(piece) ──► [Piece Added]
     │                       │
     │                       ├─ add_piece(piece2) ──► [More Pieces]
     │                       │
     │                       └─ remove_piece(id) ────► [Piece Removed]
     │
     └─ [save/load] ──────────────────────────────────► [Persisted Configuration]
```

---

## Entity Relationships

### Relationship Diagram

```
┌─────────────────────┐
│ PuzzleConfiguration │
│ - name              │◄────────────────┐
│ - board_width       │                 │
│ - board_height      │                 │
│ - pieces[]          │                 │
└─────────────────────┘                 │
         │ 1                           │
         │ has                         │ 1..*
         │                             │
         ▼                             │
┌─────────────────────┐   1..*         │
│    PuzzlePiece       │◄───────────────┘
│ - id                │
│ - shape             │
│ - color             │
└─────────────────────┘
         │
         │ 0..*
         │ placed in
         │
         ▼
┌─────────────────────┐
│      GameBoard      │◄────────────────┐
│ - width             │                 │
│ - height            │                 │
│ - cells{}           │                 │
└─────────────────────┘                 │
         │                             │
         │ tracked by                  │ 1
         │                             │
         ▼                             │
┌─────────────────────┐                 │
│    PuzzleState      │                 │
│ - board             │                 │
│ - placed_pieces[]   │                 │
│ - backtrack_history[]│                 │
└─────────────────────┘                 │
                                          │
         1..*                             │
         │ records                        │
         │                                │
         └────────────────────────────────┘
```

### Relationship Descriptions

| Relationship | Type | Description |
|--------------|------|-------------|
| **PuzzleConfiguration → PuzzlePiece** | 1..* | Configuration contains multiple pieces |
| **PuzzlePiece → GameBoard** | 0..* | Pieces can be placed on board (many orientations) |
| **GameBoard → PuzzleState** | 1 | Board is tracked by exactly one state during solving |
| **PuzzleState → Operation History** | 1 | State records its own backtrack history |

### Cascading Behaviors

- **Deleting PuzzleConfiguration**: Does not delete pieces (pieces may be reused)
- **Removing Piece from Configuration**: Invalidates any saved state referencing that piece
- **Clearing Board**: Does not affect PuzzleConfiguration (can rebuild board)
- **Copying PuzzleState**: Creates deep copy of board and placed pieces

---

## Validation Rules

### Cross-Entity Validation

1. **Piece Area vs Board Area**
   - **Rule**: Total piece area should equal board area for solvability
   - **Enforcement**: Warning in PuzzleConfiguration.validate(), not error
   - **Rationale**: User may want to define unsolvable puzzles for testing

2. **Piece Placement Validity**
   - **Rule**: All piece cells must be within board bounds
   - **Enforcement**: Error in GameBoard.place_piece()
   - **Rationale**: Prevents invalid state

3. **Unique Piece IDs**
   - **Rule**: All piece IDs in configuration must be unique
   - **Enforcement**: Error in PuzzleConfiguration.add_piece()
   - **Rationale**: Prevents confusion and state corruption

4. **Contiguous Piece Shapes**
   - **Rule**: All cells in a piece must be 4-connected
   - **Enforcement**: Error in PuzzlePiece.__init__()
   - **Rationale**: By definition, polyominoes are connected shapes

### Validation Flow

```python
# When creating a new puzzle
config = PuzzleConfiguration(name, width, height, pieces)
errors = config.validate()

if errors:
    # Display errors to user
    # e.g., "Piece area (25) does not match board area (24)"
    pass
else:
    # Proceed with solver
    board = config.get_board()
    state = PuzzleState(board, pieces)
```

### Error Hierarchy

1. **Critical Errors** (prevent operation):
   - Invalid dimensions
   - Empty piece shape
   - Non-contiguous piece
   - Duplicate piece IDs
   - Out-of-bounds placement

2. **Warnings** (allow operation but inform user):
   - Piece area ≠ board area
   - Very large puzzle (may take long to solve)
   - Many pieces (may be difficult to solve)

---

## State Management

### Immutable vs Mutable

**Immutable** (return new instances):
- `PuzzlePiece.rotate()`, `PuzzlePiece.flip()`
- `GameBoard.copy()`, `PuzzleState.copy()`, `PuzzleConfiguration.copy()`

**Mutable** (modify in place):
- `GameBoard.place_piece()`, `GameBoard.remove_piece()`, `GameBoard.clear()`
- `PuzzleState.place_piece()`, `PuzzleState.remove_piece()`
- `PuzzleConfiguration.add_piece()`, `PuzzleConfiguration.remove_piece()`

### Thread Safety Considerations

- **Read operations**: Thread-safe (no modification)
- **Write operations**: Not thread-safe, require external synchronization
- **Solver pattern**: Solver runs in separate thread, state is modified there
- **GUI updates**: Use Qt signals to communicate state changes to GUI thread

### Persistence Strategy

**JSON Serialization Format**:
```json
{
  "name": "My Puzzle",
  "board_width": 5,
  "board_height": 5,
  "pieces": [
    {
      "id": "piece-1",
      "shape": [[0, 0], [0, 1], [1, 1]],
      "color": "#FF0000"
    }
  ],
  "created_at": "2026-01-14T12:00:00Z",
  "modified_at": "2026-01-14T12:30:00Z"
}
```

**Deserialization**: Reconstruct objects from dictionaries using `from_dict()` methods

**File Locations**:
- Saved puzzles: `~/.polyomino-puzzles/saved/{name}.json`
- Exported puzzles: User-specified location

---

## Usage Examples

### Creating a Simple Puzzle

```python
from models.piece import PuzzlePiece
from models.board import GameBoard
from models.puzzle_config import PuzzleConfiguration

# Define pieces
piece1 = PuzzlePiece(
    id="tetromino-l",
    shape={(0, 0), (1, 0), (1, 1), (1, 2)},
    color="#FF0000"
)

piece2 = PuzzlePiece(
    id="tetromino-t",
    shape={(0, 0), (0, 1), (0, 2), (1, 1)},
    color="#0000FF"
)

# Create configuration
config = PuzzleConfiguration(
    name="Simple 4x4",
    board_width=4,
    board_height=4,
    pieces=[piece1, piece2]
)

# Validate
errors = config.validate()
if errors:
    print("Validation errors:", errors)
else:
    print("Configuration is valid!")
```

### Using the Solver

```python
from logic.solver import BacktrackingSolver
from models.puzzle_state import PuzzleState

# Create board and state
board = config.get_board()
state = PuzzleState(board, config.pieces)

# Run solver
solver = BacktrackingSolver(callback_delay=0.1)
result = solver.solve(config.pieces, board)

if result:
    print("Puzzle solved!")
    print(f"Placements: {len(state.placed_pieces)}")
else:
    print("No solution found")
```

### Working with Piece Orientations

```python
# Get all unique rotations
rotations = piece1.get_rotations()
print(f"Piece has {len(rotations)} unique rotations")

# Get all orientations (rotations + flips)
orientations = piece1.get_all_orientations()
print(f"Piece has {len(orientations)} unique orientations")

# Rotate a piece
rotated = piece1.rotate(90)
print(f"Rotated shape: {rotated.shape}")

# Flip a piece
flipped = piece1.flip('horizontal')
print(f"Flipped shape: {flipped.shape}")
```
