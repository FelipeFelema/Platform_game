import pygame
import os


class FimDeFase(pygame.sprite.Sprite):
    def __init__(self, x, y, caminho_sprite_sheet):
        """
        Inicializa o sprite de Fim de Fase.

        Args:
            x (int): Posição X inicial do sprite.
            y (int): Posição Y inicial do sprite.
            caminho_sprite_sheet (str): Caminho para a imagem da sprite sheet.
        """
        super().__init__()

        self.frames = []  # Lista para armazenar os frames da animação
        # Carrega a imagem da sprite sheet e converte para um formato otimizado com transparência
        imagem = pygame.image.load(caminho_sprite_sheet).convert_alpha()

        # Divide a sprite sheet em frames individuais
        # Supondo que a sprite sheet tem 7 frames, cada um com 48x48 pixels
        for i in range(7):
            # Cria um sub-retângulo para cada frame na sprite sheet
            frame = imagem.subsurface(pygame.Rect(i * 48, 0, 48, 48))
            self.frames.append(frame)  # Adiciona o frame à lista

        self.frame_index = 0  # Índice do frame atual na animação
        self.image = self.frames[self.frame_index]  # Define a imagem inicial do sprite
        # Obtém o retângulo da imagem e define sua posição no canto superior esquerdo
        self.rect = self.image.get_rect(topleft=(x, y))

        self.contador_animacao = 0  # Contador para controlar a velocidade da animação

    def update(self):
        """
        Atualiza o estado do sprite Fim de Fase, avançando sua animação.
        Este é chamado a cada frame do jogo.
        """
        # Incrementa o contador da animação
        self.contador_animacao += 1
        # Verifica se é hora de avançar para o próximo frame da animação (a cada 6 ticks de atualização)
        if self.contador_animacao >= 6:
            self.contador_animacao = 0  # Reseta o contador
            # Avança para o próximo frame, voltando ao início se chegar ao final da lista
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            # Atualiza a imagem do sprite para o novo frame
            self.image = self.frames[self.frame_index]

    def desenhar(self, tela, camera_x):
        """
        Desenha o sprite Fim de Fase na tela, ajustando pela posição da câmera.

        Args:
            tela (pygame.Surface): A superfície onde o sprite será desenhado.
            camera_x (int): A posição X da câmera no mundo do jogo, usada para parallax.
        """
        # Calcula a posição X na tela, subtraindo a posição da câmera
        pos_x = self.rect.x - camera_x
        # Desenha a imagem do sprite na posição calculada na tela
        tela.blit(self.image, (pos_x, self.rect.y))