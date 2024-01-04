import os
import pygame

images: dict[str, pygame.surface.Surface] = {}
audios: dict[str, pygame.mixer.Sound] = {}


def load_sprites():
    # Cria o caminho em String ex "C:/Users/fulano/Documents/game/assets/images"
    # resolve problemas de importação relativa
    imgs_path = os.path.join("assets", "imgs")
    print(imgs_path)
    # os.listdir(path) -> cria uma lista String com os nomes dos arquivos dentro do caminho
    for file in os.listdir(imgs_path):
        # para cada arquivo no diretório ele cria uma Surface, e adiciona ao dict com a key sendo o nome do arquivo sem o ".png, .jgp"
                                                 # ex: "assets/imgs/gameover.png"
        images[file.split('.')[0]] = pygame.image.load(os.path.join(imgs_path, file))


def get_image(name):
    return images[name]


def load_audios():
    audios_path = os.path.join("assets", "audios")
    for file in os.listdir(audios_path):
        audios[file.split('.')[0]] = pygame.mixer.Sound(os.path.join(audios_path, file))


def play_audio(name):
    audios[name].play()
