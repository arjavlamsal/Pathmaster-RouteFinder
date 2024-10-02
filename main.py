# dark blue for end nodes
# light blue for path
# dark green for currently searched nodes
# light green for already searched nodes
# white for empty

import pygame, sys

pygame.init()
pygame.font.init()

# Screen dimensions
HEIGHT = 600
WIDTH = 600

# Set up display
display = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

# Color definitions
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Font setup
font = pygame.font.SysFont('Arial', 10)

# Button labels
text1 = font.render('Start/End Node (Right Click)', False, BLACK)
text2 = font.render('Wall Node (Left Click)', False, BLACK)
text3 = font.render('Start', False, WHITE)
text4 = font.render('Undo', False, WHITE)
text5 = font.render('Clear', False, WHITE)

# Set window icon and caption
icon = pygame.image.load('./img/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Pathfinder')

# Function to update display
def update_display():
    display.fill(WHITE)
    
    # Draw labels and buttons
    pygame.draw.rect(display, BLUE, (10, 5, 10, 10))
    pygame.draw.rect(display, BLACK, (200, 5, 10, 10))
    display.blit(text1, (25, 5))
    display.blit(text2, (215, 5))

    # Buttons
    pygame.draw.rect(display, BLACK, (355, 7, 40, 10))
    pygame.draw.rect(display, BLACK, (435, 7, 40, 10))
    pygame.draw.rect(display, BLACK, (515, 7, 40, 10))

    display.blit(text3, (362, 6))
    display.blit(text4, (443, 6))
    display.blit(text5, (524, 6))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    update_display()
    pygame.display.update()
