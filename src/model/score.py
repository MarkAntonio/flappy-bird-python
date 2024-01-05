import pygame.sprite

import assets
import configs
from layer import Layer


class Score(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.value = 0
        self.__create()
        super().__init__(*groups)

    def __create(self):
        images = []
        sprites_width = 0
        # itera cada caractere do valor do Score
        for str_value_char in str(self.value):
            img = assets.get_image(str_value_char)
            images.append(img)
            sprites_width += img.get_width()

        sprites_height = images[0].get_height()
        self.image = pygame.surface.Surface(
            (sprites_width, sprites_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH // 2, 50))

        x = 0
        for img in images:
            self.image.blit(img, (x, 0))
            x += img.get_width()

    def update(self):
        self.__create()
