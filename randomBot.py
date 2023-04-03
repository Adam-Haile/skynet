import random

class Random():
    def getCardChoice(self, gamestate):
        return random.randint(0, 1)

    def getPlacementChoice(self, gamestate):
        return random.randint(0, 11)