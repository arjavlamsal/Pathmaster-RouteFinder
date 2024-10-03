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
