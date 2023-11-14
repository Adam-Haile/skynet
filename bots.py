import random
from random import choice

class Random():
    def __init__(self, opp_board=0, opp_score=1, opp_total=2, opp_cleared=3, per_board=4, per_score=5, per_total=6, per_cleared=7):
        self.opp_board = opp_board
        self.opp_score = opp_score
        self.opp_total = opp_total
        self.opp_cleared = opp_cleared
        self.per_board = per_board
        self.per_score = per_score
        self.per_total = per_total
        self.per_cleared = per_cleared

    def get_card_choice(self, gamestate):
        return 0 if gamestate[8] is None else random.randint(0, 1)
    
    def get_keep_choice(self, gamestate):
        return random.randint(0, 1)

    def get_placement_choice(self, gamestate):
        if gamestate[self.per_cleared] != -1:
            invalid = [gamestate[self.per_cleared], gamestate[self.per_cleared] + 4, gamestate[self.per_cleared] + 8]
            selection = choice([i for i in range(0, 11) if i not in [invalid]])
        else:
            selection = random.randint(0, 11)
        return selection
    
    def discarded(self, discarded):
        pass
    

class Middle():
    def __init__(self, opp_board=0, opp_score=1, opp_total=2, opp_cleared=3, per_board=4, per_score=5, per_total=6, per_cleared=7):
        self.opp_board = opp_board
        self.opp_score = opp_score
        self.opp_total = opp_total
        self.opp_cleared = opp_cleared
        self.per_board = per_board
        self.per_score = per_score
        self.per_total = per_total
        self.per_cleared = per_cleared

    def get_card_choice(self, gamestate):
        discard = gamestate[8]
        if discard is None:
            return 0
        if discard >= 7:
            return 0
        else:
            return 1
    
    def get_keep_choice(self, gamestate):
        drawn = gamestate[9]
        if drawn >= 7:
            return 0
        else:
            return 1
    
    def get_placement_choice(self, gamestate):
        board = gamestate[self.per_board]
        drawnCard = gamestate[9]
        i = 0
        for card in board:
            if gamestate[self.per_cleared] != -1:
                if i != gamestate[self.per_cleared] and i != gamestate[self.per_cleared] + 4 and i != gamestate[self.per_cleared] + 8:
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
            if gamestate[self.per_cleared] != -1:
                if i != gamestate[self.per_cleared] and i != gamestate[self.per_cleared] + 4 and i != gamestate[self.per_cleared] + 8:
                    if card is None:
                        return i
            else:
                 if card is None:
                    return i
            i += 1
        
        return 0
    
    def discarded(self, discarded):
        pass

class Speed():
    def __init__(self, opp_board=0, opp_score=1, opp_total=2, opp_cleared=3, per_board=4, per_score=5, per_total=6, per_cleared=7):
        self.opp_board = opp_board
        self.opp_score = opp_score
        self.opp_total = opp_total
        self.opp_cleared = opp_cleared
        self.per_board = per_board
        self.per_score = per_score
        self.per_total = per_total
        self.per_cleared = per_cleared

    def get_card_choice(self, gamestate):
        discard = gamestate[8]
        if discard is None:
            return 0
        if discard >= 7:
            return 0
        else:
            return 1
        
    def get_keep_choice(self, gamestate):
        drawn = gamestate[9]
        if drawn >= 7:  
            return 0
        else:
            return 1
    
    def get_placement_choice(self, gamestate):
        board = gamestate[self.per_board]
        drawnCard = gamestate[9]
        i = 0
        for card in board:
            if gamestate[self.per_cleared] != -1:
                if i != gamestate[self.per_cleared] and i != gamestate[self.per_cleared] + 4 and i != gamestate[self.per_cleared] + 8:
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
            if gamestate[self.per_cleared] != -1:
                if i != gamestate[self.per_cleared] and i != gamestate[self.per_cleared] + 4 and i != gamestate[self.per_cleared] + 8:
                    if card is None:
                        return i
            else:
                if card is None:
                    return i
            i += 1

        return 0

    def discarded(self, discarded):
        pass
        

class Smart():
    def __init__(self, opp_board=0, opp_score=1, opp_total=2, opp_cleared=3, per_board=4, per_score=5, per_total=6, per_cleared=7):
        self.opp_board = opp_board
        self.opp_score = opp_score
        self.opp_total = opp_total
        self.opp_cleared = opp_cleared
        self.per_board = per_board
        self.per_score = per_score
        self.per_total = per_total
        self.per_cleared = per_cleared

    def get_card_choice(self, gamestate):
        discard = gamestate[8]
        if discard is None:
            return 0
        
        for card in gamestate[self.per_board]:
            if card is not None:
                if card > discard:
                    return 1
        if discard < 4:
            return 1
        return 0
    
    def get_keep_choice(self, gamestate):
        drawn = gamestate[7]
        for card in gamestate[self.per_board]:
            if card is not None:
                if drawn < card and drawn < 7:
                    return 1
        
        return 0

    
    def get_placement_choice(self, gamestate):
        board = gamestate[self.per_board]
        noneCount = board.count(None)
        drawnCard = gamestate[9]

        prevMax = -2
        index = 0
        i = 0
        j = 0

        for card in board:
            if gamestate[self.per_cleared] != -1:
                if i != gamestate[self.per_cleared] and i != gamestate[self.per_cleared] + 4 and i != gamestate[self.per_cleared] + 8:
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
        elif gamestate[self.opp_score] < gamestate[self.per_score] and noneCount == 1:
            sacMax = -2
            index = 0
            i = 0
            j = 0
            for card in board:
                if gamestate[self.per_cleared] != -1:
                    if i != gamestate[self.per_cleared] and i != gamestate[self.per_cleared] + 4 and i != gamestate[self.per_cleared] + 8:
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
                if gamestate[self.per_cleared] != -1:
                    if i != gamestate[self.per_cleared] and i != gamestate[self.per_cleared] + 4 and i != gamestate[self.per_cleared] + 8:
                        if card is None:
                            return i
                else:
                    if card is None:
                        return i
                i += 1
            return 11
        
    def discarded(self, discarded):
        pass
        
class Triple():
    def __init__(self, opp_board=0, opp_score=1, opp_total=2, opp_cleared=3, per_board=4, per_score=5, per_total=6, per_cleared=7):
        self.opp_board = opp_board
        self.opp_score = opp_score
        self.opp_total = opp_total
        self.opp_cleared = opp_cleared
        self.per_board = per_board
        self.per_score = per_score
        self.per_total = per_total
        self.per_cleared = per_cleared

    def get_card_choice(self, gamestate):
        discard = gamestate[8]
        if discard is None:
            return 0
        if discard >= 7:
            return 0
        elif discard in gamestate[self.per_board] and gamestate[self.per_cleared] == 0:
            return 0
        else:
            return 1
        
    def get_keep_choice(self, gamestate):
        drawn = gamestate[7]
        if drawn in gamestate[self.per_board]:
            return 1
        elif drawn >= 7:
            return 0
        else:
            return 1
        
    def get_placement_choice(self, gamestate):
        board = gamestate[self.per_board]
        drawnCard = gamestate[9]
        i = 0

        if gamestate[self.per_cleared] == -1:
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
            if gamestate[self.per_cleared] != -1:
                if i != gamestate[self.per_cleared] and i != gamestate[self.per_cleared] + 4 and i != gamestate[self.per_cleared] + 8:
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
            if gamestate[self.per_cleared] != -1:
                if i != gamestate[self.per_cleared] and i != gamestate[self.per_cleared] + 4 and i != gamestate[self.per_cleared] + 8:
                    if card is None:
                        return i
            else:
                if card is None:
                    return i
            i += 1

        return 0
    
    def discarded(self, discarded):
        pass
    

class Counter():
    def __init__(self, opp_board=0, opp_score=1, opp_total=2, opp_cleared=3, per_board=4, per_score=5, per_total=6, per_cleared=7):
        self.opp_board = opp_board
        self.opp_score = opp_score
        self.opp_total = opp_total
        self.opp_cleared = opp_cleared
        self.per_board = per_board
        self.per_score = per_score
        self.per_total = per_total
        self.per_cleared = per_cleared
        self.deck = {}
        self.discard = []
        self._reset_deck()

    def get_card_choice(self, gamestate):
        if gamestate[8] is not None:
            self.discard.append(gamestate[8])
            self._reset_deck()
            for card in self.opp_board:
                if card is not None:
                    self.deck[card] -= 1
            for card in self.per_board:
                if card is not None:
                    self.deck[card] -= 1
            for card in self.discard:
                self.deck[card] -= 1

            deck_sum = sum(self.deck.values())
            if deck_sum < 0:
                return 0
            else:
                seven_or_greater_sum = sum([self.deck[i] for i in range(7, 13)])
                less_than_seven_sum = sum([self.deck[i] for i in range(-2, 7)])
                if seven_or_greater_sum > less_than_seven_sum:
                    return 1
                else:
                    return 0
        else:
            return 0   
        
    def get_keep_choice(self, gamestate):
        drawn = gamestate[7]
        greater_than_drawn = sum([self.deck[i] for i in range(drawn, 13)])
        less_than_drawn = sum([self.deck[i] for i in range(-2, drawn)])
        if greater_than_drawn > less_than_drawn:
            return 1
        else:
            return 0
        
    def get_placement_choice(self, gamestate):
        board = gamestate[self.per_board]
        drawnCard = gamestate[9]
        i = 0
        for card in board:
            if gamestate[self.per_cleared] != -1:
                if i != gamestate[self.per_cleared] and i != gamestate[self.per_cleared] + 4 and i != gamestate[self.per_cleared] + 8:
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
            if gamestate[self.per_cleared] != -1:
                if i != gamestate[self.per_cleared] and i != gamestate[self.per_cleared] + 4 and i != gamestate[self.per_cleared] + 8:
                    if card is None:
                        return i
            else:
                 if card is None:
                    return i
            i += 1
        
        return 0

    def discarded(self, discarded):
        self.discard.append(discarded)
         

    def _reset_deck(self):
        for i in range(-2, 13):
            if i == -2:
                self.deck[i] = 5
            elif i == -1 or i != 0:
                self.deck[i] = 10
            elif i == 0:
                self.deck[i] = 15