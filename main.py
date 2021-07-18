import pygame
import random
import sys  # We will use sys.exit to exit program
from pygame.locals import *
import time


# Game Functions
def welcomeScreen(score):
    """
    Shows welcome images on the screen
    """
    messageX = int(SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2
    messageY = int(0)

    while True:
        SCREEN.blit(GAME_SPRITES['message'], (messageX, messageY))
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        for event in pygame.event.get():
            # If user press cross or esc then quit the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # If user press space or up key then start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                mainGame()
                time.sleep(0.5)


def mainGame():
    """
    Main function which plays the game
    """
    score = 0
    playerX = int(SCREENWIDTH / 5)
    playerY = int(SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2

    baseX = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    newPipe3 = getRandomPipe()

    # My list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH, 'y': newPipe1[0]['y']},
        {'x': (4 / 3) * (SCREENWIDTH), 'y': newPipe2[0]['y']},
        {'x': (5 / 3) * (SCREENWIDTH), 'y': newPipe3[0]['y']}
    ]
    # My list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH, 'y': newPipe1[1]['y']},
        {'x': (4 / 3) * (SCREENWIDTH), 'y': newPipe2[1]['y']},
        {'x': (5 / 3) * (SCREENWIDTH), 'y': newPipe3[1]['y']}
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAcc = -8
    playerFlapped = False  # True when bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playerY > 0:
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerX, playerY, upperPipes, lowerPipes)  # Return true if crashed
        if crashTest:
            print(f"Your score is {score}")
            return

        # Check for score
        playerMidPos = playerX + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playerY = playerY + min(playerVelY, GROUNDY - playerY - playerHeight)

        # Move pipes to left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add other pipe when first pipe is about to go
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # If pipe is out of screen then remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (baseX, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerX, playerY))

        # Showing score
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digits in myDigits:
            width += GAME_SPRITES['numbers'][digits].get_width()
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.01))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def getRandomPipe():
    """
    Generate position of two pipes for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offest = int(GAME_SPRITES['player'].get_height()) + 10
    y2 = offest + random.randint(150, int(GROUNDY - 1.2 * offest))
    pipeX = SCREENWIDTH
    y1 = pipeHeight - y2 + offest + 100
    pipe = [
        {'x': pipeX, 'y': -y1},  # Upper Pipe
        {'x': pipeX, 'y': y2}  # Lower Pipe
    ]
    return pipe


def isCollide(playerX, playerY, upperPipes, lowerPipes):
    playerHeight = GAME_SPRITES['player'].get_height()
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    pipeWidth = GAME_SPRITES['pipe'][0].get_width()
    if playerY == GROUNDY - playerHeight or playerY < 1:
        GAME_SOUNDS['die'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playerY < pipeHeight + pipe['y'] and abs(playerX - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            GAME_SOUNDS['die'].play()
            return True

    for pipe in lowerPipes:
        if (playerY + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerX - pipe['x']) < \
                GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            GAME_SOUNDS['die'].play()
            return True
    return False


# Global variable for game
FPS = 32
SCREENWIDTH = 1095
SCREENHEIGHT = 624
GROUNDY = SCREENHEIGHT - 50
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'images/items/bird.png'
BACKGROUND = 'images/screen/bg.png'
PIPE = 'images/items/pipe.png'

if __name__ == '__main__':
    pygame.init()  # Initialize all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Saksham')  # Title of game
    pygame.display.set_icon(pygame.image.load("icon.ico"))

    # Loading scores
    GAME_SPRITES['numbers'] = (
        pygame.image.load('images/scores/0.png').convert_alpha(),
        pygame.image.load('images/scores/1.png').convert_alpha(),
        pygame.image.load('images/scores/2.png').convert_alpha(),
        pygame.image.load('images/scores/3.png').convert_alpha(),
        pygame.image.load('images/scores/4.png').convert_alpha(),
        pygame.image.load('images/scores/5.png').convert_alpha(),
        pygame.image.load('images/scores/6.png').convert_alpha(),
        pygame.image.load('images/scores/7.png').convert_alpha(),
        pygame.image.load('images/scores/8.png').convert_alpha(),
        pygame.image.load('images/scores/9.png').convert_alpha(),
    )

    # Loading accessories
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['message'] = pygame.image.load('images/screen/msg.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('images/screen/base.jpg').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    # Loading sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('sounds/die.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('sounds/hit.mp3')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('sounds/point.mp3')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('sounds/swoosh.mp3')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('sounds/wing.mp3')
    GAME_SOUNDS['back'] = pygame.mixer.Sound('sounds/back.mp3')

    # Game Loop
    while True:
        welcomeScreen(0)
