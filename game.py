import pygame
import numpy as np
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
    return discardedCards.pop(0)

def discard(card):
    discardedCards.insert(0, card)

def getRoundState():
    if len(discardedCards) == 0:
        topDiscard = None
    else:
        topDiscard = discardedCards[0]
    playerOneScore = getPlayerScore(1)
    playerTwoScore = getPlayerScore(2)
    roundState = (playerOneVisible, playerOneScore, playerOne, playerTwoVisible, playerTwoScore, playerTwo, topDiscard, currentPlayer, isRoundOver(), isGameOver())
    return roundState

def isRoundOver():
    roundOver = 0
    if playerOneTotal == playerOneVisible:
        roundOver = 1
    if playerTwoTotal == playerTwoVisible:
        roundOver = 2

    return roundOver

def isGameOver():
    gameOver = False
    if (playerOne >= 100) or (playerTwo >= 100):
        gameOver = True

    return gameOver

def swapCard(player, i, value):
    if player == 1:
        playerOneTotal[i] = value
        playerOneVisible[i] = value
    if player == 2:
        playerTwoTotal[i] = value
        playerTwoVisible[i] = value

def switchCurrent():
    global currentPlayer

    if currentPlayer == 1:
        currentPlayer = 2
    elif currentPlayer == 2:
        currentPlayer = 1

running = True

newRound()


if running:
    pygame.init()
    boundsX = 1024
    boundsY = 768
    window = pygame.display.set_mode([boundsX, boundsY])
    pygame.display.set_caption("Skyjo")

card_width = 100
card_height = 150

DEFAULT = (150, 100, 200)
DEEP_BLUE = (100, 50, 255)
LIGHT_BLUE = (150, 150, 255)
GREEN = (125, 255, 125)
YELLOW = (255, 255, 100)
RED = (255, 100, 100)
font = pygame.font.Font(None, 75)
skyfont = pygame.font.Font(None, 40)
smallfont = pygame.font.Font(None, 22)


class Card():
    def __init__(self, value, position=0):
        super().__init__()
        self.image = pygame.Surface((card_width, card_height))
        self.rect = self.image.get_rect()
        self.value = value
        self.position = position

        if self.value is None:
            self.image.fill(DEFAULT)
        else:
            if self.value < 0:
                self.image.fill(DEEP_BLUE)
            if self.value == 0:
                self.image.fill(LIGHT_BLUE)
            if self.value > 0 and self.value < 5:
                self.image.fill(GREEN)
            if self.value >= 5 and self.value < 9:
                self.image.fill(YELLOW)
            if self.value >= 9:
                self.image.fill(RED)

        self.color = (0, 0, 0)

        width = card_width
        height = card_height
        pygame.draw.rect(self.image, self.color, [0, 0, width, height], 3)

        if self.value is None:
            text = skyfont.render("SKYJO", True, self.color)
            self.image.blit(text, [7.5, card_height/2 - 15, text.get_rect().width, text.get_rect().height])
        else:
            text = font.render(str(value).capitalize(), True, self.color)
            if len(str(value)) == 2:
                self.image.blit(text, [card_width/2 - 27, card_height/2 - 25, text.get_rect().width, text.get_rect().height])
            if len(str(value)) == 1:
                self.image.blit(text, [card_width/2 - 15, card_height/2 - 25, text.get_rect().width, text.get_rect().height])

    def moveTo(self, x, y):
        self.rect.x = (x - card_width / 2)
        self.rect.y = (y - card_height / 2)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def getRect(self):
        return self.rect
    
swapFromDeck = False
swapFromDiscard = False
drawnCard = -3
lastSwap = False
roundOver = False
topDiscard = Card(None)

def tallyRoundScore():
    if isRoundOver() is not 0:
        global playerOne
        global playerTwo
        global playerOneVisible
        global playerTwoVisible
        
        lastWinner = isRoundOver()
        playerOneScore = getPlayerScore(1)
        playerTwoScore = getPlayerScore(2)

        if lastWinner == 1 and playerOneScore <= playerTwoScore:
            playerOneScore *= 2
        if lastWinner == 2 and playerTwoScore <= playerOneScore:
            playerTwoScore *= 2

        playerOne += playerOneScore
        playerTwo += playerTwoScore
        cards.clear()
        discardedCards.clear()
        playerOneTotal.clear()
        playerOneVisible.clear()
        playerOneVisible = [None] * 12
        playerTwoTotal.clear()
        playerTwoVisible.clear()
        playerTwoVisible = [None] * 12
        if running:
            global swapFromDeck
            global swapFromDiscard
            global drawnCard
            global lastSwap
            global roundOver
            global topDiscard
            swapFromDeck = False
            swapFromDiscard = False
            drawnCard = -3
            lastSwap = False
            roundOver = False
            topDiscard = Card(None)

        newRound()

while running:
    playerOneGameCards = []
    playerTwoGameCards = []
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill((95, 141, 186))

    i = 0

    p1 = None
    p2 = None
    if getPlayerScore(1) < getPlayerScore(2):
        p1 = GREEN
        p2 = RED
    elif getPlayerScore(2) < getPlayerScore(1):
        p1 = RED
        p2 = GREEN
    else:
        p1 = YELLOW
        p2 = YELLOW

    text = skyfont.render("Current Player: " + str(currentPlayer), True, (255, 255, 255))
    window.blit(text, [boundsX/2 - 125, boundsY - 75, text.get_rect().width, text.get_rect().height])

    text = smallfont.render("Total Player Score: " + str(playerOne), True, (255, 255, 255))
    window.blit(text, [boundsX/20, card_height/2 - 35, text.get_rect().width, text.get_rect().height])

    text = skyfont.render("Player Score: " + str(getPlayerScore(1)), True, p1)
    window.blit(text, [boundsX/20, card_height/2 - 15, text.get_rect().width, text.get_rect().height])

    text = smallfont.render("Total Player Score: " + str(playerTwo), True, (255, 255, 255))
    window.blit(text, [boundsX/20 + 500, card_height/2 - 35, text.get_rect().width, text.get_rect().height])

    text = skyfont.render("Player Score: " + str(getPlayerScore(2)), True, p2)
    window.blit(text, [boundsX/20 + 500, card_height/2 - 15, text.get_rect().width, text.get_rect().height])

    for y in range(3):
        for x in range(4):
            newCard = Card(playerOneVisible[i], i)
            newCard.moveTo((boundsX / 10) + (x * 105), (boundsY / 4) + (y * 200) - 25)
            newCard.draw(window)
            playerOneGameCards.append(newCard)

            newCard = Card(playerTwoVisible[i], i)
            newCard.moveTo((boundsX / 10) + (x * 105) + 500, (boundsY / 4) + (y * 200) - 25)
            newCard.draw(window)
            playerTwoGameCards.append(newCard)
            i += 1

    if len(discardedCards) > 0:
        topDiscard = Card(discardedCards[0])
        topDiscard.moveTo((boundsX / 10) + 650, boundsY - 25)
        topDiscard.draw(window)

    if drawnCard != -3:
        cardDrawn = Card(drawnCard)
        cardDrawn.moveTo((boundsX / 10) + 755, boundsY - 25)
        cardDrawn.draw(window)

    deck = Card(None)
    deck.moveTo((boundsX / 10) + 860, boundsY - 25)
    deck.draw(window)

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()

        if currentPlayer == 1:
            for card in playerOneGameCards:
                if card.getRect().collidepoint(mouse_pos):
                    if swapFromDeck is True or swapFromDiscard is True:
                        switchCurrent()
                        discard(playerOneTotal[card.position])
                        swapCard(1, card.position, drawnCard)
                        drawnCard = -3
                        swapFromDeck = False
                        swapFromDiscard = False
                        if lastSwap:
                            roundOver = True

        if currentPlayer == 2:   
            for card in playerTwoGameCards:
                if card.getRect().collidepoint(mouse_pos):
                    if swapFromDeck is True or swapFromDiscard is True:
                        switchCurrent()
                        discard(playerTwoTotal[card.position])
                        swapCard(2, card.position, drawnCard)
                        drawnCard = -3
                        swapFromDeck = False
                        swapFromDiscard = False
                        if lastSwap:
                            roundOver = True

        if deck.getRect().collidepoint(mouse_pos) and swapFromDiscard is False and drawnCard == -3:
            swapFromDeck = True
            drawnCard = drawDeck()
        
        if topDiscard.getRect().collidepoint(mouse_pos) and swapFromDeck is False and drawnCard == -3:
            swapFromDiscard = True
            drawnCard = drawDiscard()

    if isRoundOver():
        lastSwap = True

    if roundOver:
        tallyRoundScore()

    pygame.display.flip()