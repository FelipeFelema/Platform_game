import pygame
import os


class FimDeFase(pygame.sprite.Sprite):
    def __init__(self, x, y, caminho_sprite_sheet):
        super().__init__()

        self.frames = []
        imagem = pygame.image.load(caminho_sprite_sheet).convert_alpha()

        # Supondo 7 frames de 48x48 em uma imagem de 336x48
        for i in range(7):
            frame = imagem.subsurface(pygame.Rect(i * 48, 0, 48, 48))
            self.frames.append(frame)

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.contador_animacao = 0

    def update(self):
        # Avança a animação a cada 6 frames
        self.contador_animacao += 1
        if self.contador_animacao >= 6:
            self.contador_animacao = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

    def desenhar(self, tela, camera_x):
        pos_x = self.rect.x - camera_x
        tela.blit(self.image, (pos_x, self.rect.y))
