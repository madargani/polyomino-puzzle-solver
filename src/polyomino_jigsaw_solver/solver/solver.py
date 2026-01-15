from typing import Dict, Optional

from polyomino_jigsaw_solver.models.board_renderer import BoardRenderer
from polyomino_jigsaw_solver.models.puzzle_board import PuzzleBoard
from polyomino_jigsaw_solver.models.puzzle_piece import PuzzlePiece


def solve_puzzle(
    board: PuzzleBoard,
    pieces: Dict[PuzzlePiece, int],
    renderer: Optional[BoardRenderer] = None,
) -> Optional[PuzzleBoard]:
    """Solve a polyomino puzzle using backtracking.

    Args:
        board: The puzzle board to solve
        pieces: Dictionary mapping puzzle pieces to their counts
        renderer: Optional renderer to visualize the solving process

    Returns:
        Solved PuzzleBoard if solution found, None otherwise
    """
    if renderer:
        renderer.update(board)

    total_cells_needed = sum(
        len(next(iter(piece.transformations))) * count
        for piece, count in pieces.items()
    )
    total_cells_available = board.width * board.height - len(board.filled_cells)

    if total_cells_needed > total_cells_available:
        return None

    empty_cell = _find_first_empty_cell(board)
    if not empty_cell:
        if all(count == 0 for count in pieces.values()):
            return board
        return None

    row, col = empty_cell

    for piece in list(pieces.keys()):
        if pieces[piece] == 0:
            continue

        for transformation in piece.transformations:
            if board.check_piece(list(transformation), row, col):
                board.insert_piece(list(transformation), row, col)
                pieces[piece] -= 1

                if renderer:
                    renderer.update(board)

                result = solve_puzzle(board, pieces, renderer)

                if result is not None:
                    return result

                board.remove_piece(list(transformation), row, col)
                pieces[piece] += 1

                if renderer:
                    renderer.update(board)

    return None


def _find_first_empty_cell(board: PuzzleBoard) -> Optional[tuple[int, int]]:
    """Find the first empty cell scanning left to right, then top to bottom."""
    for row in range(board.height):
        for col in range(board.width):
            if board.is_cell_empty(row, col):
                return (row, col)
    return None
