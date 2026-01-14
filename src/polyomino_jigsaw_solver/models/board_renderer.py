from abc import ABC, abstractmethod

from .puzzle_board import PuzzleBoard


class BoardRenderer(ABC):
    """Interface for classes that can display the state of a board."""

    @abstractmethod
    def update(self, board: PuzzleBoard) -> None:
        """Update the display to reflect the current board state.

        Args:
            board: The PuzzleBoard object to display.
        """
        pass
