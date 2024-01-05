import random
import pygame.sprite
from layer import Layer
import assets
import configs


class Pipe(pygame.sprite.Sprite):
    _GAP = 100  # vertical distante of each pipe
    _VELOCITY = 2
    _FREQUENCY = 1500

    def __init__(self, *groups):
        self._layer = Layer.OBSTACLE

        sprite = assets.get_image('pipe-green')
        sprite_rect = sprite.get_rect()

        pipe_bottom = sprite
        pipe_bottom_rect = pipe_bottom.get_rect(
            topleft=(0, sprite_rect.height + self._GAP))

        pipe_top = pygame.transform.flip(sprite, False, True)
        pipe_top_rect = pipe_top.get_rect(topleft=(0, 0))

        # cria uma superfície para adicionarmos os sprites bottom e top
        # define a largura como sendo a do Pipe sprite e altura sendo 2 * altura sprite + o gap(brecha entre eles)
        # pygame.SRCALPHA indica que terá suporte à transparência
        self.image = pygame.surface.Surface((sprite_rect.width, sprite_rect.height * 2 + self._GAP),
                                            pygame.SRCALPHA)
        # juntando os sprites e finalizando a imagem
        self.image.blit(pipe_bottom, pipe_bottom_rect)
        self.image.blit(pipe_top, pipe_top_rect)

        sprite_floor_height = assets.get_image('floor').get_rect().height
        min_y = 100
        # diz que a coordenada y max será a altura da tela - a altura do chão - 100 pixels para o Pipe não ficar muito baixo
        max_y = configs.SCREEN_HEIGHT - sprite_floor_height - 100

        # a coordenada x será gerada no fim da tela e a y será aleatório entre min y e max y
        self.rect = self.image.get_rect(
            midleft=(configs.SCREEN_WIDTH, random.uniform(min_y, max_y)))
        self.mask = pygame.mask.from_surface(self.image)

        self._passed = False

        super().__init__(*groups)

    def update(self):
        self.rect.x -= self._VELOCITY
        # deleta o pipe da tela caso ele passe do fim dela (lado esquerdo = coordenada 0)
        if self.rect.right <= 0:
            self.kill()

    def is_passed(self):
        # the bird is at pixel 50, so if my Pipe is at 40, the Bird has passed
        # a verificação do self.passed é para que não aumente a pontuação mais de 1 vez
        if self.rect.x < 40 and not self._passed:
            self._passed = True
            return True
        return False
