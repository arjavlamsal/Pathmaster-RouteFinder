# Pathmaster: A* Pathfinding Algorithm Visualization Tool

## Overview

Pathmaster is a Python-based pathfinding algorithm implementation featuring the A* (A-star) algorithm, designed to visualize the process of finding the shortest path in a grid-like environment. Users can interactively add walls, set start and end points, and visualize the pathfinding process in real-time. This project serves as both an educational resource for understanding pathfinding algorithms and a demonstration of Pygame’s capabilities for creating interactive applications.This project demonstrates the application of graph theory and heuristic search algorithms, making it an excellent tool for understanding pathfinding in various contexts, such as Gaming, Robotics, and Geographic Information Systems (GIS).

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Algorithm Explanation](#algorithm-explanation)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Interactive Grid Representation:** Allows users to visualize the grid layout, including walls and traversable paths. Click to set start and end nodes or to create walls.
- A* Algorithm Implementation: Efficiently finds the shortest path from a start node to an end node while navigating obstacles.
- **Heuristic Calculation**: Utilizes heuristic scoring to optimize pathfinding decisions.
- **Reconstruction of Path**: Displays the final path found by the algorithm.
- **Custom Input Data**: Users can provide custom grid data to test various scenarios.
- **Responsive UI:** Clear labels and buttons for easy interaction.
- **Real-Time Feedback:** Immediate visual updates as nodes change states.

## Technologies Used

- **Python:** Core programming language.
- `math` library for mathematical calculations
- **Pygame:** For creating the interactive user interface and visualizations.

## Project Structure

```
Pathmaster/
├── main.py           # Main entry point for the pathfinding application
├── a_star.py         # Contains the A* algorithm implementation and associated classes
├── test_data/        # Directory containing input data files for testing
│   └── a_star.in     # Example input file defining grid layout
└── README.md         # Project documentation
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/arjavlamsal/Pathmaster-RouteFinder.git
   cd Pathmaster-RouteFinder
   ```

2. **Install dependencies**:
   This project requires Python 3.x. Pygame needs to be installed.
   ```bash
   pip install pygame
   ```

4. **Prepare input data**:
   Place your grid definition in the `test_data` directory, ensuring it's formatted correctly as integers (0 for road, 1 for wall, and 2 for start/end nodes).

## Usage

1. **Run the application**:
   Execute the following command to start the pathfinding algorithm:
   ```bash
   python main.py
   ```

2. **Input format**:
   The input file should consist of a grid where:
   - `0` represents a traversable path (road).
   - `1` represents an obstacle (wall).
   - `2` indicates the start and end nodes (only two `2`s should be present).

3. **Example input**:
   ```
   0 0 0 1 0
   0 1 0 0 0
   0 0 0 1 0
   1 1 0 2 0
   0 0 0 0 0
   ```
## Usage

1.  **Set Start and End Nodes:** Right-click on the grid to place the start and end nodes.
2.  **Add Walls:** Left-click to create walls that block the path.
3.  **Execute Pathfinding:** Click the "Start" button to initiate the A* algorithm and visualize the pathfinding process.
4.  **Undo Actions:** Click the "Undo" button to remove the last placed wall or node.
5.  **Clear Grid:** Click the "Clear" button to reset the grid.


## Algorithm Explanation

### A* Pathfinding Algorithm

The A* algorithm is a popular pathfinding and graph traversal algorithm that is efficient and optimal. It uses:
- **G-score**: The cost from the start node to the current node.
- **F-score**: The estimated total cost from the start node to the end node through the current node, calculated as:
  \[
  F = G + H
  \]
  where \( H \) is the heuristic score calculated using the distance between the current node and the end node.

The algorithm follows these steps:
1. Initialize the open set with the start node and set its G-score to zero.
2. While there are nodes in the open set:
   - Select the node with the lowest F-score.
   - If it is the end node, reconstruct the path.
   - Evaluate each neighbor and update their scores accordingly.
3. If no path is found, the algorithm concludes.

### Classes and Functions

- **Node**: Represents a single cell in the grid, including its coordinates, type, and scores.
- **get_neighbors()**: Retrieves valid neighboring nodes based on the current node's position.
- **distance()**: Calculates the Euclidean distance between two nodes.
- **h_score()**: Computes the heuristic distance from the current node to the end node.
- **reconstruct_path()**: Traces back the path from the end node to the start node.
- **a_star()**: Main function implementing the A* algorithm to find the shortest path.


## License

This project is licensed under the Apache 2.0 License.

---

Feel free to reach out if you have any questions or need further assistance with the project!

### Created by - Arjav Lamsal
