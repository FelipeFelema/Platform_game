import pygame
import sys

# Importa constantes de cores
from code.Const import C_BRANCO, C_AZUL, C_PRETO


def transicao_fade(tela, largura, altura, cor=(0, 0, 0), velocidade=3):
    """Cria um efeito de fade in para transições."""
    fade_surface = pygame.Surface((largura, altura))
    fade_surface.fill(cor)

    for alpha in range(0, 255, velocidade):
        fade_surface.set_alpha(alpha)
        tela.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)

def mostrar_controles(tela, largura, altura):
    """Exibe a tela de controles do jogo."""
    fonte_titulo = pygame.font.Font(None, 60)
    fonte_texto = pygame.font.Font(None, 40)

    while True:
        tela.fill(C_BRANCO)

        # Renderiza e posiciona o título "Controles"
        titulo = fonte_titulo.render("Controles", True, C_PRETO)
        tela.blit(titulo, titulo.get_rect(center=(largura // 2, 100)))

        # Lista de instruções
        instrucoes = [
            "Controles:",
            "Setas: Mover",
            "Espaço: Pular",
            "z: Atacar",
            "Esc: Sair"
        ]

        # Desenha cada instrução na tela
        for i, texto in enumerate(instrucoes):
            linha = fonte_texto.render(texto, True, C_PRETO)
            tela.blit(linha, linha.get_rect(center=(largura // 2, 200 + i * 50)))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Retorna ao menu se ESC for pressionado
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return

def menu(tela, largura, altura):
    """Exibe o menu principal do jogo."""
    fonte = pygame.font.Font(None, 60)
    opcoes = ['Começar', 'Controles', 'Sair']
    selecionado = 0

    while True:
        tela.fill(C_BRANCO)

        # Desenha as opções do menu
        for i, opcao in enumerate(opcoes):
            cor = C_PRETO
            if i == selecionado:
                cor = C_AZUL # Destaca a opção selecionada
            texto = fonte.render(opcao, True, cor)
            ret = texto.get_rect(center=(largura // 2, altura // 2 + i * 70))
            tela.blit(texto, ret)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                # Navegação entre as opções do menu
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                elif evento.key == pygame.K_RETURN:
                    # Executa a ação da opção selecionada
                    if opcoes[selecionado] == 'Começar':
                        transicao_fade(tela, largura, altura)
                        return # Inicia o jogo
                    elif opcoes[selecionado] == 'Controles':
                        mostrar_controles(tela, largura, altura)
                    elif opcoes[selecionado] == 'Sair':
                        pygame.quit()
                        sys.exit()