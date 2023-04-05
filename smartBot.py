class Smart():
    def __init__(self, pB=3, pS=4, pT=5):
        self.pB = pB
        self.pS = pS
        self.pT = pT

    def getCardChoice(self, gamestate):
        discard = gamestate[6]
        if discard is not None:
            for card in gamestate[self.pB]:
                if card is not None:
                    if discard < card and discard < 9:
                        return 1
        return 0

    
    def getPlacementChoice(self, gamestate):
        board = gamestate[self.pB]
        drawnCard = gamestate[7]
        max = -2
        i = 0
        j = 0
        for card in board:
            if card is not None:
                if drawnCard < card and card > max:
                    max = card
                    i = j
            j += 1

        if(max != -2 and i != 0):
            return i

        i = 0
        for card in board:
            if card is None:
                return i
            i += 1
