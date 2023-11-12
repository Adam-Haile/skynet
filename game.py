import numpy as np
import random

class Skyjo():
    def __init__(self, p1=None, p2=None):
        self.cards = []
        #(4, 5, 6, 7, 0, 1, 2, 3)
        self.player1 = p1
        self.player2 = p2
        self.player_one = 0
        self.player_two = 0
        self.current_player = 0
        self.last_out = None
        self.player_one_total = []
        self.player_one_visible = [None] * 12
        self.player_one_cleared = -1
        self.player_two_total = []
        self.player_two_visible = [None] * 12
        self.player_two_cleared = -1
        self.discarded_cards = []

        self.swap_from_deck = False
        self.swap_from_discard = False
        self.drawn_card = -3
        self.last_swap = False
        self.round_over = False
        self.keep_drawn = True

        self.current_action = 0

    def reset(self):
        new_game = Skyjo(self.player1, self.player2)
        new_game.new_round()
        return new_game

    def step(self, action):
        if self.current_action == 0:
            action = round(action / 12)
            self.card_choice(action)
            self.current_action = 1
        elif self.current_action == 1:
            action = round(action / 12)
            self.dump_drawn(action)
            self.current_action = 2
        elif self.current_action == 2:
            if self.current_player == 1:
                self.player_one_placement_choice(action)
            else:
                self.player_two_placement_choice(action)
            self.current_action = 0

    def get_observation(self):
        state = self.get_round_state()
        full_state = []
        for i in state[0]:
            full_state.append(i)
        for j in state[4]:
            full_state.append(i)
        full_state.append(state[8])
        full_state.append(state[9])
        return full_state
    
    def get_reward(self):
        if self.is_game_over():
            if self.player_one > self.player_two:
                return 1
            elif self.player_two > self.player_one:
                return -1
        return 0

    def initialize_bots(self, p2=None, p1=None):
        self.player1 = p1
        self.player2 = p2

    def new_round(self):
        for i in range(5):
            self.cards.append(-2)
        for i in range(10):
            self.cards.append(-1)
            self.cards.extend(range(1, 13))
        for i in range(15):
            self.cards.append(0)
        self.shuffle()

        for i in range(12):
            self.player_one_total.insert(0, self.draw_deck())
            self.player_two_total.insert(0, self.draw_deck())

        if self.last_out is None:
            pos1 = random.randint(0, 11)
            pos2 = random.randint(0, 11)
            while(pos1 == pos2):
                pos2 = random.randint(0, 11)
            self.player_one_visible[pos1] = self.player_one_total[pos1]
            self.player_one_visible[pos2] = self.player_one_total[pos2]

            pos1 = random.randint(0, 11)
            pos2 = random.randint(0, 11)
            while(pos1 == pos2):
                pos2 = random.randint(0, 11)
            self.player_two_visible[pos1] = self.player_two_total[pos1]
            self.player_two_visible[pos2] = self.player_two_total[pos2]

            if self.get_player_score(1) >= self.get_player_score(2):
                self.current_player = 1
            else:
                self.current_player = 2
        else:
            self.current_player = self.last_out


    def get_player_score(self, player):
        total = 0
        if player == 1:
            for ele in self.player_one_visible:
                if ele is not None:
                    total += ele
        else:
            for ele in self.player_two_visible:
                if ele is not None:
                    total += ele
        return total


    def shuffle(self):
        np.random.shuffle(self.cards)


    def draw_deck(self):
        if len(self.cards) == 0:
            top_card = self.discarded_cards.pop()
            for _ in range(len(self.discarded_cards)):
                self.cards.append(self.discarded_cards.pop())
            self.discarded_cards.clear()
            self.discarded_cards.append(top_card)
            self.shuffle()

        return self.cards.pop()


    def draw_discard(self):
        return self.discarded_cards.pop(0)


    def discard(self, card):
        self.discarded_cards.insert(0, card)

    def get_round_state(self):
        if len(self.discarded_cards) == 0:
            top_discard = None
        else:
            top_discard = self.discarded_cards[0]
        player_one_score = self.get_player_score(1)
        player_two_score = self.get_player_score(2)
        round_state = (self.player_one_visible, player_one_score, self.player_one, self.player_one_cleared,
                    self.player_two_visible, player_two_score, self.player_two, self.player_two_cleared, top_discard, self.drawn_card)
        return round_state


    def is_round_over(self):
        if self.player_one_total == self.player_one_visible:
            return 1
        if self.player_two_total == self.player_two_visible:
            return 2


    def is_game_over(self):
        return (self.player_one >= 100) or (self.player_two >= 100)


    def swap_card(self, player, i, value):
        if player == 1:
            self.player_one_total[i] = value
            self.player_one_visible[i] = value
        if player == 2:
            self.player_two_total[i] = value
            self.player_two_visible[i] = value


    def switch_current(self):
        if self.current_player == 1:
            self.check_player_columns(2)
            self.check_player_columns(1)
            self.current_player = 2
        elif self.current_player == 2:
            self.check_player_columns(1)
            self.check_player_columns(2)
            self.current_player = 1


    def tally_round_score(self, running):
        if self.is_round_over() != 0:
            last_out = self.is_round_over()
            player_one_score = 0
            for card in self.player_one_total:
                player_one_score += card if card is not None else 0
            player_two_score = 0
            for card in self.player_two_total:
                player_two_score += card if card is not None else 0

            if last_out == 1 and player_one_score >= player_two_score:
                player_one_score *= 2
            if last_out == 2 and player_two_score >= player_one_score:
                player_two_score *= 2

            self.player_one += player_one_score
            self.player_two += player_two_score
            self.cards.clear()
            self.discarded_cards.clear()
            self.player_one_total.clear()
            self.player_one_visible.clear()
            self.player_one_visible = [None] * 12
            self.player_one_cleared = -1
            self.player_two_total.clear()
            self.player_two_visible.clear()
            self.player_two_visible = [None] * 12
            self.player_two_cleared = -1

            if running:
                self.swap_from_deck = False
                self.swap_from_discard = False
                self.drawn_card = -3
                self.last_swap = False
                self.round_over = False

            if self.player_one >= 100 and self.player_one > self.player_two:
                return(2)
            elif self.player_two >= 100 and self.player_two > self.player_one:
                return(1)
            elif self.player_one >= 100 and self.player_one == self.player_two:
                return(3)
            else:
                self.new_round()
                return(0)


    def card_choice(self, choice):
        if (choice == 0):
            self.swap_from_deck = True
            self.drawn_card = self.draw_deck()
        elif (choice == 1):
            if len(self.discarded_cards) < 0:
                self.swap_from_discard = True
                self.drawn_card = self.draw_discard()
            else:
                self.card_choice(0)

    def dump_drawn(self, choice):
        if (choice == 0):
            self.keep_drawn = False
            self.discard(self.drawn_card)
        else:
            self.keep_drawn = True

    def player_one_placement_choice(self, choice):
        self.switch_current()
        self.discard(self.player_one_total[choice])
        self.swap_card(1, choice, self.drawn_card)
        self.drawn_card = -3
        self.swap_from_deck = False
        self.swap_from_discard = False
        if self.last_swap:
            self.round_over = True


    def player_two_placement_choice(self, choice):
        self.switch_current()
        self.discard(self.player_two_total[choice])
        self.swap_card(2, choice, self.drawn_card)
        self.drawn_card = -3
        self.swap_from_deck = False
        self.swap_from_discard = False
        if self.last_swap:
            self.round_over = True

    def check_player_columns(self, player):
        if player == 1 and self.player_one_cleared == -1:
            i = 0
            for x in range(4):
                card_one = self.player_one_visible[i]
                card_two = self.player_one_visible[i + 4]
                card_three = self.player_one_visible[i + 8]
                if card_one is not None and (card_one == card_two == card_three):
                    self.discard(card_one)
                    self.discard(card_two)
                    self.discard(card_three)
                    self.player_one_cleared = i
                    self.player_one_total[i - 8] = None
                    self.player_one_total[i - 4] = None
                    self.player_one_total[i] = None
                    self.player_one_visible[i - 8] = None
                    self.player_one_visible[i - 4] = None
                    self.player_one_visible[i] = None
                    return 1
                i += 1
        
        if player == 2 and self.player_two_cleared == -1:
            i = 0
            for x in range(4):
                card_one = self.player_two_visible[i]
                card_two = self.player_two_visible[i + 4]
                card_three = self.player_two_visible[i + 8]
                if card_one is not None and (card_one == card_two == card_three):
                    self.discard(card_one)
                    self.discard(card_two)
                    self.discard(card_three)
                    self.player_two_cleared = i
                    self.player_two_total[i - 8] = None
                    self.player_two_visible[i - 8] = None
                    self.player_two_total[i - 4] = None
                    self.player_two_visible[i - 4] = None
                    self.player_two_total[i] = None
                    self.player_two_visible[i] = None
                    return 1
                i += 1