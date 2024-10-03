import math

class Node:
    def __init__(self, grid, x, y):
        # Initialize a node at position (x, y) in the given grid
        self.x = x  # Node's x-coordinate
        self.y = y  # Node's y-coordinate
        self.grid = grid  # Reference to the grid containing this node
        self.type = 'road'  # Default type of node is 'road'
        self.g_score = float('inf')  # Cost from start node to this node
        self.f_score = float('inf')  # Estimated total cost from start to end through this node

    def get_neighbors(self):
        # Retrieve neighboring nodes within the grid boundaries
        rows = len(self.grid)  # Total number of rows in the grid
        cols = len(self.grid[0])  # Total number of columns in the grid
        # Directions representing 8 possible movements (N, S, E, W, and diagonals)
        directions = [[1, 0], [1, 1], [0, 1], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        neighbors = []  # List to hold valid neighboring nodes

        for direction in directions:
            # Calculate neighbor coordinates based on the current direction
            neighbor_x = self.x + direction[0]
            neighbor_y = self.y + direction[1]
            # Check if the neighbor coordinates are within grid boundaries
            if 0 <= neighbor_x < cols and 0 <= neighbor_y < rows:
                neighbors.append(self.grid[neighbor_y][neighbor_x])  # Add valid neighbor to the list
        return neighbors


# Grid dimensions
rows = 40
cols = 40
grid = []  # Initialize an empty grid

# Open the input file containing grid data
file = open('./test_data/a_star.in', 'r')
lines = file.read().split('\n')  # Read and split the file into lines
file.close()  # Close the file

start = None  # Initialize start node
end = None  # Initialize end node

# Set up the grid from the test data
for i in range(rows):
    row = list(map(int, lines[i].split()))  # Convert each line into a list of integers
    row_nodes = []  # Initialize a list to hold nodes for this row
    for j in range(len(row)):
        node = Node(grid, j, i)  # Create a new node
        element = row[j]  # Get the element value (0, 1, or 2)
        if element == 1:
            node.type = 'wall'  # Set node type to 'wall'
        elif element == 2:
            if not start:
                start = node  # Set start node if not already set
            elif not end:
                end = node  # Set end node if not already set

        row_nodes.append(node)  # Add the node to the current row
    grid.append(row_nodes)  # Add the row to the grid

# Function to calculate the Euclidean distance between two nodes
def distance(node1, node2):
    return math.sqrt(math.pow(node1.x - node2.x, 2) + math.pow(node1.y - node2.y, 2))

# Function to compute the heuristic distance from the start node to the end node
def h_score(start, end):
    # Calculate the distance in x and y dimensions
    x_dist = abs(end.x - start.x)
    y_dist = abs(end.y - start.y)
    # Calculate the number of diagonal and straight steps needed
    diagonal_steps = min(x_dist, y_dist)
    straight_steps = y_dist + x_dist - 2 * diagonal_steps
    # Return the total heuristic score
    return diagonal_steps * math.sqrt(2) + straight_steps

def reconstruct_path(grid, came_from, current):
    # Rebuild the path from the end node to the start node
    path = [current]  # Initialize the path with the current node
    current_key = str(current.x) + ' ' + str(current.y)  # Create a unique key for the current node
    while current_key in came_from:
        current = came_from[current_key]  # Get the previous node in the path
        current_key = str(current.x) + ' ' + str(current.y)  # Update the key for the current node
        path.insert(0, current)  # Insert the current node at the beginning of the path
    return path  # Return the complete path

# A* pathfinding algorithm implementation
def a_star(grid, start, end):
    open_set = []  # List of nodes to be evaluated
    closed_set = []  # List of nodes already evaluated
    came_from = {}  # Dictionary to track the path

    start.g_score = 0  # Initialize g_score of the start node
    start.f_score = h_score(start, end)  # Calculate f_score for the start node

    open_set.append(start)  # Add start node to the open set

    while len(open_set) > 0:  # Continue while there are nodes to evaluate
        current = lowest_f_score(open_set)  # Get the node with the lowest f_score
        open_set.remove(current)  # Remove it from the open set
        closed_set.append(current)  # Add it to the closed set

        if current == end:  # If the current node is the end node, reconstruct the path
            return reconstruct_path(grid, came_from, current)

        for neighbor in current.get_neighbors():  # Loop through each neighbor of the current node
            if neighbor in closed_set or neighbor.type == 'wall':
                continue  # Ignore closed neighbors and walls
            
            # Check if both adjacent nodes are walls; skip if they are
            adj_node_1 = grid[current.y][neighbor.x]
            adj_node_2 = grid[neighbor.y][current.x]
            if adj_node_1.type == 'wall' and adj_node_2.type == 'wall':
                continue

            # Calculate the tentative g_score for this neighbor
            tentative_g_score = current.g_score + distance(current, neighbor)
            if neighbor not in open_set:
                open_set.append(neighbor)  # Add neighbor to open set if not already present
            elif tentative_g_score >= neighbor.g_score:
                continue  # Ignore if this path is not better

            # Found a better path; update the path tracking and scores
            came_from[str(neighbor.x) + ' ' + str(neighbor.y)] = current
            neighbor.g_score = tentative_g_score
            neighbor.f_score = neighbor.g_score + h_score(neighbor, end)  # Update f_score

def lowest_f_score(node_list):
    # Find the node with the lowest f_score in a given list of nodes
    final_node = None  # Initialize variable to hold the best node
    for node in node_list:
        if not final_node or node.f_score < final_node.f_score:
            final_node = node  # Update final_node if a better one is found
    return final_node  # Return the node with the lowest f_score
