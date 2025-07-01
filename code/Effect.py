import pygame
import os


class EfeitoVisual(pygame.sprite.Sprite):
    def __init__(self, dono, pasta_frames, offset_x, offset_y):
        super().__init__()
        self.dono = dono # Referência ao personagem que criou o efeito
        self.offset_x = offset_x # Deslocamento X da posição do efeito em relação ao personagem
        self.offset_y = offset_y # Deslocamento Y da posição do efeito em relação ao personagem

        self.original_frames = []
        # Carrega e redimensiona todos os frames da animação do efeito
        for nome_arquivo in sorted(os.listdir(pasta_frames), key=lambda n: int(n.split(".")[0])):
            caminho = os.path.join(pasta_frames, nome_arquivo)
            imagem = pygame.image.load(caminho).convert_alpha()
            imagem = pygame.transform.scale(imagem, (80, 80))
            self.original_frames.append(imagem)

        self.frame_index = 0 # Índice do frame atual
        self.image = self.original_frames[self.frame_index] # Imagem atual do efeito
        self.rect = self.image.get_rect() # Retângulo (hitbox) do efeito
        self.update_imagem_e_posicao() # Define a posição inicial e flip da imagem
        self.contador_frames = 0 # Contador para controlar a velocidade da animação

        self.dano = 10 # Dano que o efeito causa
        self.hitbox_ativa = False # Indica se a hitbox de ataque está ativa
        self.frame_para_ativar_hitbox = 2 # Frame em que a hitbox será ativada
        self.hitbox_ja_aplicou_dano = False # Previne múltiplos danos pelo mesmo ataque

    def update(self):
        self.contador_frames += 1
        # Avança para o próximo frame da animação em intervalos definidos
        if self.contador_frames >= 6:
            self.frame_index += 1
            self.contador_frames = 0

            if self.frame_index < len(self.original_frames):
                # Ativa ou desativa a hitbox de ataque com base no frame atual
                if self.frame_index == self.frame_para_ativar_hitbox:
                    self.hitbox_ativa = True
                else:
                    self.hitbox_ativa = False
            else:
                self.kill() # Remove o sprite quando a animação termina

        self.update_imagem_e_posicao() # Atualiza a imagem e a posição do efeito

    def update_imagem_e_posicao(self):
        # Atualiza a imagem do efeito e aplica o flip se o personagem estiver virado
        if self.frame_index < len(self.original_frames):
            self.image = self.original_frames[int(self.frame_index)]
            if self.dono.flip:
                self.image = pygame.transform.flip(self.image, True, False)

        base_y = self.dono.rect.centery # Ponto de referência Y no personagem

        # Ajusta a posição X do efeito de acordo com a direção do personagem
        if self.dono.flip: # Personagem virado para a esquerda
            self.rect.topleft = (self.dono.rect.left + self.offset_x, base_y + self.offset_y)
        else: # Personagem virado para a direita
            self.rect.topleft = (self.dono.rect.right + self.offset_x, base_y + self.offset_y)

    def draw(self, screen, camera_x):
        # Desenha o efeito na tela, ajustando pela posição da câmera
        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y
        screen.blit(self.image, (screen_x, screen_y))