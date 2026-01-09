# Woodster Jigsaw Puzzle

This Christmas I was gifted the [Aztec Labrinth puzzle](https://www.amazon.com/Bending-Wooden-Labyrinth-Difficult-Puzzles/dp/B08DDFNGV6) by Woodster.

Inspired by day 12 of [Advent of Code 2025](https://adventofcode.com/2025), I decided to make a solver for this puzzle.

**Place holder for demo video**

## Usage

### Running the Application

You can run the Woodster Jigsaw Solver using either method:

**Using Python module execution:**
```bash
python -m woodster_jigsaw_solver
```

**Direct script execution (from project root):**
```bash
python src/woodster_jigsaw_solver/__main__.py
```

### Application Overview

The solver provides a GUI interface with two main tabs:

1. **Board Tab**: Visualize and interact with the puzzle board grid
2. **Pieces Tab**: Manage puzzle pieces, including adding new pieces from images

### Basic Workflow

1. Launch the application using one of the methods above
2. Navigate to the **Pieces Tab** to add puzzle pieces from image files
3. Switch to the **Board Tab** to see the puzzle board and arrange pieces
4. Use the solver functionality to find solutions (WIP)

### Development

```bash
# Install dependencies
uv sync

# Run tests
pytest

# Run with coverage
pytest --cov=woodster_jigsaw_solver
```

## Technology Stack

This project was built using Python 3 along with the following libraries:

- [opencv](https://pypi.org/project/opencv-python/) - For image processing
- [numpy](https://numpy.org/) - For efficient array storage and processing
- [matplotlib](https://matplotlib.org/) - For animating the solving process
