# https://www.youtube.com/playlist?list=PLjcN1EyupaQkz5Olxzwvo1OzDNaNLGWoJ
import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60 #frames per second

screen_width = 536
screen_height = 768

screen = pygame.display.set_mode((screen_width, screen_width)) # game window
pygame.display.set_caption('Flappy Bird') # window title
# screen_width = 850
# screen_height = 936

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)
#define Color
white = (255, 255, 255)

# define game variables
ground_scroll = 0
scroll_speed = 2.5
flying = False 
game_over = False
pipe_gap = 110
pipe_frequency = 1500 #milliseconds
# measures the time when the game starts
last_pipe = pygame.time.get_ticks() - pipe_frequency # - frequency para que no início ele já gere de cara
score = 0
pass_pipe = False

# load images
bg = pygame.image.load('img/bg.png')
bg_height = bg.get_height()
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))


def reset_game():
    # deleting all pipe
    pipe_group.empty()
    flappy.rect.x = 60
    flappy.rect.y = int(screen_height / 2) - 90
    score = 0
    return score




# Criarei a sensação de movimento movendo o Ground e repetindo o processo
# isso é possível pois o chão (ground) é maior que o backuground, permitindo-me
# conectar os tracinhos que dão a impressão de movimento

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0 # speed of the animation runs
        # addiciona os sprites à lista
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 0
        self.clicked = False
    

    def update(self):

        if flying:
            # velocidade com que o Bird cai (gravidade)
            if self.velocity < 8:
                self.velocity += 0.3
            else:
                self.velocity = 8 # max velocity
        
            # se o Bird tocar o chão ele para de cair (e também não permite mais subir)
            # 476 é onde toda o ground
            if self.rect.bottom < bg_height:
                self.rect.y += int(self.velocity)

        if not game_over:
            # jump
            # get_pressed()[0] é o mouse. == 1 é se está acionado
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            # seve para não haver oc lique infinito quando eu segurar
                self.clicked = True
                self.velocity = -6
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)
        else:
             self.image = pygame.transform.rotate(self.images[self.index], -90)
             
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            #fliping the image in 90°
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        # deleting a pipe quando ele passar da tela para não consume pc memory
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()


# novamente tive que adaptar as coordenadas para darem certo com minha tela
flappy = Bird(60, int(screen_height / 2) - 90)

bird_group.add(flappy)

# esse -100 é pra corrigir a diferença de resolução do meu monitor para o do Tutorial
# bottom_pipe = Pipe(300, int(screen_height / 2)-100, -1)
# top_pipe = Pipe(300, int(screen_height / 2)-100, 1)

# pipe_group.add(bottom_pipe)
# pipe_group.add(top_pipe)

#create restart button instance
button = Button(screen_width // 2 - 34, screen_height // 2 - 200, button_img)



run = True
while run:

    clock.tick(fps)
    #draw backgound
    screen.blit(bg, (0,0)) 

    # colocando o Bird na tela
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
   

    #draw the gound
    # coloco o chão depois do Biid para que ele fique na frente dele e quando ele cair não apareça o pássaro á frente do chão.
    screen.blit(ground_img, (ground_scroll, 476))

    #check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    #draw score on screen
    draw_text(str(score), font, white, int(screen_width/2), 20)


    #look for colission
                                                        #del bird?,  #del pipe?  #bird passou do topo da tela?
    if pygame.sprite.groupcollide(bird_group, pipe_group,  False,    False) or flappy.rect.top < 0:
        game_over = True



    #check if bird has hit the ground
    if flappy.rect.bottom >= bg_height:
        game_over = True
        flying = False

    #só gera os Pipes quando o jogo começa e o passaro está voando
    if not game_over and flying:

        #generate new pipes
        time_now = pygame.time.get_ticks()
        #verifica se o tempo atual - o tempo que gerou o Pipe é maior que a frequencia de geração de pipes
        if time_now - last_pipe > pipe_frequency:
            # gera aleatoriamente o valor para o pipe mudar de position
            pipe_height = random.randint(-100, 100)
            # esse -100 é pra corrigir a diferença de resolução do meu monitor para o do Tutorial
            bottom_pipe = Pipe(screen_width, int(screen_height / 2)-100 + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2)-100 + pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now # atualiza o momento que o pipe foi gerado


        #Scroll the ground
        ground_scroll -= scroll_speed

        # aqui é o módulo do valor pois o ground está se movendo para a esquerda "-="
        if abs(ground_scroll) > 25:
            ground_scroll = 0
        
        # somente atualizo a posição do pipe se not game_over
        pipe_group.update()

    #check for game over and reset
    if game_over:
        if button.draw():
            game_over = False
            score = reset_game()


    for event in pygame.event.get():  #serve para quando eu fechar a tela do jogo ela não continuar em loop consumindo memória
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True
            
    pygame.display.update()

pygame.quit()