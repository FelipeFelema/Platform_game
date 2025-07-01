import pygame
import sys
from code.Menu import menu
from code.Player import Player
from code.Effect import EfeitoVisual
from code.Parallax import ParallaxBackground
from code.FimDeFase import FimDeFase
from code.TilePlataforma import TilePlataforma
from code.PlataformasCustom import ParedeVertical, PlataformaHorizontal

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
    comprimento_fase = 2500
    camera_x = 0  # Posição atual da câmera no mundo
    camera_x_anterior = 0  # Nova variável para calcular o deslocamento para o parallax

    # Grupos
    grupo_plataformas = pygame.sprite.Group()
    grupo_efeitos = pygame.sprite.Group()
    grupo_fim = pygame.sprite.Group()

    # Background
    background = ParallaxBackground(largura, altura, "assets/images/background")

    # Preparando tiles para chão
    tile_dir = "assets/images/tiles"
    tile_size = 32
    num_tiles_fase = comprimento_fase // tile_size

    # Matriz de tiles para o chão (4 linhas de 32px cada = 128px de altura)
    linha_grama = ["tile_05.png"] + ["tile_07.png"] * (num_tiles_fase - 2) + ["tile_08.png"]
    linha_chao = ["tile_03.png"] * num_tiles_fase
    linha_terra_clara = ["tile_12.png"] * num_tiles_fase
    linha_terra_escura = ["tile_12.png"] * num_tiles_fase
    matriz_chao = [linha_grama, linha_chao, linha_terra_clara, linha_terra_escura]

    altura_total_chao_px = len(matriz_chao) * tile_size  # 4 * 32 = 128px

    # A linha vermelha da hitbox (y_chao_hitbox) deve estar no topo da grama.
    # Se o chão completo (128px) termina na altura da tela (600px),
    # então o topo da grama (que é a primeira linha da matriz_chao) estará em:
    y_chao_hitbox = altura - altura_total_chao_px

    # O offset visual deve ser 0 para que o desenho da grama comece exatamente na y_chao_hitbox.
    offset_visual_do_chao = -30

    plataforma_chao = TilePlataforma(0, y_chao_hitbox, matriz_chao, tile_dir, offset_visual_do_chao)
    grupo_plataformas.add(plataforma_chao)

    # Exemplo: Parede vertical1 12 tiles de altura no x=1500
    parede1_altura_tiles = 12
    parede1 = ParedeVertical(1500, y_chao_hitbox - (parede1_altura_tiles * tile_size), parede1_altura_tiles, tile_dir)
    grupo_plataformas.add(parede1)

    # Exemplo: Parede vertical2 12 tiles de altura no x=2000
    parede2_altura_tiles = 12
    parede2 = ParedeVertical(2000, y_chao_hitbox - (parede2_altura_tiles * tile_size), parede2_altura_tiles, tile_dir)
    grupo_plataformas.add(parede2)

    # Exemplo: Parede vertical2 12 tiles de altura no x=2200
    parede3_altura_tiles = 12
    parede3 = ParedeVertical(2200, y_chao_hitbox -100 - (parede3_altura_tiles * tile_size), parede3_altura_tiles, tile_dir)
    grupo_plataformas.add(parede3)


    # Exemplo: Plataforma horizontal 6 tiles no x=400, 5 tiles acima do chão
    plataforma1_y = y_chao_hitbox - 5 * tile_size
    plataforma1 = PlataformaHorizontal(400, plataforma1_y, 6, tile_dir)
    grupo_plataformas.add(plataforma1)

    # Exemplo: Plataforma horizontal2 5 tiles no x=1042, 7 tiles acima do chão
    plataforma2_y = y_chao_hitbox - 7 * tile_size
    plataforma2 = PlataformaHorizontal(1042, plataforma2_y, 5, tile_dir)
    grupo_plataformas.add(plataforma2)

    # Exemplo: Plataforma horizontal4 5 tiles no x=1342, 4 tiles acima do chão
    plataforma3_y = y_chao_hitbox - 4 * tile_size
    plataforma3 = PlataformaHorizontal(1342, plataforma3_y, 5, tile_dir)
    grupo_plataformas.add(plataforma3)

    # Exemplo: Plataforma horizontal4 5 tiles no x=1342, 12 tiles acima do chão
    plataforma4_y = y_chao_hitbox - 12 * tile_size
    plataforma4 = PlataformaHorizontal(1342, plataforma4_y, 5, tile_dir)
    grupo_plataformas.add(plataforma4)

    # Exemplo: Plataforma horizontal5 4 tiles no x=1800, 5 tiles acima do chão
    plataforma5_y = y_chao_hitbox - 5 * tile_size
    plataforma5 = PlataformaHorizontal(1650, plataforma5_y, 4, tile_dir)
    grupo_plataformas.add(plataforma5)

    # Exemplo: Plataforma horizontal6 4 tiles no x=1950, 10 tiles acima do chão
    plataforma6_y = y_chao_hitbox - 10 * tile_size
    plataforma6 = PlataformaHorizontal(1800, plataforma6_y, 4, tile_dir)
    grupo_plataformas.add(plataforma6)

    # Posição vertical do player: com os pés na grama (topo da hitbox do chão)
    altura_player_hitbox = 90
    y_player_inicial = y_chao_hitbox - altura_player_hitbox
    player = Player(0, y_player_inicial, grupo_efeitos, largura, grupo_plataformas, comprimento_fase)

    # Bandeira no fim da fase
    fim_fase_temp = pygame.image.load("assets/images/final/flag.png").convert_alpha()
    altura_bandeira = fim_fase_temp.get_height()
    y_bandeira = y_chao_hitbox - altura_bandeira
    fim_fase = FimDeFase(comprimento_fase - 100, y_bandeira, "assets/images/final/flag.png")
    grupo_fim.add(fim_fase)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()

        # 1. Atualiza o player. Ele agora apenas atualiza a própria posição no mundo.
        player.update(teclas)

        # --- Lógica de atualização da câmera (AGORA CENTRALIZADA AQUI) ---

        # 2. Define a posição "alvo" da câmera baseada no centro do player
        # A câmera tenta manter o player no centro da tela (largura // 2)
        camera_x_alvo = player.rect.centerx - largura // 2

        # 3. Aplica os limites da fase à posição da câmera
        # Limite esquerdo: câmera nunca pode ser menor que 0
        camera_x_atual = max(0, camera_x_alvo)

        # Limite direito: câmera nunca pode ser maior que (comprimento_fase - largura da tela)
        limite_max_camera = comprimento_fase - largura
        # Garante que não haja limite negativo se a fase for menor que a tela (raro, mas evita erros)
        if limite_max_camera < 0:
            limite_max_camera = 0
        camera_x_atual = min(camera_x_atual, limite_max_camera)

        # 4. Calcula o deslocamento real da câmera desde o último frame (para o parallax)
        deslocamento_camera_para_parallax = camera_x_atual - camera_x_anterior

        # 5. Atualiza a camera_x para o próximo frame
        camera_x = camera_x_atual
        camera_x_anterior = camera_x_atual  # Guarda a posição atual para o próximo cálculo de deslocamento

        # --- FIM DA LÓGICA DA CÂMERA ---

        tela.fill((135, 206, 235))
        # Passa o deslocamento *real* da câmera para o background
        background.desenhar(tela, deslocamento_camera_para_parallax)

        for plataforma in grupo_plataformas:
            if hasattr(plataforma, "draw"):
                # Plataformas como TilePlataforma e ParedeVertical/PlataformaHorizontal personalizadas
                # usam seu próprio método draw que já lida com camera_x internamente
                plataforma.draw(tela, camera_x)
            else:
                # Caso haja alguma Plataforma genérica que não tenha método draw
                tela.blit(plataforma.image, (plataforma.rect.x - camera_x, plataforma.rect.y))

            # Desenha a hitbox das plataformas (PARA DEPURAR)
            pygame.draw.rect(tela, (255, 0, 0), (plataforma.rect.x - camera_x, plataforma.rect.y, plataforma.rect.width,
                                                 plataforma.rect.height), 2)

        player.draw(tela, camera_x)

        for efeito in grupo_efeitos:
            efeito.draw(tela, camera_x)

        for sprite_fim in grupo_fim:
            sprite_fim.desenhar(tela, camera_x)

        # --- Desenho das linhas de depuração de limites do mundo ---
        # A linha inferior do mundo (borda da tela, onde o espaço roxo deve sumir)
        pygame.draw.line(tela, (255, 0, 0), (0 - camera_x, altura - 1), (comprimento_fase - camera_x, altura - 1), 2)

        # A linha que representa o topo da hitbox do chão principal
        # Esta linha agora deve aparecer no topo do seu chão de grama.
        pygame.draw.line(tela, (255, 0, 0), (0 - camera_x, y_chao_hitbox), (comprimento_fase - camera_x, y_chao_hitbox),
                         2)

        # Exemplo de linha para o topo do mundo (se precisar depurar o teto)
        # pygame.draw.line(tela, (255, 0, 0), (0 - camera_x, 0), (comprimento_fase - camera_x, 0), 2)

        # --- Fim do desenho das linhas de depuração ---

        # Checa fim da fase
        if player.rect.right > fim_fase.rect.x:
            mostrar_tela_fim(tela, largura, altura)
            rodando = False

        pygame.display.update()
        relogio.tick(60)


while True:
    menu(tela, largura, altura)
    iniciar_jogo()