import random

class Random():
    def getCardChoice(gamestate):
        return random.randint(0, 1)

    def getPlacementChoice(gamestate):
        return random.randint(0, 11)