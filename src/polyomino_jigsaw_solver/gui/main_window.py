from typing import Dict, FrozenSet, Optional

import customtkinter as ctk

from polyomino_jigsaw_solver.gui.board_tab import PuzzleBoardTab
from polyomino_jigsaw_solver.gui.piece_tab import PuzzlePieceTab
from polyomino_jigsaw_solver.models.board_renderer import BoardRenderer
from polyomino_jigsaw_solver.models.puzzle_board import PuzzleBoard
from polyomino_jigsaw_solver.models.puzzle_piece import PuzzlePiece
from polyomino_jigsaw_solver.solver import solve_puzzle


class MainWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Woodster Jigsaw Solver")
        self.geometry("1200x900")

        # Set dark theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize state
        self.pieces: Dict[PuzzlePiece, int] = {}
        self.board_cells: FrozenSet[tuple[int, int]] = frozenset()

        self._setup_ui()

    def _setup_ui(self) -> None:
        # Title
        title = ctk.CTkLabel(
            self,
            text="Woodster Jigsaw Puzzle Solver",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        title.pack(padx=20, pady=(20, 10))

        # Tabview
        self.tabview = ctk.CTkTabview(self, width=900, height=500)
        self.tabview.pack(padx=20, pady=10)

        # Add custom tabs
        self.tabview.add("Puzzle Pieces")
        self.tabview.add("Puzzle Board")

        # Add tabs
        self.pieces_tab = PuzzlePieceTab(
            self.tabview.tab("Puzzle Pieces"),
            pieces=self.pieces,
            on_pieces_change=self._on_pieces_change,
        )
        self.pieces_tab.pack(fill="both", expand=True)

        self.board_tab = PuzzleBoardTab(
            self.tabview.tab("Puzzle Board"),
            board_cells=self.board_cells,
            on_board_change=self._on_board_change,
        )
        self.board_tab.pack(fill="both", expand=True)

        # Button frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(padx=20, pady=20)

        # Solve button (placeholder)
        solve_button = ctk.CTkButton(
            button_frame,
            text="Solve Puzzle",
            width=200,
            fg_color="#27ae60",
            hover_color="#2ecc71",
            command=self._on_solve,
        )
        solve_button.pack()

    def _on_pieces_change(self, pieces: Dict[PuzzlePiece, int]) -> None:
        self.pieces = pieces

    def _on_board_change(self, board_cells: FrozenSet[tuple[int, int]]) -> None:
        self.board_cells = board_cells

    def _on_solve(self) -> None:
        board_rows, board_cols = self.board_tab.get_board_size()

        if board_rows <= 0 or board_cols <= 0:
            label = ctk.CTkLabel(
                self, text="Invalid board dimensions!", text_color="#e74c3c"
            )
            label.pack(pady=5)
            self.after(3000, label.destroy)
            return

        if not self.pieces:
            label = ctk.CTkLabel(self, text="No pieces defined!", text_color="#e74c3c")
            label.pack(pady=5)
            self.after(3000, label.destroy)
            return

        board = PuzzleBoard(
            width=board_cols, height=board_rows, filled_cells=set(self.board_cells)
        )
        pieces = self.pieces.copy()
        renderer: Optional[BoardRenderer] = None

        try:
            from polyomino_jigsaw_solver.models.pygame_board_renderer import (
                PygameBoardRenderer,
            )

            renderer = PygameBoardRenderer(
                board_width=board_cols, board_height=board_rows
            )
        except ImportError:
            pass

        result = solve_puzzle(board, pieces, renderer)

        if renderer:
            renderer.close()

        if result is not None:
            label = ctk.CTkLabel(self, text="Puzzle solved!", text_color="#27ae60")
            label.pack(pady=5)
            self.after(3000, label.destroy)

            new_board_cells = frozenset(result.filled_cells)
            self.board_tab.set_board_cells(new_board_cells)
        else:
            label = ctk.CTkLabel(self, text="No solution found!", text_color="#e74c3c")
            label.pack(pady=5)
            self.after(3000, label.destroy)
