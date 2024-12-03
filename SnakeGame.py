#########################################
# File Name: SnakeGame.py
# Description: Snake Game based on template.
# Author: ICD2O1-02
# Date: 12/05/2024
#########################################
from random import randint
import pygame
pygame.init()

#---------------------------------------#
# Define Constants                      #
#---------------------------------------#

WIDTH = 800
HEIGHT = 600

TOP = 0
BOTTOM = HEIGHT
MIDDLE = WIDTH // 2
RIGHT = WIDTH
LEFT = 0
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
OUTLINE = 0

SEGMENT_R = 10
HSTEP = 20
VSTEP = 20

FPS = 30

FONT_SIZE = 25

#---------------------------------------#
# Define Lists / Variables              #
#---------------------------------------#

gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("OCR-A Extended", FONT_SIZE)

stepX = 0
stepY = -VSTEP
segX = []
segY = []

segmentCLR = BLUE

#---------------------------------------#
# Define Functions                      #
#---------------------------------------#
def redrawGameWindow():
    gameWindow.fill(BLACK)
    for i in range(len(segX)):
        if i == 0:
            segmentCLR = RED
        else:
            segmentCLR= BLUE
        pygame.draw.circle(gameWindow, segmentCLR, (segX[i], segY[i]), SEGMENT_R, OUTLINE)
    pygame.display.update() 

#---------------------------------------#
# Main Program                          #
#---------------------------------------#

print("Use the arrows and the space bar.")
print("Hit ESC to end the program.")

for i in range(4):
    segX.append(MIDDLE)
    segY.append(BOTTOM + i * VSTEP)

inPlay = True
while inPlay:
    redrawGameWindow()
    clock.tick(FPS)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        inPlay = False
    if keys[pygame.K_LEFT]:
        if segX[0] <= segX[1]:
            stepX = -HSTEP
            stepY = 0
    if keys[pygame.K_RIGHT]:
        if segX[0] >= segX[1]:
            stepX = HSTEP
            stepY = 0
    if keys[pygame.K_UP]:
        if segY[0] <= segY[1]:
            stepX = 0
            stepY = -VSTEP
    if keys[pygame.K_DOWN]:
        if segY[0] >= segY[1]:
            stepX = 0
            stepY = VSTEP
    if keys[pygame.K_SPACE]:            # if space bar is pressed, add a segment:
        segX.append(segX[-1])           # assign it the same x and y coordinates
        segY.append(segY[-1])           # as those of the last segment (at index -1)

    if segX[0] > RIGHT or segX[0] < LEFT:
        inPlay = False
    if segY[0] > BOTTOM or segY[0] < TOP:
        inPlay = False

    # Move the segments
    lastIndex = len(segX)-1
    for i in range(lastIndex, 0, -1):
        segX[i] = segX[i - 1]
        segY[i] = segY[i - 1]
    # Move the head
    segX[0] = segX[0] + stepX
    segY[0] = segY[0] + stepY

    for i in range(1, len(segX)):
        if segX[0] == segX[i] and segY[0] == segY[i]:
            inPlay = False

    pygame.event.clear()
#---------------------------------------#    
pygame.quit()
