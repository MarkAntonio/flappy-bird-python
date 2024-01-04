import pygame.sprite

import assets
import configs
from layer import Layer
from model.floor import Floor


class Bird(pygame.sprite.Sprite):
    _FLAP_COOLDOWN = 5

    def __init__(self, *groups):
        self._layer = Layer.PLAYER
        self.sprites = [
            assets.get_image('redbird-upflap'),
            assets.get_image('redbird-midflap'),
            assets.get_image('redbird-downflap'),
            assets.get_image('redbird-midflap')
        ]
        self.image = self.sprites[0]
        # topleft -50 serve para esconder o Bird e dar uma transição
        self.rect = self.image.get_rect(topleft=(-50, configs.SCREEN_HEIGHT // 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = 0
        self._counter = 0
        super().__init__(*groups)
    
    def update(self):    
        self._flap()
        self.rect.y += self.velocity
        # doing transition left to right until the pixel 49 of the screen
        if self.rect.x < 50:
            self.rect.x += 3

    def _flap(self):
        # the bird just flaps when whe cooldown (5) is reached 
        # maybe add a thread?
        self._counter += 1
        if self._counter > self._FLAP_COOLDOWN:
            self._counter = 0
        # deleto o sprite na ultima posição e a insiro no início da lista
            self.sprites.insert(0, self.sprites.pop())
            # a imagem vista sempre é o index 0 dos sprites
            self.image = self.sprites[0]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.key.K_:
            self.velocity = 0
            # é -= pois é contra a gravidade
            self.velocity -= 6