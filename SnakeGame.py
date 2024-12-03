#########################################
# File Name: SnakeGame.py
# Description: Snake Game based on template.
# Author: ICD2O1-02
# Date: 12/05/2024
#########################################

import pygame
from random import randint

pygame.init()

#---------------------------------------#
# Constants                             #
#---------------------------------------#

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Boundaries
TOP = 0
BOTTOM = HEIGHT
MIDDLE = WIDTH // 2
RIGHT = WIDTH
LEFT = 0

# Segment dimensions and movement steps
SEGMENT_RADIUS = 10
HORIZONTAL_STEP = 20
VERTICAL_STEP = 20

# Game settings
FPS = 30
FONT_SIZE = 25

#---------------------------------------#
# Initialize Variables                  #
#---------------------------------------#

gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("OCR-A Extended", FONT_SIZE)

stepX = 0
stepY = -VERTICAL_STEP

segX = []
segY = []

segmentColor = BLUE

#---------------------------------------#
# Functions                             #
#---------------------------------------#

def redraw_game_window():
    gameWindow.fill(BLACK)
    for i in range(len(segX)):
        color = RED if i == 0 else BLUE
        pygame.draw.circle(gameWindow, color, (segX[i], segY[i]), SEGMENT_RADIUS, 0)
    pygame.display.update()

#---------------------------------------#
# Main Program                          #
#---------------------------------------#

print("Use the arrow keys and the space bar.")
print("Press ESC to quit the game.")

# Initialize the snake
for i in range(4):
    segX.append(MIDDLE)
    segY.append(BOTTOM + i * VERTICAL_STEP)

in_play = True

while in_play:
    redraw_game_window()
    clock.tick(FPS)

    # Handle user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        in_play = False

    if keys[pygame.K_LEFT] and segX[0] > segX[1]:
        stepX = -HORIZONTAL_STEP
        stepY = 0

    if keys[pygame.K_RIGHT] and segX[0] < segX[1]:
        stepX = HORIZONTAL_STEP
        stepY = 0

    if keys[pygame.K_UP] and segY[0] > segY[1]:
        stepX = 0
        stepY = -VERTICAL_STEP

    if keys[pygame.K_DOWN] and segY[0] < segY[1]:
        stepX = 0
        stepY = VERTICAL_STEP

    if keys[pygame.K_SPACE]:  # Add a segment when the space bar is pressed
        segX.append(segX[-1])
        segY.append(segY[-1])

    # Check for collisions with boundaries
    if segX[0] > RIGHT or segX[0] < LEFT or segY[0] > BOTTOM or segY[0] < TOP:
        in_play = False

    # Move the segments
    for i in range(len(segX) - 1, 0, -1):
        segX[i] = segX[i - 1]
        segY[i] = segY[i - 1]

    # Move the head
    segX[0] += stepX
    segY[0] += stepY

    # Check for self-collision
    for i in range(1, len(segX)):
        if segX[0] == segX[i] and segY[0] == segY[i]:
            in_play = False

    pygame.event.clear()

pygame.quit()
