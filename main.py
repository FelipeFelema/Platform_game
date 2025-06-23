import pygame
import sys
from code.Menu import menu
from code.Player import Player
from code.Effect import EfeitoVisual
from code.Parallax import ParallaxBackground
from code.Plataforma import Plataforma
from code.FimDeFase import FimDeFase

# Inicialização
pygame.init()
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo Plataforma Demo')
relogio = pygame.time.Clock()


def mostrar_tela_fim(tela, largura, altura):
    fonte = pygame.font.Font(None, 80)
    texto = fonte.render("Fase concluída!", True, (0, 0, 0))
    ret = texto.get_rect(center=(largura // 2, altura // 2))

    tela.fill((255, 255, 255))
    tela.blit(texto, ret)
    pygame.display.update()
    pygame.time.delay(3000)


def iniciar_jogo():
    comprimento_fase = 4000
    camera_x = 0

    # Plataformas
    grupo_plataformas = pygame.sprite.Group()
    grupo_plataformas.add(Plataforma(0, 500, comprimento_fase, 100, "assets/images/tiles/"))  # chão longo

    # Efeitos
    grupo_efeitos = pygame.sprite.Group()

    # Player
    player = Player(100, 100, grupo_efeitos, largura, grupo_plataformas, comprimento_fase)
    todos_sprites = pygame.sprite.Group()
    todos_sprites.add(player)

    # Fim de fase
    grupo_fim = pygame.sprite.Group()
    fim_fase = FimDeFase(3800, 452, "assets/images/final/flag.png")
    grupo_fim.add(fim_fase)

    # Background
    background = ParallaxBackground(largura, altura, "assets/images/background")

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        deslocamento_camera = player.update(teclas)
        camera_x += deslocamento_camera
        camera_x = max(0, min(camera_x, comprimento_fase - largura))

        # Desenho
        tela.fill((135, 206, 235))
        background.desenhar(tela, deslocamento_camera)

        grupo_efeitos.update()
        grupo_efeitos.draw(tela)
        todos_sprites.draw(tela)
        grupo_plataformas.draw(tela)

        grupo_fim.update()
        for sprite in grupo_fim:
            sprite.desenhar(tela, camera_x)

        # Colisão com bandeira
        if player.get_posicao_mundo(camera_x) + player.rect.width > fim_fase.rect.x:
            mostrar_tela_fim(tela, largura, altura)
            rodando = False  # finaliza o loop e retorna ao menu

        pygame.display.update()
        relogio.tick(60)


# Loop geral do jogo
while True:
    menu(tela, largura, altura)
    iniciar_jogo()
