"""PuzzlePiece class for representing polyomino puzzle pieces."""

from __future__ import annotations

from src.logic.validator import is_contiguous


class PuzzlePiece:
    """Represents a single polyomino piece with its shape, color, and unique identifier.

    Attributes:
        id: Unique identifier for the piece
        shape: Set of (row, col) coordinates defining the piece shape
        color: Display color (hex or named)
        precomputed_orientations: Precomputed unique orientations (8 max)
    """

    def __init__(self, id: str, shape: set[tuple[int, int]], color: str) -> None:
        """Initialize a puzzle piece.

        Args:
            id: Unique identifier for the piece
            shape: Set of (row, col) coordinates defining the piece shape
            color: Display color (hex or named)

        Raises:
            ValueError: If shape is empty or not contiguous
        """
        if not shape:
            raise ValueError("Shape cannot be empty")
        if not is_contiguous(shape):
            raise ValueError("Shape must be contiguous (all cells connected)")

        self._id = id
        self._shape = shape
        self._color = color
        # Precompute all 8 orientations (4 rotations × 2 mirrors) for performance
        self._precomputed_orientations = self._compute_all_orientations()

    @classmethod
    def _create_without_precompute(
        cls, id: str, shape: set[tuple[int, int]], color: str
    ) -> "PuzzlePiece":
        """Create a PuzzlePiece without triggering precomputation (for internal use).

        Args:
            id: Unique identifier for the piece
            shape: Set of (row, col) coordinates defining the piece shape
            color: Display color (hex or named)

        Returns:
            New PuzzlePiece instance without precomputed orientations
        """
        piece = object.__new__(cls)
        piece._id = id
        piece._shape = shape
        piece._color = color
        # Skip precomputation to avoid infinite recursion
        piece._precomputed_orientations = []
        return piece

    def _compute_all_orientations(self) -> list[PuzzlePiece]:
        """Compute and cache all unique orientations (8 max: 4 rotations × 2 mirrors).

        Returns:
            List of unique PuzzlePiece orientations (deduplicated)
        """
        orientations = []

        # Generate 4 rotations: 0°, 90°, 180°, 270°
        current_shape = self._shape
        for i in range(4):
            # Add original (not flipped) rotation (skip precomputation for these)
            orientations.append(
                PuzzlePiece._create_without_precompute(
                    f"{self._id}-rot{i * 90}",
                    current_shape.copy(),
                    self._color,
                )
            )
            # Add flipped version (horizontal flip) - compute shape without creating piece yet
            flipped_shape = self._flip_shape(current_shape, "horizontal")
            orientations.append(
                PuzzlePiece._create_without_precompute(
                    f"{self._id}-rot{i * 90}fh",
                    flipped_shape,
                    self._color,
                )
            )
            # Rotate 90° for next iteration
            current_shape = self._rotate_shape(current_shape, 90)

        # Deduplicate orientations by shape
        unique_orientations = []
        seen_shapes: set[frozenset[tuple[int, int]]] = set()
        for orientation in orientations:
            # Normalize shape to frozenset for hashing
            normalized = frozenset(orientation.get_normalized_shape())
            if normalized not in seen_shapes:
                seen_shapes.add(normalized)
                unique_orientations.append(orientation)

        return unique_orientations

    def _rotate_shape(
        self, shape: set[tuple[int, int]], degrees: int
    ) -> set[tuple[int, int]]:
        """Rotate a shape by specified degrees without creating a piece.

        Args:
            shape: Set of (row, col) coordinates
            degrees: Rotation angle in degrees (90, 180, 270)

        Returns:
            Rotated shape coordinates
        """
        degrees = degrees % 360
        if degrees == 0:
            return shape.copy()

        if degrees == 90:
            new_shape = {(col, -row) for row, col in shape}
        elif degrees == 180:
            new_shape = {(-row, -col) for row, col in shape}
        else:  # degrees == 270
            new_shape = {(-col, row) for row, col in shape}

        min_row = min(row for row, _ in new_shape)
        min_col = min(col for _, col in new_shape)
        return {(row - min_row, col - min_col) for row, col in new_shape}

    def _flip_shape(
        self, shape: set[tuple[int, int]], axis: str
    ) -> set[tuple[int, int]]:
        """Flip (mirror) a shape along specified axis without creating a piece.

        Args:
            shape: Set of (row, col) coordinates
            axis: 'horizontal' or 'vertical'

        Returns:
            Flipped shape coordinates
        """
        if axis == "horizontal":
            new_shape = {(row, -col) for row, col in shape}
        else:
            new_shape = {(-row, col) for row, col in shape}

        min_row = min(row for row, _ in new_shape)
        min_col = min(col for _, col in new_shape)
        return {(row - min_row, col - min_col) for row, col in new_shape}

    def get_precomputed_orientations(self) -> list[PuzzlePiece]:
        """Get precomputed orientations for solver use.

        Returns:
            List of unique PuzzlePiece orientations (precomputed for performance)
        """
        return self._precomputed_orientations

    @property
    def id(self) -> str:
        """Get the piece identifier."""
        return self._id

    @property
    def shape(self) -> set[tuple[int, int]]:
        """Get the piece shape coordinates."""
        return self._shape.copy()

    @property
    def color(self) -> str:
        """Get the piece color."""
        return self._color

    @property
    def area(self) -> int:
        """Get the number of cells in the piece."""
        return len(self._shape)

    def rotate(self, degrees: int = 90) -> PuzzlePiece:
        """Rotate the piece by specified degrees (90, 180, 270).

        Args:
            degrees: Rotation angle in degrees

        Returns:
            New PuzzlePiece with rotated shape

        Raises:
            ValueError: If degrees is not a multiple of 90
        """
        if degrees % 90 != 0:
            raise ValueError("Rotation must be a multiple of 90 degrees")

        # Normalize degrees to 0, 90, 180, or 270
        normalized_rotations = [0, 90, 180, 270]
        degrees = degrees % 360
        if degrees not in normalized_rotations:
            # Find the next valid rotation
            for valid_deg in normalized_rotations:
                if valid_deg > degrees:
                    degrees = valid_deg
                    break
            else:
                degrees = 0  # Wrap around to 0

        if degrees == 0:
            return self._create_copy()

        if degrees == 90:
            new_shape = {(col, -row) for row, col in self._shape}
        elif degrees == 180:
            new_shape = {(-row, -col) for row, col in self._shape}
        else:  # degrees == 270
            new_shape = {(-col, row) for row, col in self._shape}

        min_row = min(row for row, _ in new_shape)
        min_col = min(col for _, col in new_shape)
        normalized_shape = {(row - min_row, col - min_col) for row, col in new_shape}

        return PuzzlePiece(
            id=f"{self._id}-rot{degrees}",
            shape=normalized_shape,
            color=self._color,
        )

    def flip(self, axis: str = "horizontal") -> PuzzlePiece:
        """Flip (mirror) the piece along specified axis.

        Args:
            axis: 'horizontal' or 'vertical'

        Returns:
            New PuzzlePiece with flipped shape

        Raises:
            ValueError: If axis is not 'horizontal' or 'vertical'
        """
        if axis not in ("horizontal", "vertical"):
            raise ValueError("Axis must be 'horizontal' or 'vertical'")

        if axis == "horizontal":
            new_shape = {(row, -col) for row, col in self._shape}
        else:
            new_shape = {(-row, col) for row, col in self._shape}

        min_row = min(row for row, _ in new_shape)
        min_col = min(col for _, col in new_shape)
        normalized_shape = {(row - min_row, col - min_col) for row, col in new_shape}

        return PuzzlePiece(
            id=f"{self._id}-flip{axis[0]}",
            shape=normalized_shape,
            color=self._color,
        )

    def get_normalized_shape(self) -> set[tuple[int, int]]:
        """Return shape normalized to origin (min row/col = 0,0).

        Returns:
            Normalized shape coordinates
        """
        min_row = min(row for row, _ in self._shape)
        min_col = min(col for _, col in self._shape)
        return {(row - min_row, col - min_col) for row, col in self._shape}

    def get_rotations(self) -> list[PuzzlePiece]:
        """Generate all unique rotations of this piece.

        Returns:
            List of unique PuzzlePiece rotations (deduplicated)
        """
        rotations = []
        seen_shapes: set[frozenset[tuple[int, int]]] = set()

        for degrees in [0, 90, 180, 270]:
            rotated = self.rotate(degrees)
            shape_key = frozenset(rotated.get_normalized_shape())
            if shape_key not in seen_shapes:
                seen_shapes.add(shape_key)
                rotations.append(rotated)

        return rotations

    def get_all_orientations(self) -> list[PuzzlePiece]:
        """Generate all unique rotations and flips of this piece.

        Returns:
            List of unique PuzzlePiece orientations (deduplicated)
        """
        orientations = []
        seen_shapes: set[frozenset[tuple[int, int]]] = set()

        for flip_axis in [None, "horizontal", "vertical"]:
            if flip_axis is None:
                base_piece = self
            else:
                base_piece = self.flip(flip_axis)

            for degrees in [0, 90, 180, 270]:
                oriented = base_piece.rotate(degrees)
                shape_key = frozenset(oriented.get_normalized_shape())
                if shape_key not in seen_shapes:
                    seen_shapes.add(shape_key)
                    orientations.append(oriented)

        return orientations

    def get_bounding_box(self) -> tuple[int, int, int, int]:
        """Get bounding box (min_row, max_row, min_col, max_col).

        Returns:
            Tuple of bounding box coordinates
        """
        min_row = min(row for row, _ in self._shape)
        max_row = max(row for row, _ in self._shape)
        min_col = min(col for _, col in self._shape)
        max_col = max(col for _, col in self._shape)
        return (min_row, max_row, min_col, max_col)

    @property
    def width(self) -> int:
        """Get piece width (max_col - min_col + 1)."""
        min_col = min(col for _, col in self._shape)
        max_col = max(col for _, col in self._shape)
        return max_col - min_col + 1

    @property
    def height(self) -> int:
        """Get piece height (max_row - min_row + 1)."""
        min_row = min(row for row, _ in self._shape)
        max_row = max(row for row, _ in self._shape)
        return max_row - min_row + 1

    def _create_copy(self) -> PuzzlePiece:
        """Create a copy of this piece with the same attributes."""
        return PuzzlePiece(
            id=self._id,
            shape=self._shape.copy(),
            color=self._color,
        )

    def __eq__(self, other: object) -> bool:
        """Check equality with another piece."""
        if not isinstance(other, PuzzlePiece):
            return NotImplemented
        return (
            self._id == other._id
            and self._shape == other._shape
            and self._color == other._color
        )

    def __hash__(self) -> int:
        """Make piece hashable for use in sets and dicts."""
        return hash((self._id, frozenset(self._shape), self._color))

    def __repr__(self) -> str:
        """Get string representation."""
        return (
            f"PuzzlePiece(id='{self._id}', shape={self._shape}, color='{self._color}')"
        )
