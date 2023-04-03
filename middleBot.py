class Middle():
    def getCardChoice(gamestate):
        discard = gamestate[6]
        if discard == None:
            return 0
        if discard >= 7:
            return 0
        else:
            return 1
    
    def getPlacementChoice(gameState):
        board = gameState[3]
        drawnCard = gameState[7]
        i = 0
        for card in board:
            if card is not None:
                if drawnCard < card:
                    return i       
            i += 1
        
        i = 0
        for card in board:
            if card is None:
                return i
            i += 1

