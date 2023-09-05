import numpy as np
import random

cards = []
#(4, 5, 6, 7, 0, 1, 2, 3)
player1 = None
player2 = None
player_one = 0
player_two = 0
current_player = 0
lastOut = None
player_one_total = []
player_one_visible = [None] * 12
playerOneCleared = -1
player_two_total = []
player_two_visible = [None] * 12
playerTwoCleared = -1
discardedCards = []

swap_from_deck = False
swap_from_discard = False
drawn_card = -3
last_swap = False
round_over = False
keep_drawn = True

def initialize_bots(p2=None, p1=None):
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
        player_one_total.insert(0, drawDeck())
        player_two_total.insert(0, drawDeck())

    if lastOut is None:
        global current_player
        pos1 = random.randint(0, 11)
        pos2 = random.randint(0, 11)
        while(pos1 == pos2):
            pos2 = random.randint(0, 11)
        player_one_visible[pos1] = player_one_total[pos1]
        player_one_visible[pos2] = player_one_total[pos2]

        pos1 = random.randint(0, 11)
        pos2 = random.randint(0, 11)
        while(pos1 == pos2):
            pos2 = random.randint(0, 11)
        player_two_visible[pos1] = player_two_total[pos1]
        player_two_visible[pos2] = player_two_total[pos2]

        if get_player_score(1) >= get_player_score(2):
            current_player = 1
        else:
            current_player = 2
    else:
        current_player = lastOut


def get_player_score(player):
    total = 0
    if player == 1:
        for ele in player_one_visible:
            if ele is not None:
                total += ele
    else:
        for ele in player_two_visible:
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

def get_round_state():
    if len(discardedCards) == 0:
        topDiscard = None
    else:
        topDiscard = discardedCards[0]
    playerOneScore = get_player_score(1)
    playerTwoScore = get_player_score(2)
    roundState = (player_one_visible, playerOneScore, player_one, playerOneCleared,
                  player_two_visible, playerTwoScore, player_two, playerTwoCleared, topDiscard, drawn_card)
    return roundState


def is_round_over():
    if player_one_total == player_one_visible:
        return 1
    if player_two_total == player_two_visible:
        return 2


def isGameOver():
    gameOver = False
    if (player_one >= 100) or (player_two >= 100):
        gameOver = True

    return gameOver


def swap_card(player, i, value):
    if player == 1:
        player_one_total[i] = value
        player_one_visible[i] = value
    if player == 2:
        player_two_total[i] = value
        player_two_visible[i] = value


def switch_current():
    global current_player

    if current_player == 1:
        checkPlayerColumns(2)
        checkPlayerColumns(1)
        current_player = 2
    elif current_player == 2:
        checkPlayerColumns(1)
        checkPlayerColumns(2)
        current_player = 1


def tally_round_score(running):
    if is_round_over() != 0:
        global player_one
        global player_two
        global player_one_visible
        global player_two_visible
        global playerOneCleared
        global playerTwoCleared

        lastOut = is_round_over()
        playerOneScore = 0
        for card in player_one_total:
            playerOneScore += card if card is not None else 0
        playerTwoScore = 0
        for card in player_two_total:
            playerTwoScore += card if card is not None else 0

        if lastOut == 1 and playerOneScore >= playerTwoScore:
            playerOneScore *= 2
        if lastOut == 2 and playerTwoScore >= playerOneScore:
            playerTwoScore *= 2

        player_one += playerOneScore
        player_two += playerTwoScore
        cards.clear()
        discardedCards.clear()
        player_one_total.clear()
        player_one_visible.clear()
        player_one_visible = [None] * 12
        playerOneCleared = -1
        player_two_total.clear()
        player_two_visible.clear()
        player_two_visible = [None] * 12
        playerTwoCleared = -1

        if running:
            global swap_from_deck
            global swap_from_discard
            global drawn_card
            global last_swap
            global round_over
            global topDiscard
            swap_from_deck = False
            swap_from_discard = False
            drawn_card = -3
            last_swap = False
            round_over = False

        if player_one >= 100 and player_one > player_two:
            return(2)
        elif player_two >= 100 and player_two > player_one:
            return(1)
        elif player_one >= 100 and player_one == player_two:
            return(3)
        else:
            newRound()
            return(0)


def card_choice(choice):
    global swap_from_deck
    global swap_from_discard
    global drawn_card
    if (choice == 0):
        swap_from_deck = True
        drawn_card = drawDeck()
    elif (choice == 1):
        if len(discardedCards) < 0:
            swap_from_discard = True
            drawn_card = drawDiscard()
        else:
            card_choice(0)

def dump_drawn(choice):
    global keep_drawn
    if (choice == 0):
        keep_drawn = False
        discard(drawn_card)
    else:
        keep_drawn = True

def player_one_placement_choice(choice):
    global swap_from_deck
    global swap_from_discard
    global round_over
    global drawn_card
    switch_current()
    discard(player_one_total[choice])
    swap_card(1, choice, drawn_card)
    drawn_card = -3
    swap_from_deck = False
    swap_from_discard = False
    if last_swap:
        round_over = True


def player_two_placement_choice(choice):
    global swap_from_deck
    global swap_from_discard
    global round_over
    global drawn_card
    switch_current()
    discard(player_two_total[choice])
    swap_card(2, choice, drawn_card)
    drawn_card = -3
    swap_from_deck = False
    swap_from_discard = False
    if last_swap:
        round_over = True

def checkPlayerColumns(player):
    global playerOneCleared
    global playerTwoCleared
    global player_one_total
    global player_two_total

    if player == 1 and playerOneCleared == -1:
        i = 0
        for x in range(4):
            card_one = player_one_visible[i]
            card_two = player_one_visible[i + 4]
            card_three = player_one_visible[i + 8]
            if card_one is not None and (card_one == card_two == card_three):
                discard(card_one)
                discard(card_two)
                discard(card_three)
                playerOneCleared = i
                player_one_total[i - 8] = None
                player_one_total[i - 4] = None
                player_one_total[i] = None
                player_one_visible[i - 8] = None
                player_one_visible[i - 4] = None
                player_one_visible[i] = None
                return 1
            i += 1
    
    if player == 2 and playerTwoCleared == -1:
        i = 0
        for x in range(4):
            card_one = player_two_visible[i]
            card_two = player_two_visible[i + 4]
            card_three = player_two_visible[i + 8]
            if card_one is not None and (card_one == card_two == card_three):
                playerTwoCleared = i
                player_two_total[i - 8] = None
                player_two_visible[i - 8] = None
                player_two_total[i - 4] = None
                player_two_visible[i - 4] = None
                player_two_total[i] = None
                player_two_visible[i] = None
                return 1
            i += 1