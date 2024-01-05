import pygame.sprite

import assets
import configs
from layer import Layer
from model.floor import Floor
from model.pipe import Pipe


class Bird(pygame.sprite.Sprite):
    _FLAP_COOLDOWN = 5

    def __init__(self, *groups):
        self._layer = Layer.PLAYER
        self._sprites = [
            assets.get_image('redbird-upflap'),
            assets.get_image('redbird-midflap'),
            assets.get_image('redbird-downflap'),
            assets.get_image('redbird-midflap')
        ]
        self.image = self._sprites[0]
        # topleft -50 serve para esconder o Bird e dar uma transição
        self.rect = self.image.get_rect(
            topleft=(-50, configs.SCREEN_HEIGHT // 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = 0
        self._counter = 0
        super().__init__(*groups)

    def update(self):
        self._flap_animation()

        self.velocity += configs.GRAVITY  # faz o bir cair
        # Faz com que o bird suba ou caia, dependendo da velocidade e gravidade
        self.rect.y += self.velocity
        # doing transition left to right until the pixel 49 of the screen
        if self.rect.x < 50:
            self.rect.x += 3

    def _flap_animation(self):
        # the bird just flaps when whe cooldown (5) is reached (maybe add a thread?)
        self._counter += 1
        if self._counter > self._FLAP_COOLDOWN:
            self._counter = 0
        # deleto o sprite na ultima posição e a insiro no início da lista
            self._sprites.insert(0, self._sprites.pop())
            # a imagem vista sempre é o index 0 dos sprites
            self.image = self._sprites[0]
            # virar o flap bird quando ele cai
            # self.image = pygame.transform.rotate(
            #     self._sprites[0], self.velocity * -2)

    def handle_event(self, event):
        # 1º verifico se a houve um evendo de tecla apertada. 2º aí é que consigo verificar qual key foi
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # ele só pula enquando não passar do pixel 0 - tamanho dele
            # quando eles estiver no -self.rect.height que é acima da tela ele não sobe mais
            if self.rect.bottom > -self.rect.height:
                self.velocity = 0  # zero a velocidade para não vim com o valor da gravidade e subir pouco
                # é "-="" pois é contra a gravidade
                self.velocity -= 6
            assets.play_audio('wing')

    def check_collision(self, sprites):
        for sprite in sprites:
            if ((type(sprite) is Floor) and sprite.mask.overlap(self.mask, (
                    self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y))):
                return True

            if ((type(sprite) is Pipe) and sprite.mask.overlap(self.mask, (
                    self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y))):
                return True
        return False
