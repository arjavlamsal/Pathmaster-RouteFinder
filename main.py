import pygame
import sys
from astar import Node, a_star  # Import necessary components from astar

# Initialize Pygame
pygame.init()
pygame.font.init()

# Constants for display dimensions and grid size
HEIGHT = 600
WIDTH = 600
ROWS = 40
COLS = 40

# Color Definitions
WHITE = (255, 255, 255)  # Color for the background
BLUE = (0, 0, 255)        # Color for start/end nodes
LIGHT_BLUE = (135, 206, 250)  # Color for path nodes
BLACK = (0, 0, 0)        # Color for wall nodes
GRAY = (128, 128, 128)   # Color for grid lines

# Setup display
display = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)  # Set up the Pygame display
icon = pygame.image.load('./img/icon.png')  # Load the window icon
pygame.display.set_icon(icon)  # Set the window icon
pygame.display.set_caption('Pathfinder')  # Set the window title

# Font for UI text
font = pygame.font.SysFont('Arial', 10)  # Create a font object for text rendering
text_labels = {
    'start_end': font.render('Start/End Node (Right Click)', False, BLACK),  # Text label for start/end node
    'wall': font.render('Wall Node (Left Click)', False, BLACK),  # Text label for wall node
    'start': font.render('Start', False, WHITE),  # Text label for start button
    'undo': font.render('Undo', False, WHITE),  # Text label for undo button
    'clear': font.render('Clear', False, WHITE),  # Text label for clear button
}

# Global Variables
grid = []  # 2D list to hold nodes
undo_log = []  # List to track actions for undo functionality
start_node = None  # Variable to hold the start node
end_node = None  # Variable to hold the end node

def reset_grid():
    """Initialize the grid and reset start and end nodes."""
    global grid, start_node, end_node, undo_log
    grid = []  # Reset the grid
    undo_log = []  # Reset the undo log
    start_node = None  # Reset start node
    end_node = None  # Reset end node

    # Create a grid of nodes
    for i in range(ROWS):
        row_nodes = [Node(grid, j, i) for j in range(COLS)]  # Create nodes for each column
        grid.append(row_nodes)  # Append row of nodes to the grid
    update_grid()  # Update the grid display

def update_display():
    """Update the main display with the current state of the grid."""
    display.fill(WHITE)  # Fill the display with white background
    pygame.draw.rect(display, BLUE, (10, 5, 10, 10))  # Draw color box for Start/End
    pygame.draw.rect(display, BLACK, (200, 5, 10, 10))  # Draw color box for Wall
    display.blit(text_labels['start_end'], (25, 5))  # Render text label for start/end
    display.blit(text_labels['wall'], (215, 5))  # Render text label for wall

    # Draw buttons on the display
    pygame.draw.rect(display, BLACK, (355, 7, 40, 10))  # Draw Start Button
    pygame.draw.rect(display, BLACK, (435, 7, 40, 10))  # Draw Undo Button
    pygame.draw.rect(display, BLACK, (515, 7, 40, 10))  # Draw Clear Button

    display.blit(text_labels['start'], (362, 6))  # Render Start button label
    display.blit(text_labels['undo'], (443, 6))  # Render Undo button label
    display.blit(text_labels['clear'], (524, 6))  # Render Clear button label

def update_grid():
    """Draw the grid based on the node states."""
    update_display()  # Update the display with UI elements
    rect_width = (WIDTH - 1) / COLS  # Calculate the width of each grid cell
    rect_height = (HEIGHT - 21) / ROWS  # Calculate the height of each grid cell

    # Draw each node in the grid
    for i in range(ROWS):
        for j in range(COLS):
            node = grid[i][j]  # Get the current node
            color = get_node_color(node)  # Get the color based on node type
            if color:
                # Draw the node rectangle in the appropriate color
                pygame.draw.rect(display, color, (j * rect_width + 1, i * rect_height + 21, rect_width, rect_height))

    # Draw grid lines for visual reference
    for i in range(COLS + 1):
        pygame.draw.rect(display, GRAY, (i * rect_width, 20, 1, HEIGHT))  # Draw vertical grid lines
        pygame.draw.rect(display, GRAY, (0, i * rect_height + 20, WIDTH, 1))  # Draw horizontal grid lines

    pygame.display.update()  # Update the display to show the new grid

def get_node_color(node):
    """Return the color for the specified node."""
    if node.type == 'wall':  # Check if node is a wall
        return BLACK
    elif node == start_node or node == end_node:  # Check if node is start or end
        return BLUE
    elif node.type == 'path':  # Check if node is part of the path
        return LIGHT_BLUE
    return None  # Default case if no color is assigned

def draw_tile(x, y, tile_type):
    """Update the grid with a new tile based on user input."""
    global start_node, end_node, undo_log
    clear_path_nodes()  # Clear any existing path nodes

    row = ((y - 20) * ROWS) // (HEIGHT - 20)  # Calculate the row index based on mouse position
    col = (x * COLS) // WIDTH  # Calculate the column index based on mouse position

    if not (0 <= row < ROWS and 0 <= col < COLS):  # Ensure the click is within grid bounds
        return

    node = grid[row][col]  # Get the clicked node

    # Validate tile placement to avoid conflicts
    if node.type == 'wall' or node == start_node or node == end_node or (tile_type == 'endpoint' and start_node and end_node):
        return  # Prevent placement of walls or endpoints in invalid states

    # Place wall or endpoint based on user action
    if tile_type == 'wall':
        node.type = 'wall'  # Set node type to wall
    elif tile_type == 'endpoint':
        if not start_node:  # If there is no start node set it
            start_node = node
        elif not end_node:  # If there is no end node set it
            end_node = node

    undo_log.append(node)  # Add the node to the undo log
    update_grid()  # Refresh the grid display

def clear_path_nodes():
    """Reset all path nodes to their default state."""
    for row in grid:  # Iterate through each row
        for node in row:  # Iterate through each node in the row
            if node.type == 'path':  # Check if node is part of the path
                node.type = 'road'  # Reset path node to default road type

def pathfind():
    """Execute the A* pathfinding algorithm."""
    if not start_node or not end_node:  # Ensure both start and end nodes are set
        print('Please mark both endpoint nodes.')
        return

    path = a_star(grid, start_node, end_node)  # Run A* algorithm to find the path
    if not path:  # Check if a path was found
        print('No possible paths.')
        return

    distance = round(path[-1].f_score, 2)  # Get the distance of the found path
    distance = int(distance) if distance % 1 == 0 else distance  # Format distance for output
    print(f'Path found with distance {distance}.')  # Output the distance of the path

    # Mark the path nodes in the grid
    for node in path:
        if node != start_node and node != end_node:  # Avoid marking start and end nodes
            node.type = 'path'  # Set node type to path
    update_grid()  # Refresh the grid display

def main_loop():
    """Main event loop for handling user input."""
    reset_grid()  # Reset the grid at the start of the program
    update_grid()  # Update the display with the initial grid state
    
    while True:  # Main loop for handling events
        for event in pygame.event.get():  # Process each event in the queue
            if event.type == pygame.QUIT:  # Check for window close event
                pygame.quit()  # Quit Pygame
                sys.exit()  # Exit the program

            # Handle left click for walls and buttons
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()  # Get mouse position
                x, y = mouse_pos  # Unpack mouse coordinates

                # Check for button clicks to trigger actions
                if 355 <= x <= 395 and 7 <= y <= 17:  # Start Button area
                    pathfind()  # Execute pathfinding
                elif 435 <= x <= 475 and 7 <= y <= 17:  # Undo Button area
                    undo_last_action()  # Undo the last action
                elif 515 <= x <= 555 and 7 <= y <= 17:  # Clear Button area
                    reset_grid()  # Reset the grid
                else:
                    draw_tile(x, y, 'wall')  # Add wall node at clicked position

            # Right click to set start/end node
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_pos = pygame.mouse.get_pos()  # Get mouse position
                x, y = mouse_pos  # Unpack mouse coordinates
                draw_tile(x, y, 'endpoint')  # Set the clicked tile as start/end node

            # Continuous wall drawing while left button is pressed
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()  # Get mouse position
                x, y = mouse_pos  # Unpack mouse coordinates
                draw_tile(x, y, 'wall')  # Draw wall continuously

def undo_last_action():
    """Undo the last action performed by the user."""
    global start_node, end_node
    if undo_log:  # Check if there are actions to undo
        node = undo_log.pop()  # Get the last node from the undo log
        node.type = 'road'  # Reset node type to road
        if node == start_node:  # Check if the node was the start node
            start_node = None  # Clear start node if it was undone
        elif node == end_node:  # Check if the node was the end node
            end_node = None  # Clear end node if it was undone
        update_grid()  # Refresh the grid display

if __name__ == "__main__":
    main_loop()  # Start the main event loop
