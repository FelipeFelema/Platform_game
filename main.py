import pygame
import sys
from code.Menu import menu
from code.Player import Player


# Inicialização
pygame.init()
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo Plataforma Demo')
relogio = pygame.time.Clock()

# Chamando o menu
menu(tela, largura, altura)

# Player
player = Player(100, 100)
todos_sprites = pygame.sprite.Group()
todos_sprites.add(player)

# Loop principal
rodando = True
while rodando:
    tela.fill((135, 206, 235)) # cor do céu

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    todos_sprites.update(teclas)
    todos_sprites.draw(tela)

    # Desenha o chão
    pygame.draw.rect(tela, (139, 69, 19), (0, 500, 800, 100))       # Chão marrom

    pygame.display.update()
    relogio.tick(60)

pygame.quit()
sys.exit()