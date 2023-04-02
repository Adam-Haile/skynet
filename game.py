import pygame
import numpy as np
import math
import random

cards = []
playerOne = 0
playerTwo = 0
currentPlayer = 0
lastWinner = None
playerOneTotal = []
playerOneVisible = [None] * 12
playerTwoTotal = []
playerTwoVisible = [None] * 12
discardedCards = []

def newRound():
    for i in range(5):
        cards.append(-2)
    for i in range(10):
        cards.append(-1)
        cards.extend(range(1, 13))
    for i in range(15):
        cards.append(0)
    shuffle()

    for i in range(12):
        playerOneTotal.insert(0, drawDeck())
        playerTwoTotal.insert(0, drawDeck())

    for i in range(2):
        pos = random.randint(0, 11)
        playerOneVisible[pos] = playerOneTotal[pos]
        pos = random.randint(0, 11)
        playerTwoVisible[pos] = playerTwoTotal[pos]

    if lastWinner is None:
        global currentPlayer
        if getPlayerScore(1) >= getPlayerScore(2):
            currentPlayer = 1
        else:
            currentPlayer = 2
    else:
        currentPlayer = lastWinner

    print(getRoundState())

def getPlayerScore(player):
    total = 0
    if player == 1:
        for ele in playerOneVisible:
            if ele is not None:
                total += ele
    else:
        for ele in playerTwoVisible:
            if ele is not None:
                total += ele
    return total

def shuffle():
    np.random.shuffle(cards)

def drawDeck():
    if len(cards) == 0:
        topCard = discardedCards[0]
        for i in range(1, len(discardedCards) + 1):
            cards.append(discardedCards[i])
        discardedCards.clear()
        discardedCards.append(topCard)
        shuffle()

    return cards.pop()

def drawDiscard():
    return discardedCards.pop()

def discard(card):
    discardedCards.insert(0, card)

def getRoundState():
    if len(discardedCards) == 0:
        topDiscard = None
    else:
        topDiscard = discardedCards[0]
    playerOneScore = getPlayerScore(1)
    playerTwoScore = getPlayerScore(2)
    roundState = (playerOneVisible, playerOneScore, playerTwoVisible, playerTwoScore, topDiscard, currentPlayer)
    return roundState


running = True

if running:
    pygame.init()
    boundsX = 1024
    boundsY = 768
    window = pygame.display.set_mode([boundsX, boundsY])
    pygame.display.set_caption("Skyjo")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill((95, 141, 186))

    card_width = 100
    card_height = 150
    card_x = (boundsX - card_width) // 2
    card_y = (boundsY - card_height) // 2 
    red = 150
    green = 125
    blue = 255

    baseRect = pygame.draw.rect(window, (red, green, blue), (card_x, card_y, card_width, card_height), border_radius=10)
    pygame.draw.rect(window, (0, 0, 0), (card_x, card_y, card_width, card_height), 3)

    font = pygame.font.Font(None, 45)
    suit_text = font.render("Skyjo", True, (0, 0, 0))
    suit_text_rect = suit_text.get_rect(center=(card_x + 50, card_y + 70))
    window.blit(suit_text, suit_text_rect)


    pygame.display.flip()

# if running:
newRound()