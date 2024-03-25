import random
from typing import List
from game import Player, Deck

class Random(Player):
    """
    @author Adam Haile
    @param name: The name of the bot
    A bot that makes random decisions. This bot is not playable.
    """
    def __init__(self, name: str = "Random"):
        super().__init__(name, playable=False)

    def draw_card(self, players: List[Player], discard: Deck):
        """
        Randomly decides whether to draw from the deck or discard pile.
        Has an automatic safeguard incase the discard pile is empty.
        """
        if len(discard) == 0:
            return 0
        return random.randint(0, 1)
    
    def keep_discard_card(self, players: List[Player]):
        """
        Randomly decides whether to keep or discard the drawn card.
        """
        return random.randint(0, 1)
    
    def board_choice(self, players: List[Player]):
        """
        Randomly decides which spot to play the drawn card or flip a card if it does not have one.
        Hsa safeguards in case:
        - A column has been cleared (NoneType cards)
        - The bot is flipping a card and can only be allowed to flip visible cards
        """
        if self.drawn_card is not None:
            cards = [i for i, card in self.hand.items() if card is not None]
            return random.choice(cards)
        else:
            # Get the indexes of all cards in the player's hand which are not visible
            hidden_cards = [i for i, card in self.hand.items() if card is not None and not card.visible]
            if hidden_cards:
                return random.choice(hidden_cards)
            
            raise Exception("Illegal state")