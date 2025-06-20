import pygame
import sys
from code.Menu import menu
from code.Player import Player
from code.Effect import EfeitoVisual
from code.Parallax import ParallaxBackground

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
grupo_efeitos = pygame.sprite.Group()
player = Player(100, 100, grupo_efeitos, largura)  # passar largura da tela
todos_sprites = pygame.sprite.Group()
todos_sprites.add(player)

# Background
background = ParallaxBackground(largura, altura, "assets/images/background")

# Variável que acumula o quanto a câmera já andou
camera_x = 0

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Entrada
    teclas = pygame.key.get_pressed()

    # Atualiza o jogador e recebe quanto ele quer mover a câmera
    deslocamento_camera = player.update(teclas)
    camera_x += deslocamento_camera

    # Desenho
    tela.fill((135, 206, 235))  # cor do céu
    background.desenhar(tela, deslocamento_camera)

    grupo_efeitos.update()
    grupo_efeitos.draw(tela)
    todos_sprites.draw(tela)

    # Chão fixo (pode ser alterado no futuro com camera_x)
    pygame.draw.rect(tela, (139, 69, 19), (0, 500, 800, 100))

    pygame.display.update()
    relogio.tick(60)

pygame.quit()
sys.exit()
