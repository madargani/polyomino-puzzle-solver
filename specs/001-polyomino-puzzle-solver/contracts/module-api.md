# Module API Contracts

**Feature**: Polyomino Puzzle Solver  
**Date**: January 16, 2026

This document defines the public API contracts between modules.

---

## Models Module (`src/models/`)

### `piece.py` - PuzzlePiece

```python
class PuzzlePiece:
    """Represents a polyomino puzzle piece with shape, color, and transformations."""
    
    def __init__(self, id: str, shape: Set[Tuple[int, int]], color: str) -> None:
        """
        Initialize a puzzle piece.
        
        Args:
            id: Unique identifier for the piece
            shape: Set of (row, col) coordinates defining the piece shape
            color: Display color (hex or named)
        
        Raises:
            ValueError: If shape is empty, not contiguous, or color is invalid
        """
    
    @property
    def id(self) -> str:
        """Get the piece identifier."""
    
    @property
    def shape(self) -> Set[Tuple[int, int]]:
        """Get the piece shape coordinates."""
    
    @property
    def color(self) -> str:
        """Get the piece color."""
    
    @property
    def area(self) -> int:
        """Get the number of cells in the piece."""
    
    def rotate(self, degrees: int = 90) -> 'PuzzlePiece':
        """
        Rotate the piece by specified degrees.
        
        Args:
            degrees: Rotation angle in degrees (90, 180, 270)
        
        Returns:
            New PuzzlePiece with rotated shape
        
        Raises:
            ValueError: If degrees is not a multiple of 90
        """
    
    def flip(self, axis: str = 'horizontal') -> 'PuzzlePiece':
        """
        Flip (mirror) the piece along specified axis.
        
        Args:
            axis: 'horizontal' or 'vertical'
        
        Returns:
            New PuzzlePiece with flipped shape
        
        Raises:
            ValueError: If axis is not 'horizontal' or 'vertical'
        """
    
    def get_normalized_shape(self) -> Set[Tuple[int, int]]:
        """Return shape normalized to origin (min row/col = 0,0)."""
    
    def get_rotations(self) -> List['PuzzlePiece']:
        """Generate all unique rotations of this piece."""
    
    def get_all_orientations(self) -> List['PuzzlePiece']:
        """Generate all unique rotations and flips of this piece."""
    
    def get_bounding_box(self) -> Tuple[int, int, int, int]:
        """Get bounding box (min_row, max_row, min_col, max_col)."""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert piece to dictionary for serialization."""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PuzzlePiece':
        """Create piece from dictionary."""
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on shape and color."""
    
    def __hash__(self) -> int:
        """Enable use in sets and as dict keys."""
```

### `board.py` - GameBoard

```python
class GameBoard:
    """Represents the rectangular grid where pieces are placed."""
    
    def __init__(self, width: int, height: int) -> None:
        """
        Initialize a game board.
        
        Args:
            width: Number of columns (1-50)
            height: Number of rows (1-50)
        
        Raises:
            ValueError: If dimensions are out of valid range
        """
    
    @property
    def width(self) -> int:
        """Get board width in cells."""
    
    @property
    def height(self) -> int:
        """Get board height in cells."""
    
    @property
    def total_area(self) -> int:
        """Get total number of cells."""
    
    @property
    def filled_area(self) -> int:
        """Get number of occupied cells."""
    
    @property
    def empty_area(self) -> int:
        """Get number of empty cells."""
    
    def can_place_piece(self, piece: PuzzlePiece, position: Tuple[int, int]) -> bool:
        """
        Check if a piece can be placed at the specified position.
        
        Args:
            piece: The puzzle piece to place
            position: (row, col) position to place piece origin
        
        Returns:
            True if piece fits without overlapping or going out of bounds
        """
    
    def place_piece(self, piece: PuzzlePiece, position: Tuple[int, int]) -> bool:
        """
        Place a piece at the specified position.
        
        Args:
            piece: The puzzle piece to place
            position: (row, col) position to place piece origin
        
        Returns:
            True if piece was placed successfully
        
        Raises:
            ValueError: If piece cannot be placed at position
        """
    
    def remove_piece(self, position: Tuple[int, int]) -> Optional[PuzzlePiece]:
        """
        Remove a piece from the board.
        
        Args:
            position: (row, col) position where piece is placed
        
        Returns:
            The removed piece, or None if no piece at position
        
        Raises:
            ValueError: If position is out of bounds
        """
    
    def get_occupied_cells(self) -> Set[Tuple[int, int]]:
        """Get set of all occupied cell positions."""
    
    def get_empty_cells(self) -> Set[Tuple[int, int]]:
        """Get set of all empty cell positions."""
    
    def is_full(self) -> bool:
        """Check if board is completely filled."""
    
    def is_empty(self) -> bool:
        """Check if board is completely empty."""
    
    def get_piece_at(self, position: Tuple[int, int]) -> Optional[str]:
        """
        Get the piece ID at the specified position.
        
        Args:
            position: (row, col) position to query
        
        Returns:
            Piece ID if cell is occupied, None otherwise
        """
    
    def clear(self) -> None:
        """Clear all pieces from the board."""
    
    def copy(self) -> 'GameBoard':
        """Create a deep copy of the board."""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert board to dictionary for serialization."""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameBoard':
        """Create board from dictionary."""
```

### `puzzle_state.py` - PuzzleState

```python
class PuzzleState:
    """Represents the current state of the solving process."""
    
    def __init__(self, board: GameBoard, pieces: List[PuzzlePiece]) -> None:
        """
        Initialize puzzle state.
        
        Args:
            board: The game board
            pieces: List of puzzle pieces to place
        """
    
    @property
    def board(self) -> GameBoard:
        """Get the current board state."""
    
    @property
    def placed_pieces(self) -> List[Tuple[PuzzlePiece, Tuple[int, int]]]:
        """Get list of placed (piece, position) tuples."""
    
    @property
    def available_pieces(self) -> List[PuzzlePiece]:
        """Get pieces not yet placed."""
    
    @property
    def backtrack_history(self) -> List[Dict[str, Any]]:
        """Get history of solver operations."""
    
    @property
    def current_index(self) -> int:
        """Get index of piece being placed."""
    
    def place_piece(self, piece: PuzzlePiece, position: Tuple[int, int]) -> None:
        """
        Place a piece and record in state.
        
        Args:
            piece: The puzzle piece to place
            position: (row, col) position to place piece
        
        Raises:
            ValueError: If piece cannot be placed
        """
    
    def remove_piece(self, position: Tuple[int, int]) -> Optional[PuzzlePiece]:
        """
        Remove a piece (backtrack).
        
        Args:
            position: (row, col) position to remove piece from
        
        Returns:
            The removed piece, or None if no piece at position
        """
    
    def record_operation(
        self,
        operation: str,
        piece_id: str,
        position: Tuple[int, int],
        orientation: Optional[PuzzlePiece] = None
    ) -> None:
        """
        Record a solver operation for history/visualization.
        
        Args:
            operation: 'place' or 'remove'
            piece_id: ID of the piece
            position: (row, col) position
            orientation: Piece orientation (for placement)
        """
    
    def get_last_operation(self) -> Optional[Dict[str, Any]]:
        """Get the most recent operation."""
    
    def is_solved(self) -> bool:
        """Check if puzzle is solved."""
    
    def can_proceed(self) -> bool:
        """Check if solving can proceed."""
    
    def copy(self) -> 'PuzzleState':
        """Create a deep copy of the puzzle state."""
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get solver statistics."""
```

### `puzzle_config.py` - PuzzleConfiguration

```python
class PuzzleConfiguration:
    """Represents a complete puzzle definition."""
    
    def __init__(
        self,
        name: str,
        board_width: int,
        board_height: int,
        pieces: List[PuzzlePiece]
    ) -> None:
        """
        Initialize a puzzle configuration.
        
        Args:
            name: User-defined puzzle name
            board_width: Board width in cells (1-50)
            board_height: Board height in cells (1-50)
            pieces: List of puzzle pieces
        
        Raises:
            ValueError: If constraints are violated
        """
    
    @property
    def name(self) -> str:
        """Get the puzzle name."""
    
    @property
    def board_width(self) -> int:
        """Get board width."""
    
    @property
    def board_height(self) -> int:
        """Get board height."""
    
    @property
    def pieces(self) -> List[PuzzlePiece]:
        """Get the list of pieces."""
    
    def validate(self) -> List[str]:
        """
        Validate the configuration.
        
        Returns:
            List of validation errors (empty if valid)
        """
    
    def add_piece(self, piece: PuzzlePiece) -> None:
        """
        Add a piece to the configuration.
        
        Args:
            piece: Puzzle piece to add
        
        Raises:
            ValueError: If piece is invalid or duplicate ID
        """
    
    def remove_piece(self, piece_id: str) -> None:
        """
        Remove a piece from the configuration.
        
        Args:
            piece_id: ID of the piece to remove
        
        Raises:
            ValueError: If piece_id not found
        """
    
    def get_piece(self, piece_id: str) -> Optional[PuzzlePiece]:
        """
        Get a piece by ID.
        
        Args:
            piece_id: ID of the piece to retrieve
        
        Returns:
            The piece, or None if not found
        """
    
    def get_board(self) -> GameBoard:
        """Create a GameBoard from configuration."""
    
    def get_piece_area(self) -> int:
        """Get total area of all pieces."""
    
    def get_board_area(self) -> int:
        """Get total board area."""
    
    def is_solvable_area(self) -> bool:
        """Check if piece area matches board area."""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PuzzleConfiguration':
        """Create configuration from dictionary."""
    
    def copy(self) -> 'PuzzleConfiguration':
        """Create a deep copy."""
```

---

## Logic Module (`src/logic/`)

### `solver.py` - BacktrackingSolver

```python
class BacktrackingSolver:
    """Backtracking algorithm for solving polyomino puzzles."""
    
    def __init__(self, callback_delay: float = 0.1) -> None:
        """
        Initialize the solver.
        
        Args:
            callback_delay: Delay in seconds between visualization updates
        """
    
    @property
    def callback_delay(self) -> float:
        """Get the current visualization delay."""
    
    @callback_delay.setter
    def callback_delay(self, value: float) -> None:
        """Set the visualization delay."""
    
    @property
    def should_stop(self) -> bool:
        """Check if solver should stop."""
    
    def solve(
        self,
        pieces: List[PuzzlePiece],
        board: GameBoard
    ) -> bool:
        """
        Solve the puzzle using backtracking.
        
        Args:
            pieces: List of puzzle pieces to place
            board: The game board
        
        Returns:
            True if solution found, False otherwise
        """
    
    def stop(self) -> None:
        """Signal the solver to stop gracefully."""
    
    def reset(self) -> None:
        """Reset solver state."""
```

### `validator.py` - PuzzleValidator

```python
class PuzzleValidator:
    """Validates puzzle configurations and states."""
    
    @staticmethod
    def validate_piece_shape(shape: Set[Tuple[int, int]]) -> List[str]:
        """
        Validate a piece shape.
        
        Args:
            shape: Set of (row, col) coordinates
        
        Returns:
            List of validation errors (empty if valid)
        """
    
    @staticmethod
    def validate_board_dimensions(width: int, height: int) -> List[str]:
        """
        Validate board dimensions.
        
        Args:
            width: Board width
            height: Board height
        
        Returns:
            List of validation errors (empty if valid)
        """
    
    @staticmethod
    def check_area_match(
        pieces: List[PuzzlePiece],
        board: GameBoard
    ) -> List[str]:
        """
        Check if total piece area matches board area.
        
        Args:
            pieces: List of puzzle pieces
            board: The game board
        
        Returns:
            List of warnings (empty if area matches)
        """
    
    @staticmethod
    def validate_piece_placement(
        piece: PuzzlePiece,
        board: GameBoard,
        position: Tuple[int, int]
    ) -> List[str]:
        """
        Validate if piece can be placed at position.
        
        Args:
            piece: The puzzle piece
            board: The game board
            position: (row, col) position
        
        Returns:
            List of validation errors (empty if valid)
        """
```

### `rotation.py` - RotationOperations

```python
class RotationOperations:
    """Rotation and flip operations for puzzle pieces."""
    
    @staticmethod
    def rotate(
        shape: Set[Tuple[int, int]],
        degrees: int
    ) -> Set[Tuple[int, int]]:
        """
        Rotate a shape by specified degrees.
        
        Args:
            shape: Set of (row, col) coordinates
            degrees: Rotation angle (90, 180, 270)
        
        Returns:
            Rotated shape coordinates
        
        Raises:
            ValueError: If degrees is not a multiple of 90
        """
    
    @staticmethod
    def flip(
        shape: Set[Tuple[int, int]],
        axis: str
    ) -> Set[Tuple[int, int]]:
        """
        Flip a shape along specified axis.
        
        Args:
            shape: Set of (row, col) coordinates
            axis: 'horizontal' or 'vertical'
        
        Returns:
            Flipped shape coordinates
        
        Raises:
            ValueError: If axis is not 'horizontal' or 'vertical'
        """
    
    @staticmethod
    def normalize_shape(shape: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """
        Normalize shape to origin (min row/col = 0,0).
        
        Args:
            shape: Set of (row, col) coordinates
        
        Returns:
            Normalized shape coordinates
        """
    
    @staticmethod
    def get_all_orientations(
        shape: Set[Tuple[int, int]]
    ) -> List[Set[Tuple[int, int]]]:
        """
        Generate all unique orientations of a shape.
        
        Args:
            shape: Set of (row, col) coordinates
        
        Returns:
            List of unique orientation shapes
        """
```

---

## Utils Module (`src/utils/`)

### `file_io.py` - FileOperations

```python
def save_puzzle(
    config: PuzzleConfiguration,
    filepath: Path
) -> None:
    """
    Save puzzle configuration to JSON file.
    
    Args:
        config: Puzzle configuration to save
        filepath: Output file path
    
    Raises:
        IOError: If file cannot be written
    """


def load_puzzle(filepath: Path) -> PuzzleConfiguration:
    """
    Load puzzle configuration from JSON file.
    
    Args:
        filepath: Input file path
    
    Returns:
        Loaded PuzzleConfiguration
    
    Raises:
        IOError: If file cannot be read
        ValueError: If file contains invalid data
    """


def export_puzzle(
    config: PuzzleConfiguration,
    filepath: Path
) -> None:
    """
    Export puzzle configuration for sharing.
    
    Args:
        config: Puzzle configuration to export
        filepath: Output file path
    
    Raises:
        IOError: If file cannot be written
    """


def import_puzzle(filepath: Path) -> PuzzleConfiguration:
    """
    Import puzzle configuration from file.
    
    Args:
        filepath: Input file path
    
    Returns:
        Imported PuzzleConfiguration
    
    Raises:
        IOError: If file cannot be read
        ValueError: If file contains invalid data
    """
```

---

## GUI Module (`src/gui/`)

### `editor_window.py` - EditorWindow

```python
class EditorWindow(QMainWindow):
    """Main editor window for puzzle configuration."""
    
    def __init__(self) -> None:
        """Initialize the editor window."""
    
    def get_puzzle_configuration(self) -> PuzzleConfiguration:
        """
        Get the current puzzle configuration.
        
        Returns:
            Current PuzzleConfiguration
        """
    
    def set_puzzle_configuration(self, config: PuzzleConfiguration) -> None:
        """
        Set the puzzle configuration.
        
        Args:
            config: PuzzleConfiguration to display
        """
    
    def clear(self) -> None:
        """Clear all puzzle configuration."""
    
    def add_piece(self) -> PuzzlePiece:
        """
        Add a new piece to the configuration.
        
        Returns:
            The created PuzzlePiece
        """
    
    def remove_piece(self, piece_id: str) -> None:
        """
        Remove a piece from the configuration.
        
        Args:
            piece_id: ID of the piece to remove
        """
```

### `viz_window.py` - VizWindow

```python
class VizWindow(QMainWindow):
    """Visualization window for solver progress."""
    
    def __init__(self, config: PuzzleConfiguration) -> None:
        """
        Initialize the visualization window.
        
        Args:
            config: Puzzle configuration to solve
        """
    
    def start_solver(self) -> None:
        """Start the solver with current configuration."""
    
    def stop_solver(self) -> None:
        """Stop the currently running solver."""
    
    def set_speed(self, delay_ms: float) -> None:
        """
        Set the visualization speed.
        
        Args:
            delay_ms: Delay between updates in milliseconds
        """
    
    def is_solving(self) -> bool:
        """Check if solver is currently running."""
```

### `board_view.py` - BoardView

```python
class BoardView(QWidget):
    """Widget for displaying and interacting with the game board."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Initialize the board view."""
    
    def set_board(self, board: GameBoard) -> None:
        """
        Set the board to display.
        
        Args:
            board: GameBoard to display
        """
    
    def set_pieces(self, pieces: List[PuzzlePiece]) -> None:
        """
        Set the pieces to display.
        
        Args:
            pieces: List of PuzzlePiece objects
        """
    
    def highlight_cells(
        self,
        cells: Set[Tuple[int, int]],
        color: str
    ) -> None:
        """
        Highlight specific cells.
        
        Args:
            cells: Set of (row, col) positions
            color: Highlight color
        """
    
    def clear_highlights(self) -> None:
        """Clear all cell highlights."""
    
    def set_edit_mode(self, enabled: bool, piece: Optional[PuzzlePiece] = None) -> None:
        """
        Enable or disable edit mode.
        
        Args:
            enabled: Whether edit mode is enabled
            piece: Piece being edited (if enabled)
        """
```

---

## Cross-Module Dependencies

### Models → None (Pure data layer)
- No dependencies on logic, gui, or utils
- Can be imported by any module

### Logic → Models
- Imports from `models.piece`, `models.board`, `models.puzzle_state`
- No dependencies on gui or utils

### Utils → Models
- Imports from `models.puzzle_config`
- No dependencies on logic or gui

### GUI → Models, Logic, Utils
- Imports from all lower layers
- NO circular imports allowed
- Use dependency injection for testability

### Dependency Graph
```
models/
    ↑
    | (imports)
logic/  utils/
    ↑       ↑
    | (imports)
    gui/
```
