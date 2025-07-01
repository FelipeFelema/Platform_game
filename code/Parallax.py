import pygame
import os

class ParallaxBackground:
    def __init__(self, largura_tela, altura_tela, caminho_camadas):
        """
        Inicializa o plano de fundo parallax.

        Args:
            largura_tela (int): Largura da janela do jogo.
            altura_tela (int): Altura da janela do jogo.
            caminho_camadas (str): Pasta com as imagens das camadas.
        """
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.camadas = []  # Armazena as imagens de cada camada

        # Carrega e escala 6 imagens de camada (layer1.png a layer6.png)
        for i in range(1, 7):
            imagem_path = os.path.join(caminho_camadas, f"layer{i}.png")
            imagem = pygame.image.load(imagem_path).convert_alpha()
            imagem = pygame.transform.scale(imagem, (largura_tela, altura_tela))
            self.camadas.append(imagem)

        self.posicoes_x = [0] * len(self.camadas)  # Posição X de rolagem para cada camada

    def desenhar(self, tela, deslocamento):
        """
        Desenha as camadas parallax na tela.

        Args:
            tela (pygame.Surface): Superfície de desenho.
            deslocamento (float): Deslocamento horizontal da câmera.
        """
        for i, camada in enumerate(self.camadas):
           # Calcula a velocidade de rolagem (camadas mais ao fundo se movem mais lento)
           velocidade = 0.2 + i * 0.15
           # Atualiza a posição X da camada
           self.posicoes_x[i] += -deslocamento * velocidade

           # Garante rolagem contínua das imagens
           largura_img = self.camadas[i].get_width()
           x_pos = self.posicoes_x[i] % largura_img

           # Desenha a imagem duas vezes para um efeito de loop suave
           tela.blit(self.camadas[i], (x_pos - largura_img, 0))
           tela.blit(self.camadas[i], (x_pos, 0))