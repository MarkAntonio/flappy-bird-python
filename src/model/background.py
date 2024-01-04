import pygame.sprite

import assets
import configs
from layer import Layer


class Background(pygame.sprite.Sprite):

    def __init__(self, index, *groups):
        self._layer = Layer.BACKGROUND
        self.image = assets.get_image("background")
        self.rect = self.image.get_rect(topleft=(configs.SCREEN_WIDTH * index, 0))

        super().__init__(*groups)

    def update(self):
        # a cada update, será á 60 fps, o background move um pixel para a esquerda
        self.rect.x -= 1

        # Quando o útlimo pixel do lado direito da tela 
        # encostar no início da tela (pixel 0, leftside), reinicio a posição para o final da tela (rightside)
        if self.rect.right <= 0:
            self.rect.x = configs.SCREEN_WIDTH

    
