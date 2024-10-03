# Pathmaster: A Pathfinding Visualization Tool!


**Pathmaster** is a visual pathfinding tool built using Python and Pygame. It implements the **A*** ***algorithm*** to find the **shortest path between two nodes on a grid**. Users can interactively add walls, set start and end points, and visualize the pathfinding process in real-time. This project serves as both an educational resource for understanding pathfinding algorithms and a demonstration of Pygame’s capabilities for creating interactive applications.
## Table of Contents

-   [Project Overview](#project-overview)
-   [Features](#features)
-   [Technologies Used](#technologies-used)
-   [Installation](#installation)
-   [Usage](#usage)
-   [How It Works](#how-it-works)
-   [Contributing](#contributing)
-   [License](#license)
-   [Acknowledgments](#acknowledgments)


# Features

-   **Interactive Grid:** Click to set start and end nodes or to create walls.
-    A* Pathfinding Visualization: Observe the pathfinding process step-by-step.
-   **Undo Functionality:** Easily undo the last action taken.
-   **Clear Grid:** Reset the grid to start anew.
-   **Responsive UI:** Clear labels and buttons for easy interaction.
-   **Real-Time Feedback:** Immediate visual updates as nodes change states.

## Technologies Used

-   **Python:** Core programming language.
-   **Pygame:** For creating the interactive user interface and visualizations.
-   A* Algorithm: Pathfinding algorithm used for finding the shortest path.



## Installation

To run the PathMaster project locally, follow these steps:

1.  **Clone the repository:**
    
    bash
    
    Copy code
    
    `git clone https://github.com/arjavlamsal/pathmaster.git`
   `cd pathmaster` 
    
2.  **Install required libraries:** Make sure you have Python installed. Then, install Pygame using pip:
    
    bash
    
    Copy code
    
    `pip install pygame` 
    
3.  **Run the application:**
    
    bash
    
    Copy code
    
    `python main.py` 
    

## Usage

1.  **Set Start and End Nodes:** Right-click on the grid to place the start and end nodes.
2.  **Add Walls:** Left-click to create walls that block the path.
3.  **Execute Pathfinding:** Click the "Start" button to initiate the A* algorithm and visualize the pathfinding process.
4.  **Undo Actions:** Click the "Undo" button to remove the last placed wall or node.
5.  **Clear Grid:** Click the "Clear" button to reset the grid.

## How It Works

The project uses a grid system where each node represents a cell. The user can modify the grid by placing walls and defining start and end points. The A* algorithm then computes the shortest path based on the current grid configuration.

-   **Grid Initialization:** The grid is initialized with nodes, each having properties to determine its type (wall, path, road, etc.).
-   A* Algorithm: The A* algorithm evaluates paths based on cost functions, ensuring efficient pathfinding.
-   **Real-Time Visualization:** Pygame renders the grid and updates it based on user interactions and the algorithm's output.

## Contributing

Contributions are welcome! If you'd like to enhance PathMaster, feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes and commit them (`git commit -m 'Add new feature'`).
4.  Push to your branch (`git push origin feature/YourFeature`).
5.  Create a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

 ### Created by - Arjav Lamsal
```
