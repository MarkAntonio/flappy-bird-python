import pygame.sprite
from layer import Layer
import assets
import configs


class Floor(pygame.sprite.Sprite):
    _VELOCITY = 2
    
    def __init__(self, index, *groups):
        self._layer = Layer.FLOOR
        self.image = assets.get_image('floor')
        self.rect = self.image.get_rect(bottomleft=(configs.SCREEN_WIDTH * index, configs.SCREEN_HEIGHT))
        # cria uma máscara de colisão (detalhada) a partir de uma superfície (imagem) especificada
        self.mask = pygame.mask.from_surface(self.image)
        super().__init__(*groups)

    def update(self):
        self.rect.x -= self._VELOCITY

        if self.rect.right <= 0:
            self.rect.x = configs.SCREEN_WIDTH
