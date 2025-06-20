import pygame
import os


class EfeitoVisual(pygame.sprite.Sprite):
    def __init__(self, dono, pasta_frames, offset_x, offset_y):
        super().__init__()
        self.dono = dono # referência ao personagem
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.frames = []
        for nome_arquivo in sorted(os.listdir(pasta_frames), key=lambda n: int(n.split(".")[0])):
            caminho = os.path.join(pasta_frames, nome_arquivo)
            imagem = pygame.image.load(caminho).convert_alpha()
            imagem = pygame.transform.scale(imagem,(80, 80))
            if self.dono.flip:
                imagem = pygame.transform.flip(imagem, True, False)
            self.frames.append(imagem)

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.update_posicao()
        self.contador_frames = 0

    def update(self):
       self.contador_frames += 1
       if self.contador_frames >= 6:    # Velocidade da animação
           self.frame_index += 1
           self.contador_frames = 0

           if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]
           else:
                self.kill()     # Fim da animação

       self.update_posicao()    # Atualiza a posição a cada frame

    def update_posicao(self):
        base_y = self.dono.rect.bottom - self.dono.rect.height // 3  # base na altura do tórax/mão

        if self.dono.flip:
            self.rect.midright = (self.dono.rect.left - self.offset_x, base_y + self.offset_y)
        else:
            self.rect.midleft = (self.dono.rect.right + self.offset_x, base_y + self.offset_y)
