import random

class Random():
    def __init__(self, oB=0, oS=1, oT=2, pB=3, pS=4, pT=5):
        self.oB = oB
        self.oS = oS
        self.oT = oT
        self.pB = pB
        self.pS = pS
        self.pT = pT

    def getCardChoice(self, gamestate):
        return random.randint(0, 1)

    def getPlacementChoice(self, gamestate):
        return random.randint(0, 11)
    

class Middle():
    def __init__(self, oB=0, oS=1, oT=2, pB=3, pS=4, pT=5):
        self.oB = oB
        self.oS = oS
        self.oT = oT
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
                if drawnCard < card:
                    return i       
            i += 1
        
        i = 0
        for card in board:
            if card is None:
                return i
            i += 1
        
        return 0


class Speed():
    def __init__(self, oB=0, oS=1, oT=2, pB=3, pS=4, pT=5):
        self.oB = oB
        self.oS = oS
        self.oT = oT
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
        

class Smart():
    def __init__(self, oB=0, oS=1, oT=2, pB=3, pS=4, pT=5):
        self.oB = oB
        self.oS = oS
        self.oT = oT
        self.pB = pB
        self.pS = pS
        self.pT = pT

    def getCardChoice(self, gamestate):
        discard = gamestate[6]
        if discard is None:
            return 0
        
        for card in gamestate[self.pB]:
            if card is not None:
                if card > discard:
                    return 1
                
        return 0

    
    def getPlacementChoice(self, gamestate):
        board = gamestate[self.pB]
        noneCount = board.count(None)
        drawnCard = gamestate[7]

        prevMax = -2
        index = 0
        i = 0
        j = 0

        for card in board:
            if card is not None:
                if card > drawnCard:
                    if card > prevMax:
                        prevMax = card
                        index = i
                        j += 1
            i += 1
            
        if j > 0:
            return index
        elif gamestate[self.oS] < gamestate[self.pS] and noneCount == 1:
            sacMax = -2
            index = 0
            i = 0
            j = 0
            if card is not None:
                if card > sacMax:
                    sacMax = card
                    index = i
                    j += 1

            return index
        else:
            i = 0
            for card in board:
                if card is None:
                    return i
                i += 1
            return 11
