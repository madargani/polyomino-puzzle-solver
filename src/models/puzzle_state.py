"""PuzzleState class for representing the puzzle solving state."""

from __future__ import annotations

from typing import Any

from src.models.board import GameBoard
from src.models.piece import PuzzlePiece


class PuzzleState:
    """Represents the current state of the solving process.

    Attributes:
        board: Current board configuration
        placed_pieces: List of (piece, position) tuples in placement order
        available_pieces: Pieces not yet placed
        backtrack_history: History of solver operations
        current_index: Index of piece being placed
    """

    def __init__(
        self,
        board: GameBoard,
        pieces: list[PuzzlePiece],
    ) -> None:
        """Initialize puzzle state with board and pieces.

        Args:
            board: The game board
            pieces: List of puzzle pieces to place
        """
        self._board = board
        self._pieces = pieces
        self._placed_pieces: list[tuple[PuzzlePiece, tuple[int, int]]] = []
        self._available_pieces = list(pieces)
        self._backtrack_history: list[dict[str, Any]] = []
        self._current_index = 0

    @property
    def board(self) -> GameBoard:
        """Get the current board."""
        return self._board

    @property
    def placed_pieces(self) -> list[tuple[PuzzlePiece, tuple[int, int]]]:
        """Get list of placed pieces with their positions."""
        return self._placed_pieces.copy()

    @property
    def available_pieces(self) -> list[PuzzlePiece]:
        """Get list of pieces not yet placed."""
        return self._available_pieces.copy()

    @property
    def backtrack_history(self) -> list[dict[str, Any]]:
        """Get history of solver operations."""
        return self._backtrack_history.copy()

    @property
    def current_index(self) -> int:
        """Get current piece index."""
        return self._current_index

    def place_piece(
        self,
        piece: PuzzlePiece,
        position: tuple[int, int],
    ) -> bool:
        """Place a piece and record in state.

        Args:
            piece: The puzzle piece to place
            position: (row, col) position to place piece

        Returns:
            True if piece was placed successfully

        Raises:
            ValueError: If piece cannot be placed
        """
        if piece not in self._available_pieces:
            raise ValueError(f"Piece {piece.id} is not available")

        if not self._board.can_place_piece(piece.shape, position):
            raise ValueError(f"Cannot place piece {piece.id} at position {position}")

        # Place the piece on the board
        self._board.place_piece(piece.id, piece.shape, position)

        # Update state
        self._placed_pieces.append((piece, position))
        self._available_pieces.remove(piece)
        self._current_index += 1

        # Record operation
        self.record_operation("place", piece.id, position, piece)

        return True

    def remove_piece(self, position: tuple[int, int]) -> bool:
        """Remove a piece (backtrack).

        Args:
            position: (row, col) position to remove piece from

        Returns:
            True if piece was removed successfully

        Raises:
            ValueError: If no piece found at position
        """
        # Find the piece at this position
        piece_to_remove: PuzzlePiece | None = None
        piece_position: tuple[int, int] | None = None

        for piece, pos in self._placed_pieces:
            if pos == position:
                piece_to_remove = piece
                piece_position = pos
                break

        if piece_to_remove is None or piece_position is None:
            raise ValueError(f"No piece found at position {position}")

        # Remove from board
        self._board.remove_piece(
            piece_to_remove.id, piece_to_remove.shape, piece_position
        )

        # Update state
        self._placed_pieces.remove((piece_to_remove, piece_position))
        self._available_pieces.append(piece_to_remove)
        self._current_index -= 1

        # Record operation
        self.record_operation("remove", piece_to_remove.id, piece_position)

        return True

    def record_operation(
        self,
        operation: str,
        piece_id: str,
        position: tuple[int, int],
        orientation: PuzzlePiece | None = None,
    ) -> None:
        """Record a solver operation for history/visualization.

        Args:
            operation: 'place' or 'remove'
            piece_id: ID of the piece
            position: (row, col) position
            orientation: Piece orientation (for placement)
        """
        entry: dict[str, Any] = {
            "operation": operation,
            "piece_id": piece_id,
            "position": position,
        }
        if orientation is not None:
            entry["orientation"] = {
                "shape": list(orientation.shape),
                "width": orientation.width,
                "height": orientation.height,
            }
        self._backtrack_history.append(entry)

    def get_last_operation(self) -> dict[str, Any] | None:
        """Get the most recent operation.

        Returns:
            Operation dict or None if no operations recorded
        """
        if not self._backtrack_history:
            return None
        return self._backtrack_history[-1].copy()

    def is_solved(self) -> bool:
        """Check if puzzle is solved.

        Returns:
            True if all pieces are placed and board is full
        """
        return len(self._placed_pieces) == len(self._pieces) and self._board.is_full()

    def can_proceed(self) -> bool:
        """Check if solving can proceed.

        Returns:
            True if there are pieces left to place
        """
        return len(self._available_pieces) > 0

    def copy(self) -> PuzzleState:
        """Create a deep copy of the puzzle state.

        Returns:
            New PuzzleState with identical state
        """
        new_state = PuzzleState(self._board.copy(), list(self._pieces))
        new_state._placed_pieces = list(self._placed_pieces)
        new_state._available_pieces = list(self._available_pieces)
        new_state._backtrack_history = list(self._backtrack_history)
        new_state._current_index = self._current_index
        return new_state

    def get_statistics(self) -> dict[str, Any]:
        """Get solver statistics.

        Returns:
            Dict with 'placements', 'removals', 'backtracks', etc.
        """
        placements = sum(
            1 for op in self._backtrack_history if op["operation"] == "place"
        )
        removals = sum(
            1 for op in self._backtrack_history if op["operation"] == "remove"
        )
        backtracks = removals

        return {
            "placements": placements,
            "removals": removals,
            "backtracks": backtracks,
            "total_operations": len(self._backtrack_history),
            "pieces_placed": len(self._placed_pieces),
            "pieces_remaining": len(self._available_pieces),
        }

    def __repr__(self) -> str:
        """Get string representation."""
        return (
            f"PuzzleState(board={self._board}, "
            f"placed={len(self._placed_pieces)}/{len(self._pieces)})"
        )
