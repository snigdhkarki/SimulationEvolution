import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pygame 2D Array Example')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

colors = [RED, GREEN, BLUE, YELLOW]

# Define the 2D array (5x5 grid for this example)
array = [[random.choice(colors) for _ in range(5)] for _ in range(5)]

# Function to draw the 2D array
def draw_array():
    cell_size = 100
    for i, row in enumerate(array):
        for j, color in enumerate(row):
            pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))

# Function to change the array
def change_array():
    global array
    array = [[random.choice(colors) for _ in range(5)] for _ in range(5)]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_array()


    # Draw the 2D array
    draw_array()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()