# PipeMania Solver (Artificial Intelligente Project)

## Description

PipeMania Solver is a Python-based solution to solve the PipeMania puzzle. The project leverages Artificial Intelligence search algorithms, such as Depth-First Search (DFS), to compute solutions for given PipeMania board instances.

## How It Works

The game consists of a square grid where different types of pipe pieces must be connected correctly to allow fluid to flow from a starting point (source) to an endpoint (sink). The solver:

1. Parses a grid-based input format.
2. Pre-processes the board to identify obvious placements.
3. Employs search algorithms to explore and determine valid configurations.
4. Verifies the correctness of the configuration using predefined game rules.
5. Outputs the final solved board.

## Features

- **Board Representation**: Efficient grid-based representation of the PipeMania board.
- **Piece Rotation Validation**: Ensures that pipe pieces connect properly to adjacent pieces.
- **Search Algorithms**: Implements various search algorithms including Depth-First Search (DFS).
- **Pre-Processing**: Reduces computational complexity by resolving straightforward cases before searching.
- **Interactive Parsing**: Reads board configuration directly from the input.

## Setup and Usage

### Prerequisites

- Python 3.8 or higher
- NumPy library

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/MiguelCBar/PipeMania-Solver-AI.git
   cd PipeMania-Solver
   ```

2. Install dependencies:
   ```bash
   pip install numpy
   ```

### Usage

1. Provide the board instance via standard input with the usage of the possible [configurations](/PipeMania_possible_configurations.png). For example:
   ```
   FC FB
   BE VB
   ```

2. Run the solver:
   ```bash
   python pipe.py
   ```

3. The output will be the solved board printed to the console.


## Credits

This project was developed by [Miguel Barbosa](https://github.com/MiguelCBar/) and [David Quintino](https://github.com/QuintinoDavid/).

