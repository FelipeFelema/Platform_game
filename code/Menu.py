import pygame
import sys

from code.Const import C_BRANCO, C_AZUL, C_PRETO


def menu(tela, largura, altura):

    fonte = pygame.font.Font(None, 60)
    opcoes = ['Começar', 'Sair']
    selecionado = 0

    while True:
        tela.fill(C_BRANCO)

        for i, opcao in enumerate(opcoes):
            cor = C_PRETO
            if i == selecionado:
                cor = C_AZUL
            texto = fonte.render(opcao, True, cor)
            ret = texto.get_rect(center=(largura // 2, altura // 2 + i * 70))
            tela.blit(texto, ret)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                elif evento.key == pygame.K_RETURN:
                    if opcoes[selecionado] == 'Começar':
                        return
                    elif opcoes[selecionado] == 'Sair':
                        pygame.quit()
                        sys.exit()
