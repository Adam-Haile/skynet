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
    
    def board_choice(self, players: List[Player], legal_actions):
        """
        Randomly decides which spot to play the drawn card or flip a card if it does not have one.
        Randomly chooses from the given legal actions
        """
        return random.choice(legal_actions)