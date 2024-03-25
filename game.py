import random
from typing import List, Dict

class Card():
    """
    @author Adam Haile
    @param value: The value of the card, visible: If the card is visible
    Initializes a new card with the given value, hidden by default
    """
    def __init__ (self, value: int, visible: bool = False):
        self.value = value
        if value < 0:
            self.color = "#3334e3"
        if value == 0:
            self.color = "#54e4fd"
        if value > 0 and value < 5:
            self.color = "#7ee258"
        if value > 4 and value < 9:
            self.color = "#faf935"
        if value > 8 and value < 13:
            self.color = "#fe1f2a"
        self.visible = visible
        
    def __str__(self):
        if self.visible:
            return str(self.value)
        else:
            return str(None)
        
    def __eq__(self, other):
        return self.value == str(other)
        
    def flip(self):
        """
        Flips the card
        """
        self.visible = not self.visible

class Deck():
    """
    @author Adam Haile
    @param card_req: Dictionary of card values and their counts, top_card_visible: If the top card is visible, name: Name of the deck
    Initializes a new deck with the given card requirements, top card visibility, and name
    """
    def __init__(self, card_req: Dict[int, int], top_card_visible: bool = False, name: str = "Deck"):
        self.cards = [Card(value) for value, count in card_req.items() for _ in range(count)]
        self.top_card_visible = top_card_visible
        self.name = name

    def __str__(self):
        return self.name
    
    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        """
        Shuffles the deck
        """
        random.shuffle(self.cards)

    def draw(self):
        """
        @return: The top card of the deck
        """
        return self.cards.pop()
    
    def discard(self, card: Card):
        """
        @param card: The card to discard
        Discards the given card
        """
        if self.top_card_visible and str(card) == "None":
            card.flip()
        self.cards.append(card)

    def peek(self):
        """
        @return: The top card of the deck
        """
        return self.cards[-1]

class Player():
    """
    @author Adam Haile
    @param name: Name of the player, playable: If the player is controlled by a human
    Initializes a new player with the given name and playable status
    """
    def __init__ (self, name: str, playable: bool = False):
        self.name = name
        self.playable = playable
        # Game variables
        self.total_score = 0

        # Round variables
        self.score = 0
        self.hand = {}
        self.drawn_card = None
        self.cleared_column = False
    
    def __str__(self):
        return self.name
    
    def get_board(self):
        """
        @return A string representation of the player's board
        """
        board = ""
        for i, card in self.hand.items():
            board += str(card) + " "
            if i == 3 or i == 7:
                board += "\n"
        return board
    
    def compute_score(self):
        """
        @return The score of the player's board
        """
        self.score = 0
        for card in self.hand.values():
            if str(card) != "None":
                self.score += int(str(card))

        return self.score

    def get_card(self, index: int):
        """
        @return The card at the given index
        """
        return self.hand[index]
    
    def replace_card(self, index: int, card: Card):
        """
        @param index: The index of the card, card: The card to set
        Sets the card at the given index
        """
        old_card = self.hand[index]
        self.hand[index] = card
        return old_card

    def flip_card(self, index: int):
        """
        @param index: The index of the card to flip
        Flips the card at the given index
        """
        if index in self.hand.keys():
            self.hand[index].flip()

    def discard_drawn(self, deck: Deck):
        """
        @param deck: The deck to discard the drawn card to
        Discards the drawn card
        """
        deck.discard(self.drawn_card)
        self.drawn_card = None

    def get_unknown_count(self):
        """
        @return The number of unknown cards in the player's hand
        """
        return len([card for card in self.hand.values() if str(card) == "None" and isinstance(card, Card)])
    
    # Abstract methods which are required to be set up by any AI players
    def draw_card(self, players: List['Player'], discard: Deck):
        """
        @param players: List of players, discard: The discard deck
        @return: 0 for deck, 1 for discard
        Logic for player's choice on drawing a card from the deck or discard
        """
        if not self.playable:
            raise NotImplementedError("This method must be implemented by the subclass")
        
        # for player in players:
        #     print(player.name + "'s board: ")
        #     print(player.get_board() + "\n")
        
        # print("Top Discard: " + str(discard.peek()) + "\n")

        answer = None
        while answer is None:
            response = input("Draw from deck (0) or discard (1)?: ")
            try:
                if int(response) >= 0 and int(response) <= 1:
                    answer = int(response)
            except:
                pass

        return answer
    
    def keep_discard_card(self, players: List['Player']):
        """
        @param players: List of players
        @return: 0 for discard, 1 for keep
        Logic for player's choice on keeping or discarding the drawn card
        """
        if not self.playable:
            raise NotImplementedError("This method must be implemented by the subclass")
        
        # print(self.get_board())
        # print("Holding: " + str(self.drawn_card))
        answer = None
        while answer is None:
            response = input("Keep the card? (0: Discard, 1: Keep): ")
            try:
                if int(response) >= 0 and int(response) <= 1:
                    answer = int(response)
            except:
                pass

        return answer
    
    def board_choice(self, players: List['Player']):
        """
        @param players: List of players
        @return: (0-11) The index of the card to replace or flip
        Logic for player's choice on replacing or flipping a card
        """
        if not self.playable:
            raise NotImplementedError("This method must be implemented by the subclass")
        
        # print(self.get_board())
        answer = None
        while answer is None:
            if self.drawn_card is not None:
                response = input("Replace a card (0-11): ")
            else:
                response = input("Flip a card (0-11): ")

            try:
                # Check if response is a valid option
                if int(response) >= 0 and int(response) <= 11:
                    # Check if user has a card and allow them to replace anything on board with if so
                    if self.drawn_card is not None:
                        answer = int(response)
                    else:
                        # Check if spot user is attempting to flip is not already flipped
                        if str(self.hand[int(response)]) == "None":
                            answer = int(response)
            except:
                pass

        return answer

class Skyjo():
    """
    @author Adam Haile
    @param players: List of players
    Initializes a new game of Skyjo with the given players
    """
    def __init__(self, players: List[Player]):
        self.players = players
        self.turn: Player = None
        self.deck: Deck = Deck({-2: 5, -1: 10, 0: 15, 1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10, 8: 10, 9: 10, 10: 10, 11: 10, 12: 10})
        self.deck.shuffle()
        self.discard = Deck({}, top_card_visible=True, name="Discard")
        self.last_winner = None
        for player in self.players:
            # Inititalize the player's hand with 12 cards
            player.hand = {i: self.deck.draw() for i in range(12)}
                
            # Flip 2 random cards for start of game
            random_indices = random.sample(range(12), 2)
            for index in random_indices:
                player.flip_card(index)
            
            # Compute the score based on flipped cards
            player.compute_score()

            # Set the first player to play based on the lowest score
            if self.turn == None:
                self.turn = player
            elif player.score < self.turn.score:
                self.turn = player

    def _turn(self):
        """
        Call current player for their actions and performs them
        Clears columns and updates scores
        """
        # print(self.turn.name + "'s turn")
        # Draw a card from the deck or discard (first action for player)
        first_action = 0 if len(self.discard) == 0 else self.turn.draw_card(self.players, self.discard)

        if first_action == 0:
            self.turn.drawn_card = self.deck.draw()
            if len(self.deck) == 0:
                self.deck.cards = self.discard.cards
                self.deck.shuffle()
                self.discard.cards = []
        else:
            self.turn.drawn_card = self.discard.draw()

        if not str(self.turn.drawn_card).isdigit():
            self.turn.drawn_card.flip()

        # Keep the drawn card or discard it (second action for player)
        second_action = self.turn.keep_discard_card(self.players)
        if second_action == 0:
            self.turn.discard_drawn(self.discard)

        # Flip or replace a card (third action for player)
        third_action = self.turn.board_choice(self.players)
        if self.turn.drawn_card != None:
            old_card = self.turn.replace_card(third_action, self.turn.drawn_card)
            self.turn.drawn_card = None
            self.discard.discard(old_card)

        else:
            self.turn.flip_card(third_action)

        # Check if a column should be cleared and compute the score based on flipped cards
        self.check_for_column()
        self.turn.compute_score()

    def _round(self):
        """
        Play a round of Skyjo calling _turn until any player has no unknown cards
        """
        while all([player.get_unknown_count() > 0 for player in self.players]):
            self._turn()
            index = self.players.index(self.turn)
            self.turn = self.players[(index + 1) % len(self.players)]
        
        self.last_winner = min(self.players, key=lambda player: player.score)
        self.reset_round()

    def play(self):
        """
        Play a game of Skyjo calling _round until a player has a total score of 100 or greater
        """
        while all([player.total_score < 100 for player in self.players]):
            self._round()
            
        return min(self.players, key=lambda player: player.total_score)
    
    def reset_round(self):
        """
        Reset the round by updating score and initializing new hands and decks.
        """
        if self.last_winner.score > min([player.score for player in self.players if player != self.last_winner]):
            self.last_winner.score *= 2
            
        for player in self.players:
            player.drawn_card = None
            player.hand = {}
            player.total_score += player.score
            player.score = 0
            player.cleared_column = False

        self.turn = self.last_winner
        self.deck = Deck({-2: 5, -1: 10, 0: 15, 1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10, 8: 10, 9: 10, 10: 10, 11: 10, 12: 10})
        self.deck.shuffle()
        self.discard = Deck({}, top_card_visible=True, name="Discard")
        for player in self.players:
            player.hand = {i: self.deck.draw() for i in range(12)}

    def check_for_column(self):
        """
        Check if a player has met the requirements to clear a column and clears it if so
        """
        for player in self.players:
            if not player.cleared_column and (str(player.hand[0]) == str(player.hand[4]) == str(player.hand[8])) and str(player.hand[0]) != "None":
                player.cleared_column = True
                player.hand[0] = None
                player.hand[4] = None
                player.hand[8] = None

            if not player.cleared_column and (str(player.hand[1]) == str(player.hand[5]) == str(player.hand[9])) and str(player.hand[1]) != "None":
                player.cleared_column = True
                player.hand[1] = None
                player.hand[5] = None
                player.hand[9] = None

            if not player.cleared_column and (str(player.hand[2]) == str(player.hand[6]) == str(player.hand[10])) and str(player.hand[2]) != "None":
                player.cleared_column = True
                player.hand[2] = None
                player.hand[6] = None
                player.hand[10] = None

            if not player.cleared_column and (str(player.hand[3]) == str(player.hand[7]) == str(player.hand[11])) and str(player.hand[3]) != "None":
                player.cleared_column = True
                player.hand[3] = None
                player.hand[7] = None
                player.hand[11] = None