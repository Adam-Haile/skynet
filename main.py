import game as g
import pygame
import bots
import random
import time

twoBot = False

def randomBot():
    rand = bots.Random()
    mid = bots.Middle()
    speed = bots.Speed()
    smart = bots.Smart()
    triple = bots.Triple()
    if twoBot:
        for i in range(2):
            bot = random.randint(0, 4)
            if bot == 0:
                if i == 0:
                    g.player1 = bots.Random(4, 5, 6, 7, 0, 1, 2, 3)
                    print("Bot is RandomBot")
                else:
                    g.player2 = rand
                    print("Bot is RandomBot")
            elif bot == 1:
                if i == 0:
                    g.player1 = bots.Middle(4, 5, 6, 7, 0, 1, 2, 3)
                    print("Bot is MiddleBot")
                else:
                    g.player2 = mid
                    print("Bot is MiddleBot")
            elif bot == 2:
                if i == 0:
                    g.player1 = bots.Speed(4, 5, 6, 7, 0, 1, 2, 3)
                    print("Bot is SpeedBot")
                else:
                    g.player2 = speed
                    print("Bot is SpeedBot")
            elif bot == 3:
                if i == 0:
                    g.player1 = bots.Smart(4, 5, 6, 7, 0, 1, 2, 3)
                    print("Bot is SmartBot")
                else:
                    g.player2 = smart
                    print("Bot is SmartBot")
            else:
                if i == 0:
                    g.player1 = bots.Triple(4, 5, 6, 7, 0, 1, 2, 3)
                    print("Bot is TripleBot")
                else:
                    g.player2 = triple
                    print("Bot is TripleBot")
    else:
        bot = random.randint(0, 4)
        if bot == 0:
            g.player2 = rand
            print("Bot is RandomBot")
        elif bot == 1:
            g.player2 = mid
            print("Bot is MiddleBot")
        elif bot == 2:
            g.player2 = speed
            print("Bot is SpeedBot")
        elif bot == 3:
            g.player2 = smart
            print("Bot is SmartBot")
        else:
            g.player2 = triple
            print("Bot is TripleBot")

g.initializeBots(bots.Smart())
g.newRound()

running = True

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


while running:
    playerOneGameCards = []
    playerTwoGameCards = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((95, 141, 186))
    i = 0

    p1 = None
    p2 = None
    if g.getPlayerScore(1) < g.getPlayerScore(2):
        p1 = GREEN
        p2 = RED
    elif g.getPlayerScore(2) < g.getPlayerScore(1):
        p1 = RED
        p2 = GREEN
    else:
        p1 = YELLOW
        p2 = YELLOW

    text = skyfont.render("Current Player: " +
                            str(g.currentPlayer), True, (255, 255, 255))
    window.blit(text, [boundsX/2 - 125, boundsY - 75,
                text.get_rect().width, text.get_rect().height])

    text = smallfont.render(
        "Total Player Score: " + str(g.playerOne), True, (255, 255, 255))
    window.blit(text, [boundsX/20, card_height/2 - 35,
                text.get_rect().width, text.get_rect().height])

    text = skyfont.render(
        "Player Score: " + str(g.getPlayerScore(1)), True, p1)
    window.blit(text, [boundsX/20, card_height/2 - 15,
                text.get_rect().width, text.get_rect().height])

    text = smallfont.render(
        "Total Player Score: " + str(g.playerTwo), True, (255, 255, 255))
    window.blit(text, [boundsX/20 + 500, card_height/2 -
                35, text.get_rect().width, text.get_rect().height])

    text = skyfont.render(
        "Player Score: " + str(g.getPlayerScore(2)), True, p2)
    window.blit(text, [boundsX/20 + 500, card_height/2 -
                15, text.get_rect().width, text.get_rect().height])

    for y in range(3):
        for x in range(4):
            if g.playerOneTotal[i] is not None:
                newCard = Card(g.playerOneVisible[i], i)
                newCard.moveTo((boundsX / 10) + (x * 105), (boundsY / 4) + (y * 200) - 25)
                newCard.draw(window)
                playerOneGameCards.append(newCard)

            if g.playerTwoTotal[i] is not None:
                newCard = Card(g.playerTwoVisible[i], i)
                newCard.moveTo((boundsX / 10) + (x * 105) + 500, (boundsY / 4) + (y * 200) - 25)
                newCard.draw(window)
                playerTwoGameCards.append(newCard)

            i += 1

    if len(g.discardedCards) > 0:
        topDiscard = Card(g.discardedCards[0])
        topDiscard.moveTo((boundsX / 10) + 650, boundsY - 35)
        topDiscard.draw(window)

    if g.drawnCard != -3:
        cardDrawn = Card(g.drawnCard)
        cardDrawn.moveTo((boundsX / 10) + 755, boundsY - 35)
        cardDrawn.draw(window)

    deck = Card(None)
    deck.moveTo((boundsX / 10) + 860, boundsY - 35)
    deck.draw(window)

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()

        if g.currentPlayer == 1:
            for card in playerOneGameCards:
                if card.getRect().collidepoint(mouse_pos):
                    if g.swapFromDeck is True or g.swapFromDiscard is True:
                        g.switchCurrent()
                        g.discard(g.playerOneTotal[card.position])
                        g.swapCard(1, card.position, g.drawnCard)
                        g.drawnCard = -3
                        g.swapFromDeck = False
                        g.swapFromDiscard = False
                        if g.lastSwap:
                            g.roundOver = True

        if g.currentPlayer == 2:
            for card in playerTwoGameCards:
                if card.getRect().collidepoint(mouse_pos):
                    if g.swapFromDeck is True or g.swapFromDiscard is True:
                        g.switchCurrent()
                        g.discard(g.playerTwoTotal[card.position])
                        g.swapCard(2, card.position, g.drawnCard)
                        g.drawnCard = -3
                        g.swapFromDeck = False
                        g.swapFromDiscard = False
                        if g.lastSwap:
                            g.roundOver = True

        if deck.getRect().collidepoint(mouse_pos) and g.swapFromDiscard is False and g.drawnCard == -3:
            g.swapFromDeck = True
            g.drawnCard = g.drawDeck()

        if topDiscard.getRect().collidepoint(mouse_pos) and g.swapFromDeck is False and g.drawnCard == -3:
            g.swapFromDiscard = True
            g.drawnCard = g.drawDiscard()

    if g.isRoundOver():
        g.lastSwap = True

    if g.roundOver:
        result = g.tallyRoundScore()
        if result == 1:
            print("Player 1 Wins!")
        elif result == 2:
            print("Player 2 Wins!")
        elif result == 3:
            print("Players tied!")

    if g.currentPlayer == 1 and g.player1 is not None:
        g.cardChoice(g.player1.getCardChoice(g.getRoundState()))
        g.playerOnePlacementChoice(g.player1.getPlacementChoice(g.getRoundState()))
    if g.currentPlayer == 2 and g.player2 is not None:
        c = g.player2.getCardChoice(g.getRoundState())
        # print(c)
        g.cardChoice(c)
        c = g.player2.getPlacementChoice(g.getRoundState())
        # print(c)
        g.playerTwoPlacementChoice(c)

    pygame.display.flip()
    if twoBot:
        time.sleep(0.25)
