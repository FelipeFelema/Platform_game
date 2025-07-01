import pygame
import os


class EfeitoVisual(pygame.sprite.Sprite):
    def __init__(self, dono, pasta_frames, offset_x, offset_y):
        super().__init__()
        self.dono = dono  # referência ao personagem
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.original_frames = []  # Lista para armazenar os frames na orientação padrão (sem flip)
        for nome_arquivo in sorted(os.listdir(pasta_frames), key=lambda n: int(n.split(".")[0])):
            caminho = os.path.join(pasta_frames, nome_arquivo)
            imagem = pygame.image.load(caminho).convert_alpha()
            imagem = pygame.transform.scale(imagem, (80, 80))  # Redimensiona o frame
            self.original_frames.append(imagem)  # Adiciona o frame original

        self.frame_index = 0
        self.image = self.original_frames[self.frame_index]  # Começa com o primeiro frame original
        self.rect = self.image.get_rect()
        self.update_imagem_e_posicao()  # Chama o novo método para atualizar a imagem (com flip) e a posição
        self.contador_frames = 0

        # --- NOVOS ATRIBUTOS PARA A HITBOX DE ATAQUE ---
        self.dano = 10  # Dano que este ataque causa
        self.hitbox_ativa = False # Booleano para controlar quando a hitbox está ativa
        self.frame_para_ativar_hitbox = 2 # Exemplo: Ativar a hitbox no 3º frame (índice 2)
        self.hitbox_ja_aplicou_dano = False # Evita que o mesmo ataque dê dano múltiplas vezes

    def update(self):
        self.contador_frames += 1
        if self.contador_frames >= 6:  # Velocidade da animação (ajuste conforme a fluidez desejada)
            self.frame_index += 1
            self.contador_frames = 0

            if self.frame_index < len(self.original_frames):
                # A imagem será atualizada no método update_imagem_e_posicao

                # --- LÓGICA PARA ATIVAR A HITBOX ---
                if self.frame_index == self.frame_para_ativar_hitbox:
                    self.hitbox_ativa = True
                else:
                    self.hitbox_ativa = False # Desativa após o frame ativo, ou mantém desativada antes
            else:
                self.kill()  # Fim da animação, remove o sprite

        self.update_imagem_e_posicao()  # Atualiza a posição E aplica o flip à imagem a cada frame

    # NOVO MÉTODO: Atualiza a imagem do efeito (com flip) e sua posição
    def update_imagem_e_posicao(self):
        # Primeiro, atualiza a imagem baseada no frame_index
        if self.frame_index < len(self.original_frames):  # Garante que o índice é válido
            self.image = self.original_frames[int(self.frame_index)] # Usar int() para o índice
            # Agora, aplica o flip à imagem se o dono estiver virado
            if self.dono.flip:
                self.image = pygame.transform.flip(self.image, True, False)

        # Em seguida, atualiza a posição do rect do efeito
        base_y = self.dono.rect.centery  # Pega o centro Y da hitbox do player

        if self.dono.flip:  # Se o player está virado para a esquerda
            # O efeito é anexado ao lado esquerdo da hitbox do player, e offset_x é adicionado
            self.rect.topleft = (self.dono.rect.left + self.offset_x, base_y + self.offset_y)
        else:  # Se o player está virado para a direita
            # O efeito é anexado ao lado direito da hitbox do player, e offset_x é adicionado
            self.rect.topleft = (self.dono.rect.right + self.offset_x, base_y + self.offset_y)

    def draw(self, screen, camera_x):
        # Desenha a imagem visual do efeito
        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y
        screen.blit(self.image, (screen_x, screen_y))

        # Opcional: Desenhar a hitbox do ataque para depuração
        if self.hitbox_ativa:
            pygame.draw.rect(screen, (255, 0, 255), (screen_x, screen_y, self.rect.width, self.rect.height), 2)