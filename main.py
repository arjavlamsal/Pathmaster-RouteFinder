import pygame
import sys
from astar import Node, a_star  # Import necessary components from astar

# Initialize Pygame
pygame.init()
pygame.font.init()

# Constants
HEIGHT = 600
WIDTH = 600
ROWS = 40
COLS = 40

# Color Definitions
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 250)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Setup display
display = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
icon = pygame.image.load('./img/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Pathfinder')

# Font for UI text
font = pygame.font.SysFont('Arial', 10)
text_labels = {
    'start_end': font.render('Start/End Node (Right Click)', False, BLACK),
    'wall': font.render('Wall Node (Left Click)', False, BLACK),
    'start': font.render('Start', False, WHITE),
    'undo': font.render('Undo', False, WHITE),
    'clear': font.render('Clear', False, WHITE),
}

# Global Variables
grid = []
undo_log = []
start_node = None
end_node = None

def reset_grid():
    """Initialize the grid and reset start and end nodes."""
    global grid, start_node, end_node, undo_log
    grid = []
    undo_log = []
    start_node = None
    end_node = None

    for i in range(ROWS):
        row_nodes = [Node(grid, j, i) for j in range(COLS)]
        grid.append(row_nodes)
    update_grid()

def update_display():
    """Update the main display with the current state of the grid."""
    display.fill(WHITE)
    pygame.draw.rect(display, BLUE, (10, 5, 10, 10))  # Start/End color
    pygame.draw.rect(display, BLACK, (200, 5, 10, 10))  # Wall color
    display.blit(text_labels['start_end'], (25, 5))
    display.blit(text_labels['wall'], (215, 5))

    # Draw buttons
    pygame.draw.rect(display, BLACK, (355, 7, 40, 10))  # Start Button
    pygame.draw.rect(display, BLACK, (435, 7, 40, 10))  # Undo Button
    pygame.draw.rect(display, BLACK, (515, 7, 40, 10))  # Clear Button

    display.blit(text_labels['start'], (362, 6))
    display.blit(text_labels['undo'], (443, 6))
    display.blit(text_labels['clear'], (524, 6))

def update_grid():
    """Draw the grid based on the node states."""
    update_display()
    rect_width = (WIDTH - 1) / COLS
    rect_height = (HEIGHT - 21) / ROWS

    for i in range(ROWS):
        for j in range(COLS):
            node = grid[i][j]
            color = get_node_color(node)
            if color:
                pygame.draw.rect(display, color, (j * rect_width + 1, i * rect_height + 21, rect_width, rect_height))

    # Draw grid lines
    for i in range(COLS + 1):
        pygame.draw.rect(display, GRAY, (i * rect_width, 20, 1, HEIGHT))  # Vertical lines
        pygame.draw.rect(display, GRAY, (0, i * rect_height + 20, WIDTH, 1))  # Horizontal lines

    pygame.display.update()

def get_node_color(node):
    """Return the color for the specified node."""
    if node.type == 'wall':
        return BLACK
    elif node == start_node or node == end_node:
        return BLUE
    elif node.type == 'path':
        return LIGHT_BLUE
    return None

def draw_tile(x, y, tile_type):
    """Update the grid with a new tile based on user input."""
    global start_node, end_node, undo_log
    clear_path_nodes()

    row = ((y - 20) * ROWS) // (HEIGHT - 20)
    col = (x * COLS) // WIDTH

    if not (0 <= row < ROWS and 0 <= col < COLS):
        return  # Ensure the click is within the grid

    node = grid[row][col]

    # Validate tile placement
    if node.type == 'wall' or node == start_node or node == end_node or (tile_type == 'endpoint' and start_node and end_node):
        return

    # Place wall or endpoint
    if tile_type == 'wall':
        node.type = 'wall'
    elif tile_type == 'endpoint':
        if not start_node:
            start_node = node
        elif not end_node:
            end_node = node

    undo_log.append(node)
    update_grid()

def clear_path_nodes():
    """Reset all path nodes to their default state."""
    for row in grid:
        for node in row:
            if node.type == 'path':
                node.type = 'road'

def pathfind():
    """Execute the A* pathfinding algorithm."""
    if not start_node or not end_node:
        print('Please mark both endpoint nodes.')
        return

    path = a_star(grid, start_node, end_node)
    if not path:
        print('No possible paths.')
        return

    distance = round(path[-1].f_score, 2)
    distance = int(distance) if distance % 1 == 0 else distance
    print(f'Path found with distance {distance}.')

    for node in path:
        if node != start_node and node != end_node:
            node.type = 'path'
    update_grid()

def main_loop():
    """Main event loop for handling user input."""
    reset_grid()
    update_grid()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle left click for walls and buttons
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                x, y = mouse_pos

                # Check for button clicks
                if 355 <= x <= 395 and 7 <= y <= 17:  # Start Button
                    pathfind()
                elif 435 <= x <= 475 and 7 <= y <= 17:  # Undo Button
                    undo_last_action()
                elif 515 <= x <= 555 and 7 <= y <= 17:  # Clear Button
                    reset_grid()
                else:
                    draw_tile(x, y, 'wall')  # Add wall node

            # Right click to set start/end node
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                x, y = mouse_pos
                draw_tile(x, y, 'endpoint')

            # Continuous wall drawing while left button is pressed
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                x, y = mouse_pos
                draw_tile(x, y, 'wall')

def undo_last_action():
    """Undo the last action performed by the user."""
    global start_node, end_node
    if undo_log:
        node = undo_log.pop()  # Get the last node
        node.type = 'road'  # Reset node type
        if node == start_node:
            start_node = None  # Clear start node if it was undone
        elif node == end_node:
            end_node = None  # Clear end node if it was undone
        update_grid()  # Refresh the grid display

if __name__ == "__main__":
    main_loop()  # Start the main event loop
