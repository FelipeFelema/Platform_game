import pygame
import os

class ParallaxBackground:
    def __init__(self, largura_tela, altura_tela, caminho_camadas):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.camadas = []

        for i in range(1, 7):   # 6 camadas: layer1 até layer6
            imagem = pygame.image.load(os.path.join(caminho_camadas, f"layer{i}.png")).convert_alpha()
            imagem = pygame.transform.scale(imagem, (largura_tela, altura_tela))
            self.camadas.append(imagem)

        self.posicoes_x = [0] * len(self.camadas)   # controle de cada camada

    def desenhar(self, tela, deslocamento):
        for i, camada in enumerate(self.camadas):
           velocidade = 0.2 + i * 0.15     # Mais distante = mais lento
           self.posicoes_x[i] += -deslocamento * velocidade

           # Loop infinito horizontal
           largura_img = self.camadas[i].get_width()
           x_pos = self.posicoes_x[i] % largura_img

           # Blita 2 vezes para garantir cobertura da tela
           tela.blit(self.camadas[i], (x_pos - largura_img, 0))
           tela.blit(self.camadas[i], (x_pos, 0))