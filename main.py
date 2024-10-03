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
    rect_width = (WIDTH - 1)/cols
    rect_height = (HEIGHT - 21)/cols

    for i in range(rows):
        for j in range(cols):
            color = None
            node = grid[i][j]
            if node.type == 'wall':
                color = BLACK
            elif node == start or node == end:
                color = BLUE
            elif node.type == 'path':
                color = LIGHT_BLUE

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

    undo_log.append(node)
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
