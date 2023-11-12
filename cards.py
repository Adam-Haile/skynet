import pygame
from defaults import *

class Card():
    def __init__(self, value, hidden_value=12, position=0):
        super().__init__()
        self.image = pygame.Surface((card_width, card_height))
        self.rect = self.image.get_rect()
        self.value = value
        self.position = position
        self.hidden_value = hidden_value

        if self.value is None:
            self.image.fill(DEFAULT)
        else:
            if self.value < 0:
                self.image.fill(DEEP_BLUE)
            if self.value == 0:
                self.image.fill(LIGHT_BLUE)
            if self.value > 0 and self.value < 5:
                self.image.fill(GREEN)
            if self.value >= 5 and self.value < 9:
                self.image.fill(YELLOW)
            if self.value >= 9:
                self.image.fill(RED)

        self.color = (0, 0, 0)

        pygame.draw.rect(self.image, self.color, [0, 0, card_width, card_height], 3)

        if self.value is None:
            text = sky_font.render("SKYJO", True, self.color)
            self.image.blit(
                text, [7.5, card_height/2 - 15, text.get_rect().width, text.get_rect().height])
        else:
            text = default_font.render(str(value).capitalize(), True, self.color)
            if len(str(value)) == 2:
                self.image.blit(text, [card_width/2 - 27, card_height /
                                2 - 25, text.get_rect().width, text.get_rect().height])
            if len(str(value)) == 1:
                self.image.blit(text, [card_width/2 - 15, card_height /
                                2 - 25, text.get_rect().width, text.get_rect().height])

    def move_to(self, x, y):
        self.rect.x = (x - card_width / 2)
        self.rect.y = (y - card_height / 2)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect