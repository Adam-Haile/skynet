class Speed():
    def getCardChoice(self, gamestate):
        discard = gamestate[6]
        if discard == None:
            return 0
        if discard >= 7:
            return 0
        else:
            return 1
    
    def getPlacementChoice(self, gamestate):
        board = gamestate[3]
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
        