import pygame
import numpy as np
import random
import bots
import time

cards = []
#(4, 5, 6, 7, 0, 1, 2, 3)
player1 = None
player2 = bots.Triple()
playerOne = 0
playerTwo = 0
currentPlayer = 0
lastWinner = None
playerOneTotal = []
playerOneVisible = [None] * 12
playerOneCleared = -1
playerTwoTotal = []
playerTwoVisible = [None] * 12
playerTwoCleared = -1
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

    pos1 = random.randint(0, 11)
    pos2 = random.randint(0, 11)
    while(pos1 == pos2):
        pos2 = random.randint(0, 11)
    playerOneVisible[pos1] = playerOneTotal[pos1]
    playerOneVisible[pos2] = playerOneTotal[pos2]

    pos1 = random.randint(0, 11)
    pos2 = random.randint(0, 11)
    while(pos1 == pos2):
        pos2 = random.randint(0, 11)
    playerTwoVisible[pos1] = playerTwoTotal[pos1]
    playerTwoVisible[pos2] = playerTwoTotal[pos2]

    if lastWinner is None:
        global currentPlayer
        if getPlayerScore(1) >= getPlayerScore(2):
            currentPlayer = 1
        else:
            currentPlayer = 2
    else:
        currentPlayer = lastWinner


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
        for i in range(1, len(discardedCards)):
            cards.append(discardedCards[i])
        discardedCards.clear()
        discardedCards.append(topCard)
        shuffle()

    return cards.pop()


def drawDiscard():
    return discardedCards.pop(0)


def discard(card):
    discardedCards.insert(0, card)

swapFromDeck = False
swapFromDiscard = False
drawnCard = -3
lastSwap = False
roundOver = False

def getRoundState():
    if len(discardedCards) == 0:
        topDiscard = None
    else:
        topDiscard = discardedCards[0]
    playerOneScore = getPlayerScore(1)
    playerTwoScore = getPlayerScore(2)
    roundState = (playerOneVisible, playerOneScore, playerOne, playerOneCleared,
                  playerTwoVisible, playerTwoScore, playerTwo, playerTwoCleared, topDiscard, drawnCard)
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
        checkPlayerColumns(2)
        checkPlayerColumns(1)
        currentPlayer = 2
    elif currentPlayer == 2:
        checkPlayerColumns(1)
        checkPlayerColumns(2)
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
            self.image.blit(
                text, [7.5, card_height/2 - 15, text.get_rect().width, text.get_rect().height])
        else:
            text = font.render(str(value).capitalize(), True, self.color)
            if len(str(value)) == 2:
                self.image.blit(text, [card_width/2 - 27, card_height /
                                2 - 25, text.get_rect().width, text.get_rect().height])
            if len(str(value)) == 1:
                self.image.blit(text, [card_width/2 - 15, card_height /
                                2 - 25, text.get_rect().width, text.get_rect().height])

    def moveTo(self, x, y):
        self.rect.x = (x - card_width / 2)
        self.rect.y = (y - card_height / 2)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def getRect(self):
        return self.rect

topDiscard = Card(None)

def tallyRoundScore():
    if isRoundOver() != 0:
        global running
        global playerOne
        global playerTwo
        global playerOneVisible
        global playerTwoVisible
        global playerOneCleared
        global playerTwoCleared

        lastWinner = isRoundOver()
        playerOneScore = 0
        for card in playerOneTotal:
            playerOneScore += card if card is not None else 0
        playerTwoScore = 0
        for card in playerTwoTotal:
            playerTwoScore += card if card is not None else 0

        if lastWinner == 1 and playerOneScore >= playerTwoScore:
            playerOneScore *= 2
        if lastWinner == 2 and playerTwoScore >= playerOneScore:
            playerTwoScore *= 2

        playerOne += playerOneScore
        playerTwo += playerTwoScore
        cards.clear()
        discardedCards.clear()
        playerOneTotal.clear()
        playerOneVisible.clear()
        playerOneVisible = [None] * 12
        playerOneCleared = -1
        playerTwoTotal.clear()
        playerTwoVisible.clear()
        playerTwoVisible = [None] * 12
        playerTwoCleared = -1

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

        if playerOne >= 100 and playerOne > playerTwo:
            print("Player 2 wins!")
            exit()
        elif playerTwo >= 100 and playerTwo > playerOne:
            print("Player 1 wins!")
            exit()
        elif playerOne >= 100 and playerOne == playerTwo:
            print("Game tied!")
            exit()
        else:
            newRound()
        # newRound()


def cardChoice(choice):
    global swapFromDeck
    global swapFromDiscard
    global drawnCard
    if (choice == 0):
        swapFromDeck = True
        drawnCard = drawDeck()
    elif (choice == 1):
        if len(discardedCards) < 0:
            swapFromDiscard = True
            drawnCard = drawDiscard()
        else:
            cardChoice(0)


def playerOnePlacementChoice(choice):
    global swapFromDeck
    global swapFromDiscard
    global roundOver
    global drawnCard
    switchCurrent()
    discard(playerOneTotal[choice])
    swapCard(1, choice, drawnCard)
    drawnCard = -3
    swapFromDeck = False
    swapFromDiscard = False
    if lastSwap:
        roundOver = True


def playerTwoPlacementChoice(choice):
    global swapFromDeck
    global swapFromDiscard
    global roundOver
    global drawnCard
    switchCurrent()
    discard(playerTwoTotal[choice])
    swapCard(2, choice, drawnCard)
    drawnCard = -3
    swapFromDeck = False
    swapFromDiscard = False
    if lastSwap:
        roundOver = True

def checkPlayerColumns(player):
    global playerOneCleared
    global playerTwoCleared
    global playerOneTotal
    global playerTwoTotal

    if player == 1 and playerOneCleared == -1:
        i = 0
        for x in range(4):
            card_one = playerOneVisible[i]
            card_two = playerOneVisible[i + 4]
            card_three = playerOneVisible[i + 8]
            if card_one is not None and (card_one == card_two == card_three):
                playerOneCleared = i
                playerOneTotal[i - 8] = None
                playerOneTotal[i - 4] = None
                playerOneTotal[i] = None
                playerOneVisible[i - 8] = None
                playerOneVisible[i - 4] = None
                playerOneVisible[i] = None
                return 1
            i += 1
    
    if player == 2 and playerTwoCleared == -1:
        i = 0
        for x in range(4):
            card_one = playerTwoVisible[i]
            card_two = playerTwoVisible[i + 4]
            card_three = playerTwoVisible[i + 8]
            if card_one is not None and (card_one == card_two == card_three):
                playerTwoCleared = i
                playerTwoTotal[i - 8] = None
                playerTwoVisible[i - 8] = None
                playerTwoTotal[i - 4] = None
                playerTwoVisible[i - 4] = None
                playerTwoTotal[i] = None
                playerTwoVisible[i] = None
                return 1
            i += 1

playGame = True

while playGame:
    playerOneGameCards = []
    playerTwoGameCards = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playGame = False

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

    text = skyfont.render("Current Player: " +
                            str(currentPlayer), True, (255, 255, 255))
    window.blit(text, [boundsX/2 - 125, boundsY - 75,
                text.get_rect().width, text.get_rect().height])

    text = smallfont.render(
        "Total Player Score: " + str(playerOne), True, (255, 255, 255))
    window.blit(text, [boundsX/20, card_height/2 - 35,
                text.get_rect().width, text.get_rect().height])

    text = skyfont.render(
        "Player Score: " + str(getPlayerScore(1)), True, p1)
    window.blit(text, [boundsX/20, card_height/2 - 15,
                text.get_rect().width, text.get_rect().height])

    text = smallfont.render(
        "Total Player Score: " + str(playerTwo), True, (255, 255, 255))
    window.blit(text, [boundsX/20 + 500, card_height/2 -
                35, text.get_rect().width, text.get_rect().height])

    text = skyfont.render(
        "Player Score: " + str(getPlayerScore(2)), True, p2)
    window.blit(text, [boundsX/20 + 500, card_height/2 -
                15, text.get_rect().width, text.get_rect().height])

    for y in range(3):
        for x in range(4):
            if playerOneTotal[i] is not None:
                newCard = Card(playerOneVisible[i], i)
                newCard.moveTo((boundsX / 10) + (x * 105), (boundsY / 4) + (y * 200) - 25)
                newCard.draw(window)
                playerOneGameCards.append(newCard)

            if playerTwoTotal[i] is not None:
                newCard = Card(playerTwoVisible[i], i)
                newCard.moveTo((boundsX / 10) + (x * 105) + 500, (boundsY / 4) + (y * 200) - 25)
                newCard.draw(window)
                playerTwoGameCards.append(newCard)

            i += 1

    if len(discardedCards) > 0:
        topDiscard = Card(discardedCards[0])
        topDiscard.moveTo((boundsX / 10) + 650, boundsY - 35)
        topDiscard.draw(window)

    if drawnCard != -3:
        cardDrawn = Card(drawnCard)
        cardDrawn.moveTo((boundsX / 10) + 755, boundsY - 35)
        cardDrawn.draw(window)

    deck = Card(None)
    deck.moveTo((boundsX / 10) + 860, boundsY - 35)
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

    if currentPlayer == 1 and player1 is not None:
        cardChoice(player1.getCardChoice(getRoundState()))
        playerOnePlacementChoice(player1.getPlacementChoice(getRoundState()))
    if currentPlayer == 2 and player2 is not None:
        c = player2.getCardChoice(getRoundState())
        # print(c)
        cardChoice(c)
        c = player2.getPlacementChoice(getRoundState())
        # print(c)
        playerTwoPlacementChoice(c)

    pygame.display.flip()
    time.sleep(0.25)
