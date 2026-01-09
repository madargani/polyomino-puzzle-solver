import pytest

from polyomino_jigsaw_solver.models.puzzle_board import (
    PiecePlacementError,
    PieceRemovalError,
    PuzzleBoard,
)


class TestPuzzleBoardInitialization:
    def test_board_with_default_filled_cells(self):
        board = PuzzleBoard(width=5, height=5)
        assert board.width == 5
        assert board.height == 5
        assert len(board.filled_cells) == 0

    def test_board_with_pre_filled_cells(self):
        filled = {(0, 0), (1, 1), (2, 2)}
        board = PuzzleBoard(width=5, height=5, filled_cells=filled)
        assert len(board.filled_cells) == 3
        assert (0, 0) in board.filled_cells
        assert (1, 1) in board.filled_cells
        assert (2, 2) in board.filled_cells


class TestCheckPieceBounds:
    def test_piece_fits_within_bounds(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape
        assert board.check_piece(transformation, row=0, col=0) is True
        assert board.check_piece(transformation, row=3, col=3) is True

    def test_piece_exceeds_right_bound(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (2, 0)]  # Horizontal line of 3
        assert board.check_piece(transformation, row=0, col=4) is False

    def test_piece_exceeds_bottom_bound(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (0, 1), (0, 2)]  # Vertical line of 3
        assert board.check_piece(transformation, row=4, col=0) is False

    def test_piece_at_top_left_corner(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape
        assert board.check_piece(transformation, row=0, col=0) is True

    def test_piece_at_bottom_right_corner(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape
        # L-shape is 2x2, so bottom-right valid position is (3, 3) not (4, 4)
        assert board.check_piece(transformation, row=3, col=3) is True

    def test_negative_position(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape
        assert board.check_piece(transformation, row=-1, col=0) is False
        assert board.check_piece(transformation, row=0, col=-1) is False

    def test_piece_that_extends_beyond_all_bounds(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (5, 0), (0, 5)]  # Large L-shape
        assert board.check_piece(transformation, row=0, col=0) is False


class TestCheckPieceOverlap:
    def test_piece_does_not_overlap_empty_cells(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape
        assert board.check_piece(transformation, row=1, col=1) is True

    def test_piece_overlaps_single_filled_cell(self):
        board = PuzzleBoard(width=5, height=5, filled_cells={(1, 1)})
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape
        assert board.check_piece(transformation, row=1, col=1) is False

    def test_piece_overlaps_multiple_filled_cells(self):
        board = PuzzleBoard(width=5, height=5, filled_cells={(1, 1), (2, 1)})
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape
        assert board.check_piece(transformation, row=1, col=1) is False

    def test_piece_next_to_filled_cells(self):
        board = PuzzleBoard(width=5, height=5, filled_cells={(0, 0)})
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape
        assert board.check_piece(transformation, row=1, col=0) is True


class TestInsertPiece:
    def test_insert_piece_adds_cells(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape
        board.insert_piece(transformation, row=0, col=0)

        assert (0, 0) in board.filled_cells
        assert (1, 0) in board.filled_cells
        assert (0, 1) in board.filled_cells
        assert len(board.filled_cells) == 3

    def test_insert_piece_at_offset_position(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape
        board.insert_piece(transformation, row=2, col=2)

        assert (2, 2) in board.filled_cells
        assert (3, 2) in board.filled_cells
        assert (2, 3) in board.filled_cells
        assert len(board.filled_cells) == 3

    def test_insert_multiple_pieces(self):
        board = PuzzleBoard(width=5, height=5)
        transformation1 = [(0, 0), (1, 0), (0, 1)]  # L-shape
        transformation2 = [(0, 0)]  # Single cell

        board.insert_piece(transformation1, row=0, col=0)
        board.insert_piece(transformation2, row=2, col=2)

        assert len(board.filled_cells) == 4
        assert (0, 0) in board.filled_cells
        assert (1, 0) in board.filled_cells
        assert (0, 1) in board.filled_cells
        assert (2, 2) in board.filled_cells

    def test_insert_square_piece(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (0, 1), (1, 1)]  # 2x2 square
        board.insert_piece(transformation, row=1, col=1)

        assert (1, 1) in board.filled_cells
        assert (2, 1) in board.filled_cells
        assert (1, 2) in board.filled_cells
        assert (2, 2) in board.filled_cells
        assert len(board.filled_cells) == 4

    def test_insert_piece_out_of_bounds(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (2, 0)]  # Horizontal line of 3

        with pytest.raises(PiecePlacementError):
            board.insert_piece(transformation, row=0, col=4)

    def test_insert_piece_overlapping(self):
        board = PuzzleBoard(width=5, height=5, filled_cells={(0, 0)})
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape

        with pytest.raises(PiecePlacementError):
            board.insert_piece(transformation, row=0, col=0)


class TestRemovePiece:
    def test_remove_piece_clears_cells(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape

        board.insert_piece(transformation, row=0, col=0)
        assert len(board.filled_cells) == 3

        board.remove_piece(transformation, row=0, col=0)
        assert len(board.filled_cells) == 0

    def test_remove_piece_at_offset_position(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape

        board.insert_piece(transformation, row=2, col=2)
        board.remove_piece(transformation, row=2, col=2)

        assert (2, 2) not in board.filled_cells
        assert (3, 2) not in board.filled_cells
        assert (2, 3) not in board.filled_cells
        assert len(board.filled_cells) == 0

    def test_remove_piece_from_multiple_pieces(self):
        board = PuzzleBoard(width=5, height=5)
        transformation1 = [(0, 0), (1, 0), (0, 1)]  # L-shape
        transformation2 = [(0, 0)]  # Single cell

        board.insert_piece(transformation1, row=0, col=0)
        board.insert_piece(transformation2, row=2, col=2)
        assert len(board.filled_cells) == 4

        board.remove_piece(transformation1, row=0, col=0)
        assert len(board.filled_cells) == 1
        assert (2, 2) in board.filled_cells

    def test_remove_nonexistent_piece(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape

        with pytest.raises(PieceRemovalError):
            board.remove_piece(transformation, row=0, col=0)

    def test_remove_piece_from_wrong_position(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape

        board.insert_piece(transformation, row=0, col=0)
        assert len(board.filled_cells) == 3

        with pytest.raises(PieceRemovalError):
            board.remove_piece(transformation, row=2, col=2)


class TestIntegration:
    def test_check_then_insert_workflow(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape

        assert board.check_piece(transformation, row=0, col=0) is True

        board.insert_piece(transformation, row=0, col=0)

        assert board.check_piece(transformation, row=0, col=0) is False

    def test_insert_remove_insert_workflow(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(0, 0), (1, 0), (0, 1)]  # L-shape

        board.insert_piece(transformation, row=0, col=0)
        assert len(board.filled_cells) == 3

        board.remove_piece(transformation, row=0, col=0)
        assert len(board.filled_cells) == 0

        board.insert_piece(transformation, row=0, col=0)
        assert len(board.filled_cells) == 3

    def test_puzzle_tetris_example(self):
        board = PuzzleBoard(width=4, height=4)

        l_piece = [(0, 0), (1, 0), (0, 1)]
        line_piece = [(0, 0), (1, 0), (2, 0)]
        square_piece = [(0, 0), (1, 0), (0, 1), (1, 1)]

        board.insert_piece(l_piece, row=0, col=0)
        # Place line piece at row=1, col=1 to avoid overlap
        board.insert_piece(line_piece, row=1, col=1)
        # Square piece in bottom-right
        board.insert_piece(square_piece, row=2, col=2)

        # Total cells: 3 + 3 + 4 = 10
        assert len(board.filled_cells) == 10
        assert (0, 0) in board.filled_cells  # L-piece
        assert (1, 1) in board.filled_cells  # Line piece (at 1,1)
        assert (2, 2) in board.filled_cells  # Square piece


class TestPiecePositioning:
    def test_piece_positioning_leftmost_cell_of_first_row(self):
        board = PuzzleBoard(width=5, height=5)
        # Piece shape (first row has cells at column 1 and 2, second row has cell at column 0):
        #   xx
        # x
        transformation = [(1, 0), (2, 0), (0, 1)]

        board.insert_piece(transformation, row=1, col=2)

        # The leftmost cell of the first row is at (1, 0), so:
        # This should be at board position (col=2, row=1)
        # x_offset = 2 - 1 = 1, y_offset = 1 - 0 = 1
        # So: (1, 0) -> (2, 1), (2, 0) -> (3, 1), (0, 1) -> (1, 2)
        assert (2, 1) in board.filled_cells
        assert (3, 1) in board.filled_cells
        assert (1, 2) in board.filled_cells

    def test_check_piece_respects_positioning(self):
        board = PuzzleBoard(width=5, height=5)
        transformation = [(1, 0), (2, 0), (0, 1)]

        board.filled_cells.add((2, 1))
        board.filled_cells.add((3, 1))
        board.filled_cells.add((1, 2))

        assert board.check_piece(transformation, row=1, col=2) is False
        # At (0, 0): piece would extend to negative coordinates
        assert board.check_piece(transformation, row=0, col=0) is False

    def test_piece_with_single_cell_in_first_row(self):
        board = PuzzleBoard(width=5, height=5)
        # Piece shape:
        #  x
        # xx
        transformation = [(0, 0), (0, 1), (1, 1)]

        board.insert_piece(transformation, row=2, col=2)

        assert (2, 2) in board.filled_cells
        assert (2, 3) in board.filled_cells
        assert (3, 3) in board.filled_cells
