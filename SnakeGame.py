import pygame
from random import randint

pygame.init()

#---------------------------------------#
# Define Constants                      #
#---------------------------------------#

# Define game window dimensions
WIDTH = 800
HEIGHT = 600
RIGHT = WIDTH
LEFT = 0
TOP = 0
BOTTOM = HEIGHT
MIDDLE = WIDTH // 2

# Define Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Define gameplay mechanics
SEGMENT_RADIUS = 10
EDGE_BUFFER = 1
OUTLINE = 0
STEP = 20
FPS_NORMAL = 20
FPS_FAST = 30
FONT_SIZE = 25
STARTING_LENGTH = 4
GAME_TIME = 60

#---------------------------------------#
# Initialize Objects/Variables          #
#---------------------------------------#

# Create the game window and set up clock and font
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("OCR-A Extended", FONT_SIZE)
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.5)
chompSound = pygame.mixer.Sound("chomp.wav")
chompSound.set_volume(1)


# Snake-related variables
score = 0
highScore = 0
stepX = 0
stepY = 0
segX = []
segY = []
color = None

# Apple-related variables
appleX = []
appleY = []
locationFree = None

# Timer-related variables
startTime = 0
timeLeft = 0
elapsedTime = 0

# Game state variables
inPlay = False
gameOver = False
inHome = False
FPS = 20

# Keys-related variables
keys = None

#---------------------------------------#
# Functions                             #
#---------------------------------------#

# Define the apple-generating function
def generateApples(appleX, appleY, segX, segY):
    # Randomly generate an apple with a 1/20 chance per frame
    if randint(1, 20) == 1:
        appleXPosition = randint(EDGE_BUFFER, WIDTH // STEP - EDGE_BUFFER) * STEP
        appleYPosition = randint(EDGE_BUFFER, HEIGHT // STEP - EDGE_BUFFER) * STEP
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

    # Return variables
    return appleX, appleY

# Define the game-drawing function
def drawGameWindow(segX, segY, appleX, appleY, score, timeLeft, highScore):
    # Clear the screen
    gameWindow.fill(BLACK)

    # Draw the snake with multiple colors
    for i in range(len(segX)):
        color = RED if i == 0 else BLUE
        pygame.draw.circle(gameWindow, color, (segX[i], segY[i]), SEGMENT_RADIUS, OUTLINE)

    # Draw the apples
    for i in range(len(appleX)):
        pygame.draw.circle(gameWindow, WHITE, (appleX[i], appleY[i]), SEGMENT_RADIUS, OUTLINE)

    # Draw the text info
    scoreText = font.render(f"Score: {score}", True, WHITE)
    highScoreText = font.render(f"High Score: {highScore}", True, WHITE)
    timerText = font.render(f"Time: {timeLeft}s", True, WHITE)

    gameWindow.blit(scoreText, (MIDDLE - 50, HEIGHT // 80))
    gameWindow.blit(highScoreText, (LEFT + 20, HEIGHT // 80))
    gameWindow.blit(timerText, (RIGHT - 150, HEIGHT // 80))

    # Update the display
    pygame.display.update()

# Define the game-initializing function
def startGame(FPS, fastMode):
    score = 0
    highScore = 0
    stepX = 0
    stepY = -STEP
    segX = []
    segY = []
    appleX = []
    appleY = []
    
    # Add head and 3 segments
    for i in range(4):
        segX.append(MIDDLE)
        segY.append(HEIGHT - 20 + i * STEP)

    # Set the countdown timer
    startTime = pygame.time.get_ticks()
    timeLeft = GAME_TIME

    if fastMode:
        FPS = 30
    else:
        FPS = 20

    inPlay = True
    while inPlay:
        # Calculate remaining time
        elapsedTime = (pygame.time.get_ticks() - startTime) // 1000 
        timeLeft = GAME_TIME - elapsedTime

        # If time runs out, end the game
        if timeLeft <= 0:
            inPlay = False

        # Generate apples and draw the game window
        appleX, appleY = generateApples(appleX, appleY, segX, segY)
        drawGameWindow(segX, segY, appleX, appleY, score, timeLeft, highScore)

        # Control game speed
        clock.tick(FPS)

        # Check if the snake head collides with the edges of the screen
        if segX[0] < LEFT or segX[0] >= RIGHT or segY[0] < TOP or segY[0] >= BOTTOM:
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

                # Play the chomp sound effect
                chompSound.play(loops = 0)

                # Increase the score when an apple is eaten
                score += 1

                # Increase FPS every 5 apples
                if score % 5 == 0:
                    FPS += 5
        
        if highScore < score:
            highScore = score

        # Move the snake
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

    # Show Game Over screen after death
    gameOver = True
    while gameOver:
        gameWindow.fill(BLACK)
        gameOverText = font.render("Game Over", True, WHITE)
        scoreText = font.render(f"Total Score: {score}", True, WHITE)
        highScoreText = font.render(f"High Score: {highScore}", True, WHITE)
        restartText = font.render("Press R to Restart", True, WHITE)
        homeText = font.render("Press H to Return to Home", True, WHITE)

        gameWindow.blit(gameOverText, (MIDDLE - 70, HEIGHT // 3 - 50))
        gameWindow.blit(scoreText, (MIDDLE - 105, HEIGHT // 3))
        gameWindow.blit(highScoreText, (LEFT + 20, HEIGHT // 80))
        gameWindow.blit(restartText, (MIDDLE - 135, HEIGHT // 3 + 50))
        gameWindow.blit(homeText, (MIDDLE - 190, HEIGHT // 3 + 100))

        pygame.display.update()

        # Wait for key press
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = False

        # Check if the user would like to replay or return to the home screen
        if keys[pygame.K_r]:
            return startGame(FPS, fastMode)
        if keys[pygame.K_h]:
            gameOver = False

    # Return variables
    return score, stepX, stepY, segX, segY, appleX, appleY, highScore

# Main loop
pygame.mixer.music.play(loops=-1)
inHome = True
while inHome:
    # Draw the home screen 
    gameWindow.fill(BLACK)
    titleText = font.render("Snake Game", True, WHITE)
    authorText = font.render("Created by Ari Khan", True, WHITE)
    modeText = font.render("Press 1 for Normal Mode", True, WHITE)
    fastModeText = font.render("Press 2 for Fast Mode", True, WHITE)
    highScoreText = font.render(f"High Score: {highScore}", True, WHITE)

    gameWindow.blit(titleText, (MIDDLE - 75, HEIGHT // 3 - 50))
    gameWindow.blit(authorText, (MIDDLE - 140, HEIGHT // 3))
    gameWindow.blit(modeText, (MIDDLE - 190, HEIGHT // 3 + 50))
    gameWindow.blit(fastModeText, (MIDDLE - 170, HEIGHT // 3 + 100))
    gameWindow.blit(highScoreText, (LEFT + 20, HEIGHT // 80))

    # Update the display
    pygame.display.update()

    # Handle quits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inHome = False

    keys = pygame.key.get_pressed()

    # Handle user input to start game
    if keys[pygame.K_1]:
        startGame(FPS_NORMAL, False)
    if keys[pygame.K_2]:
        startGame(FPS_FAST, True)

pygame.quit()
