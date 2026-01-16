# Feature Specification: Polyomino Puzzle Solver

**Feature Branch**: `[001-polyomino-puzzle-solver]`
**Created**: January 14, 2026
**Status**: Draft
**Input**: User description: "Build an app in python that solves a jigsaw puzzle with polyomino pieces. Initially the app will open a GUI where the user can manually input the pieces of the puzzle and the shape of the board. After, when the user presses solve, the app will open another window where it will give a visualization of the program trying to solve the puzzle using a backtracking algorithm."

## Clarifications

### Session 2026-01-14

- Q: What format should be used for saving/loading puzzle configurations and export/import? → A: JSON (JavaScript Object Notation)
- Q: What should be the maximum allowed board dimensions (width × height in cells) that the application can handle? → A: 50×50 cells
- Q: Should users be able to control the visualization speed during solving, or should it be a fixed delay? → A: User-adjustable speed control (slider or presets)
- Q: Should pieces be distinguished by unique colors in the visualization, or use a single color for all pieces? → A: Unique colors for each piece type
- Q: When the user modifies the puzzle configuration while the solver is running, how should the system respond? → A: Disable edit controls during solving with notification

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Define Puzzle Configuration (Priority: P1)

The user launches the application and sees a graphical interface where they can define the puzzle pieces and board shape. They interact with a grid-based editor to draw the shape of each polyomino piece and specify the dimensions of the board where pieces will be placed. The user can add multiple pieces of various shapes and sizes to their puzzle configuration.

**Why this priority**: This is the foundational user journey - without the ability to define puzzles, no other functionality can exist. It represents the core value proposition of allowing users to create and solve custom puzzles.

**Independent Test**: Can be tested by launching the application, drawing a simple piece, setting board dimensions, and verifying the configuration persists. Delivers the ability to define puzzle structures without needing solving capabilities.

**Acceptance Scenarios**:

1. **Given** the application is launched, **When** the user draws a shape on the grid editor, **Then** the shape is visually displayed and stored as a defined piece
2. **Given** the application is launched, **When** the user sets the board dimensions (width and height), **Then** the board boundary is displayed in the editor
3. **Given** multiple pieces have been defined, **When** the user selects a piece, **Then** the piece shape is highlighted in the editor
4. **Given** a piece has been defined, **When** the user deletes it, **Then** the piece is removed from the configuration

---

### User Story 2 - Solve Puzzle Visualization (Priority: P2)

After defining the puzzle configuration, the user clicks the "Solve" button. A new window opens displaying the board and pieces. The application shows a real-time visualization of the backtracking algorithm attempting to place pieces on the board. The user watches as pieces are tried in different positions, backtracking when placements lead to dead ends, until a solution is found or all possibilities are exhausted.

**Why this priority**: This is the primary user-facing outcome - users want to see the algorithm work and understand how the solution is reached. It provides educational value and demonstrates the problem-solving process.

**Independent Test**: Can be tested by defining a simple solvable puzzle (e.g., 2x2 board with two L-shaped tetrominoes), clicking solve, and verifying pieces are placed on the board with visible backtracking behavior when dead ends are encountered.

**Acceptance Scenarios**:

1. **Given** a valid puzzle configuration, **When** the user clicks "Solve", **Then** a new visualization window opens showing the empty board
2. **Given** the visualization window is open, **When** the algorithm attempts a piece placement, **Then** the piece appears on the board in the trial position
3. **Given** a piece placement leads to a dead end, **When** the algorithm backtracks, **Then** the piece is removed and a different placement is tried
4. **Given** the algorithm finds a solution, **When** the board is fully filled, **Then** all pieces are displayed in their final positions and the process stops
5. **Given** no solution exists, **When** all possibilities are exhausted, **Then** the visualization indicates that no solution was found

---

### User Story 3 - Puzzle Management (Priority: P3)

The user can save puzzle configurations for later use and load previously saved puzzles. They can also clear the current configuration to start fresh, export puzzle configurations to share with others, and import configurations received from other users.

**Why this priority**: This enhances usability by allowing users to build a library of puzzles and share interesting configurations. It's valuable but not essential for core functionality.

**Independent Test**: Can be tested by creating a puzzle configuration, saving it, clearing the editor, loading the saved puzzle, and verifying the configuration matches what was saved. Delivers persistence and sharing capabilities.

**Acceptance Scenarios**:

1. **Given** a puzzle configuration is defined, **When** the user saves it with a name, **Then** the configuration is stored and appears in the list of saved puzzles
2. **Given** saved puzzles exist, **When** the user selects and loads one, **Then** the editor displays the loaded configuration exactly as saved
3. **Given** a puzzle configuration is defined, **When** the user clicks "Clear", **Then** all pieces and board settings are reset to the default state
4. **Given** a puzzle configuration, **When** the user exports it, **Then** a file is created containing the puzzle data
5. **Given** a puzzle file, **When** the user imports it, **Then** the editor displays the imported configuration

---

### Edge Cases

- What happens when the user defines pieces that have a total area larger than the board area?
- What happens when the user defines no pieces or an empty board?
- What happens when pieces have overlapping shapes or invalid geometries?
- How does the system handle puzzles at the maximum limit (50×50 board with many pieces)?
- What happens if the user clicks "Solve" multiple times quickly?
- How does the visualization handle puzzles that take an extremely long time to solve or are computationally intractable?
- What happens when the user closes the visualization window before solving completes?
- When the user attempts to modify the puzzle configuration while the solver is running, edit controls are disabled and a notification is displayed informing the user that editing is locked during solving

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a graphical interface for defining polyomino piece shapes on a grid
- **FR-002**: System MUST allow users to specify board dimensions through the graphical interface, with maximum dimensions of 50×50 cells
- **FR-003**: System MUST support defining multiple polyomino pieces of various shapes and sizes
- **FR-004**: System MUST validate that piece shapes are contiguous and contain at least one grid cell
- **FR-005**: System MUST visualize each piece type with a unique color for clear visual distinction in both editor and visualization windows
- **FR-006**: System MUST provide a "Solve" action that triggers the solving algorithm
- **FR-007**: System MUST open a separate visualization window when solving begins
- **FR-008**: System MUST display the board grid in the visualization window
- **FR-009**: System MUST show real-time placement of pieces as the algorithm attempts solutions
- **FR-010**: System MUST visualize backtracking by removing pieces and trying alternative placements
- **FR-011**: System MUST indicate when a complete solution has been found
- **FR-012**: System MUST indicate when no solution exists after exhaustive search
- **FR-013**: System MUST allow users to interrupt or stop the solving process at any time
- **FR-014**: System MUST disable edit controls while the solver is running and display a notification to the user
- **FR-015**: System MUST allow users to adjust visualization speed during solving through slider or preset options
- **FR-016**: System MUST prevent duplicate piece placements in the same position during a single solution attempt
- **FR-017**: System MUST support rotating pieces at 90°, 180°, and 270° orientations during solving
- **FR-018**: System MUST support flipping (mirroring) pieces during solving to create additional orientation variations
- **FR-019**: System MUST save and load puzzle configurations using JSON format
- **FR-020**: System MUST export and import puzzle configurations using JSON format

### Key Entities

- **Polyomino Piece**: Represents a connected shape made of square grid cells, characterized by its shape (pattern of cells), its unique color assignment, and potentially its orientation/rotation state
- **Board**: Represents the rectangular grid area where pieces must be placed without overlap to solve the puzzle, characterized by its width, height, and cell occupancy state
- **Puzzle Configuration**: Represents a complete puzzle definition containing the board dimensions and the set of polyomino pieces that must be placed
- **Solution State**: Represents the current state of the solving process, including the current board configuration, pieces placed, placement order, and backtracking history

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can define a complete puzzle configuration (board + pieces) in under 3 minutes
- **SC-002**: The solver visualization shows piece placements with default delay of 100ms between placements for puzzles with up to 20 pieces, with user-adjustable speed control
- **SC-003**: 95% of users successfully define and solve their first puzzle within 5 minutes of launching the application
- **SC-004**: The application maintains a minimum of 30 frames per second during visualization for puzzles with up to 50 total grid cells
- **SC-005**: 80% of users can correctly identify when backtracking occurs in the visualization (verified through user testing)
- **SC-006**: The solver finds valid solutions for all correctly configured solvable puzzles (no false negatives)
- **SC-007**: The solver correctly identifies unsolvable configurations (no false positives)

## Assumptions

- Polyomino pieces are made of connected square cells (common definition in tiling puzzles)
- The backtracking algorithm should explore all possible piece placements systematically
- Users have basic familiarity with grid-based drawing interfaces
- Puzzles are small enough that backtracking can find solutions in reasonable time (e.g., under 2 minutes for typical puzzles)
- Users want to understand the solving process, not just see the final result
- The visualization speed should be slow enough to follow but fast enough not to be tedious

## Out of Scope

- Pre-defined puzzle libraries or templates
- Automatic piece generation or puzzle generation algorithms
- Solving optimization beyond basic backtracking (e.g., heuristics, pruning strategies, parallel solving)
- Advanced features like piece mirroring or non-rectangular board shapes (note: flipping is allowed per FR-016)
- Mobile or web interfaces
- Performance optimization for very large puzzles (100+ cells)
- Save/load functionality beyond JSON file-based export/import (e.g., databases, cloud sync)
- Multi-user or collaborative features
- Analysis tools (e.g., move counting, time statistics)
