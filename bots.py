import random

class Random():
    def __init__(self, oB=0, oS=1, oT=2, oC=3, pB=4, pS=5, pT=6, pC=7):
        self.oB = oB
        self.oS = oS
        self.oT = oT
        self.oC = oC
        self.pB = pB
        self.pS = pS
        self.pT = pT
        self.pC = pC

    def getCardChoice(self, gamestate):
        return random.randint(0, 1)

    def getPlacementChoice(self, gamestate):
        choice = random.randint(0, 11)
        if gamestate[self.pC] != -1:
            while choice == gamestate[self.pC] or gamestate[self.pC] + 4 or gamestate[self.pC] + 8:
                choice = random.randint(0, 11)
        return choice
    

class Middle():
    def __init__(self, oB=0, oS=1, oT=2, oC=3, pB=4, pS=5, pT=6, pC=7):
        self.oB = oB
        self.oS = oS
        self.oT = oT
        self.oC = oC
        self.pB = pB
        self.pS = pS
        self.pT = pT
        self.pC = pC

    def getCardChoice(self, gamestate):
        discard = gamestate[8]
        if discard == None:
            return 0
        if discard >= 7:
            return 0
        else:
            return 1
    
    def getPlacementChoice(self, gamestate):
        board = gamestate[self.pB]
        drawnCard = gamestate[9]
        i = 0
        for card in board:
            if gamestate[self.pC] != -1:
                if i != gamestate[self.pC] and i != gamestate[self.pC] + 4 and i != gamestate[self.pC] + 8:
                    if card is not None:
                        if drawnCard < card:
                            return i       
            else:
                if card is not None:
                    if drawnCard < card:
                        return i    
            i += 1
        
        i = 0
        for card in board:
            if gamestate[self.pC] != -1:
                if i != gamestate[self.pC] and i != gamestate[self.pC] + 4 and i != gamestate[self.pC] + 8:
                    if card is None:
                        return i
            else:
                 if card is None:
                    return i
            i += 1
        
        return 0


class Speed():
    def __init__(self, oB=0, oS=1, oT=2, oC=3, pB=4, pS=5, pT=6, pC=7):
        self.oB = oB
        self.oS = oS
        self.oT = oT
        self.oC = oC
        self.pB = pB
        self.pS = pS
        self.pT = pT
        self.pC = pC

    def getCardChoice(self, gamestate):
        discard = gamestate[8]
        if discard == None:
            return 0
        if discard >= 7:
            return 0
        else:
            return 1
    
    def getPlacementChoice(self, gamestate):
        board = gamestate[self.pB]
        drawnCard = gamestate[9]
        i = 0
        for card in board:
            if gamestate[self.pC] != -1:
                if i != gamestate[self.pC] and i != gamestate[self.pC] + 4 and i != gamestate[self.pC] + 8:
                    if card is not None:
                        if card > 4 and drawnCard < card:
                            return i
            else:
                if card is not None:
                    if card > 4 and drawnCard < card:
                        return i
            i += 1
            
        i = 0
        for card in board:
            if gamestate[self.pC] != -1:
                if i != gamestate[self.pC] and i != gamestate[self.pC] + 4 and i != gamestate[self.pC] + 8:
                    if card is None:
                        return i
            else:
                if card is None:
                    return i
            i += 1

        return 0
        

class Smart():
    def __init__(self, oB=0, oS=1, oT=2, oC=3, pB=4, pS=5, pT=6, pC=7):
        self.oB = oB
        self.oS = oS
        self.oT = oT
        self.oC = oC
        self.pB = pB
        self.pS = pS
        self.pT = pT
        self.pC = pC

    def getCardChoice(self, gamestate):
        discard = gamestate[8]
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
        drawnCard = gamestate[9]

        prevMax = -2
        index = 0
        i = 0
        j = 0

        for card in board:
            if gamestate[self.pC] != -1:
                if i != gamestate[self.pC] and i != gamestate[self.pC] + 4 and i != gamestate[self.pC] + 8:
                    if card is not None:
                        if card > drawnCard:
                            if card > prevMax:
                                prevMax = card
                                index = i
                                j += 1
            else:
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
            for card in board:
                if gamestate[self.pC] != -1:
                    if i != gamestate[self.pC] and i != gamestate[self.pC] + 4 and i != gamestate[self.pC] + 8:
                        if card is not None:
                            if card > sacMax:
                                sacMax = card
                                index = i
                                j += 1
                else:
                    if card is not None:
                        if card > sacMax:
                            sacMax = card
                            index = i
                            j += 1

            return index
        else:
            i = 0
            for card in board:
                if gamestate[self.pC] != -1:
                    if i != gamestate[self.pC] and i != gamestate[self.pC] + 4 and i != gamestate[self.pC] + 8:
                        if card is None:
                            return i
                else:
                    if card is None:
                        return i
                i += 1
            return 11
        
class Triple():
    def __init__(self, oB=0, oS=1, oT=2, oC=3, pB=4, pS=5, pT=6, pC=7):
        self.oB = oB
        self.oS = oS
        self.oT = oT
        self.oC = oC
        self.pB = pB
        self.pS = pS
        self.pT = pT
        self.pC = pC

    def getCardChoice(self, gamestate):
        discard = gamestate[8]
        if discard == None:
            return 0
        if discard >= 7:
            return 0
        elif discard in gamestate[self.pB] and gamestate[self.pC] == 0:
            return 0
        else:
            return 1
        
    def getPlacementChoice(self, gamestate):
        board = gamestate[self.pB]
        drawnCard = gamestate[9]
        i = 0

        if gamestate[self.pC] == -1:
            for card in board:
                if card is not None:
                    if card == drawnCard:
                        j = i
                        while j + 4 < len(board):
                            j += 4
                            if board[j] != drawnCard:
                                return j
                        j = i
                        while j - 4 > 0:
                            j -= 4
                            if board[j] != drawnCard:
                                return j
                i += 1

        i = 0
        for card in board:
            if gamestate[self.pC] != -1:
                if i != gamestate[self.pC] and i != gamestate[self.pC] + 4 and i != gamestate[self.pC] + 8:
                    if card is not None:
                        if card > 4 and drawnCard < card:
                            return i
            else:
                if card is not None:
                    if card > 4 and drawnCard < card:
                        return i
            i += 1
            
        i = 0
        for card in board:
            if gamestate[self.pC] != -1:
                if i != gamestate[self.pC] and i != gamestate[self.pC] + 4 and i != gamestate[self.pC] + 8:
                    if card is None:
                        return i
            else:
                if card is None:
                    return i
            i += 1

        return 0
