import pygame
import sys
import os
import random
import time

pygame.init()
screenWidth = 1000
screenHeight = 690
size = (screenWidth, screenHeight)

ranList = []


def updateRandom():
    x = 0
    for i in range(20):
        x = random.randrange(100, 900, 1)
        ranList.append(x)


class StaticBlocks:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = WHITE
        pygame.draw.rect(screen, self.color,
                         [self.x, self.y, self.width, self.height])

    def display(self):
        pygame.draw.rect(screen, self.color,
                         [self.x, self.y, self.width, self.height])

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class MovingBlocks:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = WHITE
        pygame.draw.rect(screen, self.color,
                         [self.x, self.y, self.width, self.height])

    def display(self):
        pygame.draw.rect(screen, self.color,
                         [self.x, self.y, self.width, self.height])

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Hero:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 30
        self.color = RED
        pygame.draw.rect(screen, self.color,
                         [self.x, self.y, self.width, self.height])
        # pygame.display.update()

    def display(self):
        pygame.draw.rect(screen, self.color,
                         [self.x, self.y, self.width, self.height])
        # pygame.display.update()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


# colors and bunch of starting statements
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Beep Society")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# text display


def message_display(text):
    screen.fill(WHITE)
    largeText = pygame.font.Font('freesansbold.ttf', 60)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((1000/2), (690/2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


winner, loser, winPoints, lossPoints = "", "", 0, 0

speedOne = 2
speedTwo = 2


def roundChange(winner, loser, winPoints, lossPoints):
    if speedOne == 20 or speedTwo == 20:
        endingMessage(speedOne, speedTwo)
    screen.fill(WHITE)
    largeText = pygame.font.Font('freesansbold.ttf', 40)
    winningText = winner+" won the round with "+str(winPoints)+" points."
    losingText = loser+" lost the round with "+str(lossPoints)+" points."
    if winner=="Tie":
        winningTewxt = "It was a tie."
        losingText = ""
    TextSurf, TextRect = text_objects(winningText, largeText)
    TextRect.center = ((1000/2), (690/2))
    screen.blit(TextSurf, TextRect)
    TextSurf, TextRect = text_objects(losingText, largeText)
    TextRect.center = ((1000/2), (690/2+80))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)


def endingMessage(speedOne, speedTwo):
    screen.fill(WHITE)
    largeText = pygame.font.Font('freesansbold.ttf', 60)
    if speedOne == 20:
        text = "Player One won."
    else:
        text = "Player Two won."
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((1000/2), (690/2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()


carryOn = True
clock = pygame.time.Clock()
velocity = 8
player1 = True
playerHero = Hero(500, 660, 20, 30)
playerHero.display()
# 500 is middle. 660 is where we draw from

# static blocks
staticObstacle = StaticBlocks(100, 100, 10, 10)
staticScore = [False, False, False, False]

# moving blocks
speedOne = 2
speedTwo = 2
speedCount = [0, 0, 0, 0, 0]
directionRight = [True, False, True, False, True]
movingScore = [False, False, False, False, False]

updateRandom()
score = 0
space = False
died = False

message_display("PRESS SPACE TO START")

while carryOn:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
    screen.fill(GREEN)
    phx = playerHero.x
    phy = playerHero.y

    # checking for play pause
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not space:
        space = True
        start_time = pygame.time.get_ticks()

    # each river is 90 units. land is 40 units.
    riverY = 40
    riverHeight = 90
    for i in range(5):
        pygame.draw.rect(screen, BLUE, (0, riverY, 1000, riverHeight))
        riverY += 130

    playerHero.display()

    # static obstacles
    staticarrayX = []
    staticY = 150
    for i in range(4):
        if died:
            break
        staticX = ranList[i]
        staticObstacle = StaticBlocks(staticX, staticY-10, 20, 20)
        staticObstacle.display()
        if playerHero.get_rect().colliderect(staticObstacle.get_rect()):
            if not staticScore[i]:
                staticScore[i] = True
            died = True
        elif not player1 and not staticScore[i]:
            if playerHero.y > staticY+10:
                staticScore[i] = True
                score += 5
        elif player1 and not staticScore[i]:
            if playerHero.y < staticY-10:
                staticScore[i] = True
                score += 5
        staticY += 130

    # moving objects
    movingarrayX = []
    movingY = 40
    for i in range(5):
        if died:
            break
        movingX = ranList[-i]
        movingObstacle = MovingBlocks(
            movingX+speedCount[i], movingY+20, 40, 40)
        movingObstacle.display()
        if space:
            if player1:
                speed = speedOne
            else:
                speed = speedTwo
            if directionRight[i]:
                speedCount[i] += speed
            else:
                speedCount[i] -= speed
            if movingX+speedCount[i] > 950:
                directionRight[i] = False
            if movingX+speedCount[i] < 50:
                directionRight[i] = True
        if playerHero.get_rect().colliderect(movingObstacle.get_rect()):
            if not movingScore[i]:
                movingScore[i] = True
            died = True
        elif not player1 and not movingScore[i]:
            if playerHero.y > movingY+20:
                movingScore[i] = True
                score += 10
        elif player1 and not movingScore[i]:
            if playerHero.y < movingY-20:
                movingScore[i] = True
                score += 10
        movingY += 130

    pygame.display.flip()

    if player1:
        if playerHero.y < 10 or died:
            timeTaken = 0
            if not died:
                timeTaken = pygame.time.get_ticks() - start_time
            else:
                timeTaken = 100000 
            player1 = False
            playerHero.y = 10
            space = False
            playerHero.x = 500
            movingScore = [False, False, False, False, False]
            staticScore = [False, False, False, False]
            died = False
            playerOneScore = score+int((100-(timeTaken/1000)))
            score = 0
    else:
        if playerHero.y > 630 or died:
            timeTaken = 0
            if not died:
                timeTaken = pygame.time.get_ticks() - start_time
            else:
                timeTaken = 100000            
            player1 = True
            playerHero.y = 650
            space = False
            playerHero.x = 500
            movingScore = [False, False, False, False, False]
            staticScore = [False, False, False, False]
            died = False
            playerTwoScore = score+int((100-(timeTaken/1000)))
            if playerOneScore == playerTwoScore:
                winner = "Tie"
                roundChange(winner, loser, winPoints, lossPoints)
            elif playerOneScore > playerTwoScore:
                winner = "Player One"
                loser = "Player Two"
                winPoints = playerOneScore
                lossPoints = playerTwoScore
                speedOne += 2
                roundChange(winner, loser, winPoints, lossPoints)
            else:
                winner = "Player Two"
                loser = "Player One"
                winPoints = playerTwoScore
                lossPoints = playerOneScore
                speedTwo += 2
                roundChange(winner, loser, winPoints, lossPoints)
            score = 0

    # movement of player
    if space:
        if player1:
            if keys[pygame.K_LEFT] and phx > velocity:
                playerHero.x -= velocity
            if keys[pygame.K_RIGHT] and phx < (screenWidth-20-velocity):
                playerHero.x += velocity
            if keys[pygame.K_UP] and phy > velocity:
                playerHero.y -= velocity
            if keys[pygame.K_DOWN] and phy < (screenHeight-30-velocity):
                playerHero.y += velocity
        else:
            if keys[pygame.K_a] and phx > velocity:
                playerHero.x -= velocity
            if keys[pygame.K_d] and phx < (screenWidth-20-velocity):
                playerHero.x += velocity
            if keys[pygame.K_w] and phy > velocity:
                playerHero.y -= velocity
            if keys[pygame.K_s] and phy < (screenHeight-30-velocity):
                playerHero.y += velocity

    clock.tick(60)

pygame.quit()
