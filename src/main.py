import pygame
import assets
import configs
from model.background import Background
from model.floor import Floor
from model.bird import Bird


pygame.init()

pygame.display.set_caption('Flappy Bird')
screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False
gamestarted = False

# loading audios and sprites into the assets.py's dictionary
assets.load_sprites()
assets.load_audios()

# Além de permitir a ordenação dos sprites por camadas,
# essa classe também oferece a funcionalidade de atualização otimizada
sprites = pygame.sprite.LayeredUpdates()


def create_sprites():
    # criando sprites, adicionando imagens aos sprites e 
    # e adicionando o background ao sprites groups

    Background(0, sprites)  # First loop background
    Background(1, sprites)  # second loop background
    Floor(0, sprites)  # first loop floor
    Floor(1, sprites)  # second loop floor

    return Bird(sprites)


# Criando Sprites temporários (anonimos) e com referência
bird = create_sprites()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gamestarted and not gameover:
                gamestarted = True
        if not gameover:
            bird.handle_event(event)
    if not gameover:
        sprites.draw(screen)

    sprites.update()

    pygame.display.flip()
    clock.tick(configs.FPS)


pygame.quit()
