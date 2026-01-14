import random

import pygame

from polyomino_jigsaw_solver.models.board_renderer import BoardRenderer
from polyomino_jigsaw_solver.models.puzzle_board import PuzzleBoard
from polyomino_jigsaw_solver.models.puzzle_piece import PuzzlePiece


class PygameBoardRenderer(BoardRenderer):
    """Renders a PuzzleBoard using Pygame."""

    def __init__(
        self,
        board_width: int,
        board_height: int,
        cell_size: int = 30,
        window_size: int | None = None,
        background_color: tuple[int, int, int] = (26, 26, 46),
        fill_color: tuple[int, int, int] = (74, 144, 226),
        grid_color: tuple[int, int, int] = (45, 45, 68),
        outline_color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        """Initialize the Pygame board renderer.

        Args:
            board_width: Width of the board in cells.
            board_height: Height of the board in cells.
            cell_size: Size of each cell in pixels.
            window_size: Size of the window in pixels (square). If None, uses board dimensions.
            background_color: RGB color for empty cells.
            fill_color: RGB color for filled cells.
            grid_color: RGB color for grid lines.
            outline_color: RGB color for piece outlines.
        """
        pygame.init()

        if window_size is None:
            window_size = max(board_width, board_height) * cell_size

        self.surface = pygame.display.set_mode((window_size, window_size))
        self.cell_size = cell_size
        self.board_width = board_width
        self.board_height = board_height
        self.background_color = background_color
        self.fill_color = fill_color
        self.grid_color = grid_color
        self.outline_color = outline_color

    def _draw_piece(
        self,
        transformation: list[tuple[int, int]],
        row: int,
        col: int,
        offset_x: int,
        offset_y: int,
    ) -> None:
        """Draw a single piece with outline.

        Args:
            transformation: The piece transformation as a list of (x, y) coordinates.
            row: The row where the piece is placed.
            col: The column where the piece is placed.
            offset_x: X offset for centering.
            offset_y: Y offset for centering.
        """
        if not transformation:
            return

        min_y = min(y for _, y in transformation)
        min_x = min(x for x, y in transformation if y == min_y)

        x_offset = col - min_x
        y_offset = row - min_y

        piece_cells = []
        for x, y in transformation:
            board_x = x + x_offset
            board_y = y + y_offset
            piece_cells.append((board_x, board_y))

        # Draw tight outline around piece (only unique edges)
        edges = set()

        # Add all edges to set
        for x, y in piece_cells:
            edges.add((x, y, "top"))
            edges.add((x, y, "bottom"))
            edges.add((x, y, "left"))
            edges.add((x, y, "right"))

        # Remove shared edges (two cells sharing the same edge)
        edges_to_remove = set()
        for x, y in piece_cells:
            # Check if right edge shares with left edge of neighbor
            if (x, y, "right") in edges and (x + 1, y, "left") in edges:
                edges_to_remove.add((x, y, "right"))
                edges_to_remove.add((x + 1, y, "left"))
            # Check if bottom edge shares with top edge of neighbor
            if (x, y, "bottom") in edges and (x, y + 1, "top") in edges:
                edges_to_remove.add((x, y, "bottom"))
                edges_to_remove.add((x, y + 1, "top"))

        edges -= edges_to_remove

        # Draw remaining unique edges
        for x, y, edge in edges:
            if edge == "top":
                start_pos = (
                    offset_x + x * self.cell_size,
                    offset_y + y * self.cell_size,
                )
                end_pos = (
                    offset_x + (x + 1) * self.cell_size,
                    offset_y + y * self.cell_size,
                )
                pygame.draw.line(
                    self.surface, self.outline_color, start_pos, end_pos, 4
                )
            elif edge == "bottom":
                start_pos = (
                    offset_x + x * self.cell_size,
                    offset_y + (y + 1) * self.cell_size,
                )
                end_pos = (
                    offset_x + (x + 1) * self.cell_size,
                    offset_y + (y + 1) * self.cell_size,
                )
                pygame.draw.line(
                    self.surface, self.outline_color, start_pos, end_pos, 4
                )
            elif edge == "left":
                start_pos = (
                    offset_x + x * self.cell_size,
                    offset_y + y * self.cell_size,
                )
                end_pos = (
                    offset_x + x * self.cell_size,
                    offset_y + (y + 1) * self.cell_size,
                )
                pygame.draw.line(
                    self.surface, self.outline_color, start_pos, end_pos, 4
                )
            elif edge == "right":
                start_pos = (
                    offset_x + (x + 1) * self.cell_size,
                    offset_y + y * self.cell_size,
                )
                end_pos = (
                    offset_x + (x + 1) * self.cell_size,
                    offset_y + (y + 1) * self.cell_size,
                )
                pygame.draw.line(
                    self.surface, self.outline_color, start_pos, end_pos, 4
                )

    def update(self, board: PuzzleBoard) -> None:
        """Render the board state to the Pygame surface and update display.

        Args:
            board: The PuzzleBoard object to display.
        """
        # Calculate board position to center it
        board_width = self.board_width * self.cell_size
        board_height = self.board_height * self.cell_size
        surface_width, surface_height = self.surface.get_size()
        offset_x = (surface_width - board_width) // 2
        offset_y = (surface_height - board_height) // 2

        self.surface.fill(self.background_color)

        # Draw all filled cells
        for x, y in board.filled_cells:
            x1 = offset_x + x * self.cell_size
            y1 = offset_y + y * self.cell_size
            rect = pygame.Rect(x1, y1, self.cell_size, self.cell_size)
            pygame.draw.rect(self.surface, self.fill_color, rect)

        # Draw each placed piece
        for transformation, row, col in board.placed_pieces:
            self._draw_piece(transformation, row, col, offset_x, offset_y)

        # Draw grid lines with transparency
        grid_surface = pygame.Surface((board_width, board_height), pygame.SRCALPHA)
        grid_surface.fill((0, 0, 0, 0))

        # Horizontal lines
        for i in range(self.board_height + 1):
            y = i * self.cell_size
            pygame.draw.line(
                grid_surface,
                (*self.grid_color, 128),
                (0, y),
                (board_width, y),
            )

        # Vertical lines
        for i in range(self.board_width + 1):
            x = i * self.cell_size
            pygame.draw.line(
                grid_surface,
                (*self.grid_color, 128),
                (x, 0),
                (x, board_height),
            )

        self.surface.blit(grid_surface, (offset_x, offset_y))

        pygame.display.flip()

    def close(self) -> None:
        """Close the pygame window and quit pygame."""
        pygame.quit()


if __name__ == "__main__":
    pygame.init()

    CELL_SIZE = 40
    BOARD_SIZE = 5
    WINDOW_SIZE = 400
    MAX_PLACEMENTS = 5

    def generate_random_piece() -> PuzzlePiece:
        piece_shapes = [
            # Monomino
            [(0, 0)],
            # Domino
            [(0, 0), (1, 0)],
            # Trominoes
            [(0, 0), (1, 0), (2, 0)],
            [(0, 0), (1, 0), (0, 1)],
            # Tetrominoes
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 0), (1, 0), (2, 0), (1, 1)],
            [(0, 0), (1, 0), (0, 1), (1, 1)],
            [(0, 0), (1, 0), (2, 0), (0, 1)],
        ]

        return PuzzlePiece(random.choice(piece_shapes))

    def find_valid_placement(board: PuzzleBoard, piece: PuzzlePiece) -> tuple | None:
        for transformation in piece.transformations:
            for row in range(board.height):
                for col in range(board.width):
                    if board.check_piece(list(transformation), row, col):
                        return (list(transformation), row, col)
        return None

    board = PuzzleBoard(width=BOARD_SIZE, height=BOARD_SIZE)
    pygame.display.set_caption("PygameBoardRenderer Test - Press ENTER to place pieces")

    renderer = PygameBoardRenderer(
        board_width=BOARD_SIZE,
        board_height=BOARD_SIZE,
        window_size=WINDOW_SIZE,
        cell_size=CELL_SIZE,
    )
    placements = 0

    # Place initial piece
    initial_piece = generate_random_piece()
    initial_placement = find_valid_placement(board, initial_piece)

    if initial_placement:
        transformation, row, col = initial_placement
        board.insert_piece(transformation, row, col)
        placements += 1
        print(f"Initial piece placed at row={row}, col={col}")
    else:
        print("Could not place initial piece")

    running = True
    renderer.update(board)

    print(
        f"Press ENTER to place a random piece (up to {MAX_PLACEMENTS} placements total)"
    )
    print("Press ESC or close window to exit")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN and placements < MAX_PLACEMENTS:
                    piece = generate_random_piece()
                    placement = find_valid_placement(board, piece)

                    if placement:
                        transformation, row, col = placement
                        board.insert_piece(transformation, row, col)
                        renderer.update(board)
                        placements += 1
                        print(f"Placed piece {placements}/{MAX_PLACEMENTS}")

                        if placements >= MAX_PLACEMENTS:
                            print("Maximum placements reached. Press ESC to exit.")
                    else:
                        print("Could not find a valid placement for the piece")

        pygame.time.wait(10)

    renderer.close()
