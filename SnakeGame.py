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

# Define game window dimensions and colors
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Define gameplay mechanics
SEGMENT_RADIUS = 10
OUTLINE = 0
STEP = 20
FPS = 30
FONT_SIZE = 25

#---------------------------------------#
# Initialize Variables                  #
#---------------------------------------#

# Create the game window and set up clock and font
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("OCR-A Extended", FONT_SIZE)

# Movement variables for the snake
stepX = 0
stepY = -STEP
# Lists to track snake segments and apples
segX = []
segY = []
appleX = []
appleY = []

#---------------------------------------#
# Functions                             #
#---------------------------------------#

def generateApples():
    # Randomly generate an apple with a 1/20 chance per frame
    if randint(1, 20) == 1:
        appleXPosition = randint(0, WIDTH // STEP) * STEP
        appleYPosition = randint(0, HEIGHT // STEP) * STEP
        locationFree = True

        # Check if the apple's position overlaps the snake
        for i in range(len(segX)):
            if appleXPosition == segX[i] and appleYPosition == segY[i]:
                locationFree = False
        # Check if the apple's position overlaps existing apples
        for i in range(len(appleX)):
            if appleXPosition == appleX[i] and appleYPosition == appleY[i]:
                locationFree = False

        # Add apple if location is free
        if locationFree:
            appleX.append(appleXPosition)
            appleY.append(appleYPosition)

def drawGameWindow():
    # Clear the screen with a black background
    gameWindow.fill(BLACK)

    # Draw the snake; head is red, body is blue
    for i in range(len(segX)):
        color = RED if i == 0 else BLUE
        pygame.draw.circle(gameWindow, color, (segX[i], segY[i]), SEGMENT_RADIUS, OUTLINE)

    # Draw the apples
    for i in range(len(appleX)):
        pygame.draw.circle(gameWindow, WHITE, (appleX[i], appleY[i]), SEGMENT_RADIUS, OUTLINE)

    # Update the display with the new frame
    pygame.display.update()

#---------------------------------------#
# Main Program                          #
#---------------------------------------#

# Print instructions to the console
print("Use arrow keys to move. Press ESC to quit.")

# Initialize snake in the middle of the screen
for i in range(4):
    segX.append(WIDTH // 2)
    segY.append(HEIGHT // 2 + i * STEP)

inPlay = True
while inPlay:
    # Generate apples and draw the game window
    generateApples()
    drawGameWindow()
    # Control game speed
    clock.tick(FPS)

    # Check if the snake collides with the edges of the screen
    if segX[0] < 0 or segX[0] >= WIDTH or segY[0] < 0 or segY[0] >= HEIGHT:
        inPlay = False

    # Check if the snake collides with itself
    for i in range(1, len(segX)):
        if segX[0] == segX[i] and segY[0] == segY[i]:
            inPlay = False

    # Check if the snake eats an apple
    for i in range(len(appleX) - 1, -1, -1):
        if segX[0] == appleX[i] and segY[0] == appleY[i]:
            # Remove the apple and grow the snake
            del appleX[i]
            del appleY[i]
            segX.append(segX[-1])
            segY.append(segY[-1])

    # Move the snake by shifting segment positions
    for i in range(len(segX) - 1, 0, -1):
        segX[i] = segX[i - 1]
        segY[i] = segY[i - 1]
    segX[0] += stepX
    segY[0] += stepY
    
    # Check which keys are pressed
    keys = pygame.key.get_pressed()

    # Handle quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False

    # Handle player input for movement
    if keys[pygame.K_ESCAPE]:
        inPlay = False
    if keys[pygame.K_LEFT] and stepX == 0:
        stepX = -STEP
        stepY = 0
    if keys[pygame.K_RIGHT] and stepX == 0:
        stepX = STEP
        stepY = 0
    if keys[pygame.K_UP] and stepY == 0:
        stepX = 0
        stepY = -STEP
    if keys[pygame.K_DOWN] and stepY == 0:
        stepX = 0
        stepY = STEP

# Quit the game
pygame.quit()
