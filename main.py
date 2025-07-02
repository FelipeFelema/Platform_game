import pygame
import sys
from code.Menu import menu
from code.Player import Player
from code.Parallax import ParallaxBackground
from code.FimDeFase import FimDeFase
from code.TilePlataforma import TilePlataforma
from code.PlataformasCustom import ParedeVertical, PlataformaHorizontal
from code.Enemy import Enemy

pygame.init()
pygame.mixer.init()
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jump n Slash!')
relogio = pygame.time.Clock()

COR_PRETO = (0, 0, 0)
COR_VERMELHO = (255, 0, 0)
COR_BRANCO = (255, 255, 255)


def mostrar_tela_fim(tela, largura, altura, mensagem="Fase concluída!", cor_texto=COR_PRETO):
    fonte = pygame.font.Font(None, 80)
    texto = fonte.render(mensagem, True, cor_texto)
    ret = texto.get_rect(center=(largura // 2, altura // 2))
    tela.fill((255, 255, 255))
    tela.blit(texto, ret)
    pygame.display.update()
    pygame.time.delay(3000)


def iniciar_jogo():
    pygame.mixer.music.stop()       # Para a música do menu quando o jogo inicia
    pygame.mixer.music.load("assets/music/background/background_music.mp3")         # carrega a música de fundo
    pygame.mixer.music.play(-1)         # toca a música em loop

    comprimento_fase = 2500
    camera_x = 0
    camera_x_anterior = 0

    grupo_plataformas = pygame.sprite.Group()
    grupo_efeitos = pygame.sprite.Group()
    grupo_fim = pygame.sprite.Group()
    grupo_inimigos = pygame.sprite.Group()

    background = ParallaxBackground(largura, altura, "assets/images/background")

    tile_dir = "assets/images/tiles"
    tile_size = 32
    num_tiles_fase = comprimento_fase // tile_size

    # Definição das matrizes de tiles para o chão principal
    linha_grama = ["tile_05.png"] + ["tile_07.png"] * (num_tiles_fase - 2) + ["tile_08.png"]
    linha_chao = ["tile_03.png"] * num_tiles_fase
    linha_terra_clara = ["tile_12.png"] * num_tiles_fase
    linha_terra_escura = ["tile_12.png"] * num_tiles_fase
    matriz_chao = [linha_grama, linha_chao, linha_terra_clara, linha_terra_escura]

    altura_total_chao_px = len(matriz_chao) * tile_size
    y_chao_hitbox = altura - altura_total_chao_px
    offset_visual_do_chao = -30 # Ajuste visual para o chão

    plataforma_chao = TilePlataforma(0, y_chao_hitbox, matriz_chao, tile_dir, offset_visual_do_chao)
    grupo_plataformas.add(plataforma_chao)

    # Criação de paredes verticais
    parede1_altura_tiles = 12
    parede1 = ParedeVertical(1500, y_chao_hitbox - (parede1_altura_tiles * tile_size), parede1_altura_tiles, tile_dir)
    grupo_plataformas.add(parede1)

    parede2_altura_tiles = 12
    parede2 = ParedeVertical(2000, y_chao_hitbox - (parede2_altura_tiles * tile_size), parede2_altura_tiles, tile_dir)
    grupo_plataformas.add(parede2)

    parede3_altura_tiles = 12
    parede3 = ParedeVertical(2200, y_chao_hitbox - 100 - (parede3_altura_tiles * tile_size), parede3_altura_tiles, tile_dir)
    grupo_plataformas.add(parede3)

    # Criação de plataformas horizontais
    plataforma1_y = y_chao_hitbox - 5 * tile_size
    plataforma1 = PlataformaHorizontal(400, plataforma1_y, 6, tile_dir)
    grupo_plataformas.add(plataforma1)

    plataforma2_y = y_chao_hitbox - 7 * tile_size
    plataforma2 = PlataformaHorizontal(1042, plataforma2_y, 5, tile_dir)
    grupo_plataformas.add(plataforma2)

    plataforma3_y = y_chao_hitbox - 4 * tile_size
    plataforma3 = PlataformaHorizontal(1342, plataforma3_y, 5, tile_dir)
    grupo_plataformas.add(plataforma3)

    plataforma4_y = y_chao_hitbox - 12 * tile_size
    plataforma4 = PlataformaHorizontal(1342, plataforma4_y, 5, tile_dir)
    grupo_plataformas.add(plataforma4)

    plataforma5_y = y_chao_hitbox - 5 * tile_size
    plataforma5 = PlataformaHorizontal(1650, plataforma5_y, 4, tile_dir)
    grupo_plataformas.add(plataforma5)

    plataforma6_y = y_chao_hitbox - 10 * tile_size
    plataforma6 = PlataformaHorizontal(1800, plataforma6_y, 4, tile_dir)
    grupo_plataformas.add(plataforma6)

    altura_player_hitbox = 90
    y_player_inicial = y_chao_hitbox - altura_player_hitbox
    player = Player(0, y_player_inicial, grupo_efeitos, largura, grupo_plataformas, comprimento_fase)

    # Obtém a altura da hitbox de inimigos para posicionamento inicial
    altura_enemy1_hitbox = Enemy(0, 0, "enemy1", None, 1).hitbox_altura
    altura_enemy2_hitbox = Enemy(0, 0, "enemy2", None, 1).hitbox_altura

    # Instanciação de inimigos em posições estratégicas
    inimigo1_plataforma1 = Enemy(plataforma1.rect.x + 50, plataforma1_y - altura_enemy1_hitbox, "enemy1", grupo_plataformas, comprimento_fase, plataforma_rect_alvo=plataforma1.rect)
    grupo_inimigos.add(inimigo1_plataforma1)

    inimigo2_chao_plataforma1 = Enemy(plataforma1.rect.x + 50, y_chao_hitbox - altura_enemy2_hitbox, "enemy2", grupo_plataformas, comprimento_fase, plataforma_rect_alvo=None)
    grupo_inimigos.add(inimigo2_chao_plataforma1)

    inimigo3_plataforma2 = Enemy(plataforma2.rect.x + 50, plataforma2_y - altura_enemy2_hitbox, "enemy2", grupo_plataformas, comprimento_fase, plataforma_rect_alvo=plataforma2.rect)
    grupo_inimigos.add(inimigo3_plataforma2)

    inimigo4_plataforma3 = Enemy(plataforma3.rect.x + 50, plataforma3_y - altura_enemy1_hitbox, "enemy1", grupo_plataformas, comprimento_fase, plataforma_rect_alvo=plataforma3.rect)
    grupo_inimigos.add(inimigo4_plataforma3)

    inimigo5_plataforma4 = Enemy(plataforma4.rect.x + 50, plataforma4_y - altura_enemy2_hitbox, "enemy2", grupo_plataformas, comprimento_fase, plataforma_rect_alvo=plataforma4.rect)
    grupo_inimigos.add(inimigo5_plataforma4)

    inimigo6_plataforma6 = Enemy(plataforma6.rect.x + 50, plataforma6_y - altura_enemy1_hitbox, "enemy1", grupo_plataformas, comprimento_fase, plataforma_rect_alvo=plataforma6.rect)
    grupo_inimigos.add(inimigo6_plataforma6)

    inimigo7_chao_final = Enemy(2200, y_chao_hitbox - altura_enemy2_hitbox, "enemy2", grupo_plataformas, comprimento_fase, plataforma_rect_alvo=None)
    grupo_inimigos.add(inimigo7_chao_final)

    # Configuração do fim de fase (bandeira)
    fim_fase_temp = pygame.image.load("assets/images/final/flag.png").convert_alpha()
    altura_bandeira = fim_fase_temp.get_height()
    y_bandeira = y_chao_hitbox - altura_bandeira
    fim_fase = FimDeFase(comprimento_fase - 100, y_bandeira, "assets/images/final/flag.png")
    grupo_fim.add(fim_fase)

    fonte_vida = pygame.font.Font(None, 36)

    rodando = True
    game_over = False
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if game_over:
            continue

        teclas = pygame.key.get_pressed()

        player.update(teclas)
        for inimigo in grupo_inimigos:
            inimigo.update(player.rect)

        # Lógica de atualização da câmera
        camera_x_alvo = player.rect.centerx - largura // 2
        camera_x_atual = max(0, camera_x_alvo)
        limite_max_camera = comprimento_fase - largura
        if limite_max_camera < 0:
            limite_max_camera = 0
        camera_x_atual = min(camera_x_atual, limite_max_camera)
        deslocamento_camera_para_parallax = camera_x_atual - camera_x_anterior
        camera_x = camera_x_atual
        camera_x_anterior = camera_x_atual

        tela.fill((135, 206, 235)) # Cor de fundo do céu
        background.desenhar(tela, deslocamento_camera_para_parallax)

        # Desenho das plataformas e suas hitboxes de depuração
        for plataforma in grupo_plataformas:
            if hasattr(plataforma, "draw"):
                plataforma.draw(tela, camera_x)
            else:
                tela.blit(plataforma.image, (plataforma.rect.x - camera_x, plataforma.rect.y))

        player.draw(tela, camera_x)

        for inimigo in grupo_inimigos:
            inimigo.draw(tela, camera_x)

        # Lógica de efeitos e colisões de ataque do player
        for efeito in grupo_efeitos:
            efeito.draw(tela, camera_x)

            inimigos_atingidos = pygame.sprite.spritecollide(efeito, grupo_inimigos, False)
            for inimigo in inimigos_atingidos:
                if not inimigo.esta_morto and not inimigo.invencivel:
                    inimigo.tomar_dano(efeito.dano)

            # Remove o efeito após a animação
            if efeito.frame_index >= len(efeito.original_frames) - 1:
                efeito.kill()

        # Lógica de colisão de inimigos com o player (para dano ao player)
        agora = pygame.time.get_ticks()
        for inimigo in grupo_inimigos:
            if not inimigo.esta_morto and not inimigo.esta_hurting:
                if player.rect.colliderect(inimigo.rect):
                    if agora - player.dano_sofrido_cooldown > player.duracao_invencibilidade:
                        player.tomar_dano(inimigo.dano_ataque)
                        player.dano_sofrido_cooldown = agora

        # Remove inimigos mortos (após animação completa)
        for inimigo in grupo_inimigos:
            if inimigo.esta_morto and inimigo.frame_index >= len(inimigo.animacoes["dead"]) - 1:
                inimigo.kill()

        # Desenho do sprite de fim de fase
        for sprite_fim in grupo_fim:
            sprite_fim.desenhar(tela, camera_x)

        # Exibir vida do player na tela
        texto_vida = fonte_vida.render(f"Vida: {player.vida_atual}/{player.vida_maxima}", True, (30, 250, 96, 98))
        tela.blit(texto_vida, (10, 10))

        # Checa condições de fim de jogo
        if player.esta_morto:
            mostrar_tela_fim(tela, largura, altura, "VOCÊ MORREU!", COR_VERMELHO)
            game_over = True
            rodando = False
        elif player.rect.right > fim_fase.rect.x:
            mostrar_tela_fim(tela, largura, altura)
            rodando = False

        pygame.display.update()
        relogio.tick(60)


# Loop principal que chama o menu e, em seguida, o jogo
while True:
    menu(tela, largura, altura)
    iniciar_jogo()