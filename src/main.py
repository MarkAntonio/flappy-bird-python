import pygame
import assets
import configs
from model.background import Background
from model.floor import Floor
from model.bird import Bird
from model.pipe import Pipe
from model.score import Score
from model.gamestart_message import GameStartMessage
from model.gameover_message import GameOverMessage

pygame.init()

pygame.display.set_caption('Flappy Bird')
screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()
pipe_create_event = pygame.USEREVENT
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

    Floor(0, sprites)  # first loop floor
    Floor(1, sprites)  # second loop floor
    Background(0, sprites)  # First loop background
    Background(1, sprites)  # second loop background

    # score será None para eu só mostrá-lo quando começar o jogo
    return Bird(sprites), None, GameStartMessage(sprites)


# Criando Sprites temporários (anonimos) e com referência
bird, score, game_start_message = create_sprites()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pipe_create_event:
            Pipe(sprites)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gamestarted and not gameover:
                gamestarted = True
                game_start_message.kill()
                # só mostro o score depois que começa
                score = Score(sprites)
                # configura um temporizador para gerar eventos de pipe_create_event a cada 1500 ms
                pygame.time.set_timer(pipe_create_event, Pipe._FREQUENCY)

            # somente reinicio o jogo com o Esc se ele estiver terminado
            if event.key == pygame.K_ESCAPE and gameover:
                gameover = False
                gamestarted = False
                sprites.empty()
                bird, score, game_start_message = create_sprites()

        if not gameover:
            bird.handle_event(event)

    sprites.draw(screen)

    # se o jogo não estiver iniciado eu não atualizdo os frames
    if gamestarted and not gameover:
        sprites.update()

    if bird.check_collision(sprites) and not gameover:
        gameover = True
        gamestarted = False
        GameOverMessage(sprites)
        # paro de spawnar Pipes
        pygame.time.set_timer(pipe_create_event, 0)
        assets.play_audio('hit')

    for sprite in sprites:
        if type(sprite) is Pipe and sprite.is_passed():
            score.value += 1
            assets.play_audio('point')

    pygame.display.flip()
    clock.tick(configs.FPS)


pygame.quit()
