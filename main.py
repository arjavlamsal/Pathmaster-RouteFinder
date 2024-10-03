import pygame, math, sys
from astar import *

pygame.init()
pygame.font.init()

HEIGHT = 600
WIDTH = 600

display = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 250)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)  # Color for the final path
RED = (255, 0, 0)    # Color for evaluated nodes

font = pygame.font.SysFont('Arial', 10)

rows = 40
cols = 40
grid = []
undo_log = []
start = None
end = None

def reset_grid():
    global grid, start, end, undo_log
    grid, undo_log, start, end = [], [], None, None

    for i in range(rows):
        row_nodes = []
        for j in range(cols):
            node = Node(grid, j, i)
            row_nodes.append(node)
        grid.append(row_nodes)
    update_grid(display, grid)

def update_grid(display, grid):
    rect_width = (WIDTH - 1) / cols
    rect_height = (HEIGHT - 21) / cols

    for i in range(rows):
        for j in range(cols):
            color = None
            node = grid[i][j]
            if node.type == 'wall':
                color = BLACK
            elif node == start:
                color = BLUE
            elif node == end:
                color = BLUE
            elif node.type == 'path':
                color = LIGHT_BLUE
            elif node.type == 'evaluated':
                color = RED  # Color for evaluated nodes

            if color:
                pygame.draw.rect(display, color, (j * rect_width + 1, i * rect_height + 21, rect_width, rect_height))

    for i in range(len(grid) + 1):
        pygame.draw.rect(display, GRAY, (i * rect_width, 20, 1, HEIGHT))
        pygame.draw.rect(display, GRAY, (0, i * rect_height + 20, WIDTH, 1))

    pygame.display.update()

reset_grid()
update_grid(display, grid)

def clear_path_nodes():
    # Clear all path nodes, resetting them to 'road'
    for i in range(rows):
        for j in range(cols):
            node = grid[i][j]
            if node.type == 'path':
                node.type = 'road'
            elif node.type == 'evaluated':
                node.type = 'road'  # Reset evaluated nodes to 'road'

def draw_tile(x, y, tile_type):
    global start, end, undo_log
    clear_path_nodes()  # Clear path nodes before drawing new nodes

    row = ((y - 20) * rows) // (HEIGHT - 20)
    col = (x * cols) // WIDTH
    node = grid[row][col]

    # Validate position
    if row < 0 or col < 0 or row >= rows or col >= cols or node.type == 'wall' or node == start or node == end:
        return
    elif tile_type == 'endpoint' and start and end:
        return

    if tile_type == 'wall':
        grid[row][col].type = 'wall'
    elif tile_type == 'endpoint':
        if not start:
            start = node
        elif not end:
            end = node

    undo_log.append((node, node.type))  # Store the node and its type in undo_log
    update_grid(display, grid)

def undo_action():
    global start, end, undo_log

    if undo_log:
        node, node_type = undo_log.pop()  # Get the last action from the undo_log

        if node == start:
            start = None
        elif node == end:
            end = None
        elif node_type == 'wall':
            node.type = 'road'
        
        update_grid(display, grid)

def visualize_pathfinding():
    global start, end

    if not start or not end:
        return

    open_set = [start]
    closed_set = []

    while open_set:
        current_node = min(open_set, key=lambda n: n.f)

        if current_node == end:
            reconstruct_path(current_node)
            return

        open_set.remove(current_node)
        closed_set.append(current_node)
        current_node.type = 'evaluated'  # Mark node as evaluated
        update_grid(display, grid)
        pygame.time.delay(50)  # Slow down the visualization

        for neighbor in current_node.neighbors:
            if neighbor in closed_set or neighbor.type == 'wall':
                continue
            if neighbor not in open_set:
                open_set.append(neighbor)

def reconstruct_path(current_node):
    while current_node:
        current_node.type = 'path'
        current_node = current_node.parent  # Assuming each node has a reference to its parent

    update_grid(display, grid)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check for left or right clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            x = mouse_pos[0]
            y = mouse_pos[1]

            # Right click to place start/end nodes
            if event.button == 3:
                draw_tile(x, y, 'endpoint')

            # Left click to place walls
            elif event.button == 1:
                draw_tile(x, y, 'wall')

        # Continuous left-click for drawing walls
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            x = mouse_pos[0]
            y = mouse_pos[1]
            draw_tile(x, y, 'wall')

        # Undo action when 'z' key is pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            undo_action()

        # Start pathfinding when 'p' key is pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            visualize_pathfinding()
