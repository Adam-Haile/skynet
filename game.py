import numpy as np
import random

cards = []
#(4, 5, 6, 7, 0, 1, 2, 3)
player1 = None
player2 = None
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

swapFromDeck = False
swapFromDiscard = False
drawnCard = -3
lastSwap = False
roundOver = False

def initializeBots(p2=None, p1=None):
    global player1
    global player2
    player1 = p1
    player2 = p2


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

        if playerOne >= 100 and playerOne > playerTwo:
            return(2)
        elif playerTwo >= 100 and playerTwo > playerOne:
            return(1)
        elif playerOne >= 100 and playerOne == playerTwo:
            return(3)
        else:
            newRound()
            return(0)


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
                discard(card_one)
                discard(card_two)
                discard(card_three)
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