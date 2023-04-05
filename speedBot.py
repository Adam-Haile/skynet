class Speed():
    def __init__(self, pB=3, pS=4, pT=5):
        self.pB = pB
        self.pS = pS
        self.pT = pT

    def getCardChoice(self, gamestate):
        discard = gamestate[6]
        if discard == None:
            return 0
        if discard >= 7:
            return 0
        else:
            return 1
    
    def getPlacementChoice(self, gamestate):
        board = gamestate[self.pB]
        drawnCard = gamestate[7]
        i = 0
        for card in board:
            if card is not None:
                if card > 4 and drawnCard < card:
                    return i
            i += 1
            
        i = 0
        for card in board:
            if card is None:
                return i
            i += 1

        return 0
        