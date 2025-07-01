import pygame
import os


def carregar_sprite_sheet(caminho, largura_frame, altura_frame):
    """Carrega uma sprite sheet e a divide em frames individuais."""
    imagem = pygame.image.load(caminho).convert_alpha()
    largura_total, altura_total = imagem.get_size()

    frames = []
    for i in range(largura_total // largura_frame):
        frame = imagem.subsurface(pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame))
        frames.append(frame)

    return frames


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo_inimigo, grupo_plataformas, comprimento_fase, plataforma_rect_alvo=None):
        super().__init__()
        self.tipo_inimigo = tipo_inimigo
        self.grupo_plataformas = grupo_plataformas
        self.comprimento_fase = comprimento_fase
        self.original_x = x  # Armazena o X inicial para patrulha padrão

        # Carrega as animações do inimigo
        self.animacoes = {
            "idle": carregar_sprite_sheet(f"assets/images/{self.tipo_inimigo}/idle/idle.png", 128, 128),
            "walk": carregar_sprite_sheet(f"assets/images/{self.tipo_inimigo}/walk/walk.png", 128, 128),
            "attack": carregar_sprite_sheet(f"assets/images/{self.tipo_inimigo}/attack/attack.png", 128, 128),
            "hurt": carregar_sprite_sheet(f"assets/images/{self.tipo_inimigo}/hurt/hurt.png", 128, 128),
            "dead": carregar_sprite_sheet(f"assets/images/{self.tipo_inimigo}/dead/dead.png", 128, 128),
        }
        # Fallback para animações ausentes
        if not self.animacoes.get("hurt"):
            self.animacoes["hurt"] = self.animacoes["idle"]
        if not self.animacoes.get("dead"):
            self.animacoes["dead"] = self.animacoes["idle"]

        self.estado = "idle" # Estado atual do inimigo
        self.frame_index = 0
        self.velocidade_animacao = 0.15

        # Define características específicas do inimigo
        if self.tipo_inimigo == "enemy1":
            self.hitbox_largura = 60
            self.hitbox_altura = 80
            self.offset_x_imagem = -35
            self.offset_y_imagem = -40
            self.velocidade = 2
            self.vida = 30
            self.dano_ataque = 10
        elif self.tipo_inimigo == "enemy2":
            self.hitbox_largura = 70
            self.hitbox_altura = 90
            self.offset_x_imagem = -30
            self.offset_y_imagem = -35
            self.velocidade = 3
            self.vida = 30
            self.dano_ataque = 10
        else:
            self.hitbox_largura = 50
            self.hitbox_altura = 70
            self.offset_x_imagem = -40
            self.offset_y_imagem = -40
            self.velocidade = 1
            self.vida = 3
            self.dano_ataque = 1

        self.rect = pygame.Rect(x, y, self.hitbox_largura, self.hitbox_altura) # Hitbox do inimigo
        self.image = self.animacoes[self.estado][self.frame_index]
        self.image_draw_pos = (self.rect.x + self.offset_x_imagem, self.rect.y + self.offset_y_imagem)

        self.vel_y = 0 # Velocidade vertical (para gravidade e pulo)
        self.gravidade = 1.0
        self.no_chao = False # Flag para saber se está no chão

        self.padding_patrulha = 15 # Margem para os limites de patrulha

        # Define os limites de X para a patrulha do inimigo
        if plataforma_rect_alvo:
            self.patrol_min_x = plataforma_rect_alvo.left + self.padding_patrulha
            self.patrol_max_x = plataforma_rect_alvo.right - self.hitbox_largura - self.padding_patrulha
        else:  # Para inimigos no chão principal
            self.patrol_min_x = max(0, self.original_x - 100)
            self.patrol_max_x = min(comprimento_fase - self.hitbox_largura, self.original_x + 100)

        self.direcao_movimento = 1  # 1 para direita, -1 para esquerda
        self.flip = False if self.direcao_movimento == 1 else True  # Define se a imagem deve ser virada

        self.esta_morto = False
        self.esta_hurting = False # Indica se o inimigo está sofrendo dano
        self.tempo_inicio_hurt = 0
        self.duracao_hurt = 300 # Tempo que o inimigo fica no estado "hurt"
        self.invencivel = False # Invencibilidade temporária
        self.tempo_invencivel = 0
        self.duracao_invencibilidade = 500

        self.tempo_ultimo_ataque = 0
        self.cooldown_ataque = 1000 # Tempo de espera entre ataques

        self.tempo_ultimo_dano_causado = 0
        self.cooldown_dano_causado = 500 # Tempo de espera para causar dano ao player

    def tomar_dano(self, quantidade_dano):
        """Processa o dano recebido pelo inimigo."""
        if not self.invencivel and not self.esta_morto:
            self.vida -= quantidade_dano
            if self.vida <= 0:
                self.morrer()
            else:
                self.esta_hurting = True
                self.tempo_inicio_hurt = pygame.time.get_ticks()
                self.estado = "hurt"
                self.frame_index = 0
                self.invencivel = True
                self.tempo_invencivel = pygame.time.get_ticks()

    def morrer(self):
        """Define o inimigo como morto."""
        if not self.esta_morto:
            self.esta_morto = True
            self.estado = "dead"
            self.frame_index = 0
            self.vel_y = 0

    def atualizar_estado(self, player_rect=None):
        """Atualiza o estado de animação do inimigo (idle, walk, attack, etc.)."""
        estado_anterior = self.estado # Guarda o estado anterior para checar mudanças
        agora = pygame.time.get_ticks()

        if self.esta_morto:
            return

        # Gerencia o tempo de invencibilidade
        if self.invencivel:
            if agora - self.tempo_invencivel > self.duracao_invencibilidade:
                self.invencivel = False

        # Gerencia o estado de "hurt" (dano)
        if self.esta_hurting:
            if agora - self.tempo_inicio_hurt > self.duracao_hurt:
                self.esta_hurting = False
                self.estado = "idle" # Retorna para "idle" após a duração do "hurt"
            else:
                return # Permanece no estado "hurt"

        # Lógica de comportamento em relação ao player
        if player_rect:
            distancia_x = self.rect.centerx - player_rect.centerx
            distancia_y = self.rect.centery - player_rect.centery

            # Se o player está próximo
            if abs(distancia_x) < 150 and abs(distancia_y) < 50:
                # Tenta atacar se o cooldown permitir
                if agora - self.tempo_ultimo_ataque > self.cooldown_ataque and self.estado != "attack":
                    self.tempo_ultimo_ataque = agora
                    self.estado = "attack"
                    self.frame_index = 0
                    self.flip = distancia_x > 0 # Vira o inimigo na direção do player
                    return
                elif self.estado != "attack": # Se não pode atacar, persegue o player
                    if distancia_x > 0:
                        self.direcao_movimento = -1
                        self.flip = True
                        self.estado = "walk"
                    else:
                        self.direcao_movimento = 1
                        self.flip = False
                        self.estado = "walk"
            elif self.estado != "attack": # Se o player está longe, anda
                self.estado = "walk"
        elif self.estado != "attack": # Se não há player ou ele está muito longe, apenas anda
            self.estado = "walk"

        # Reseta o frame da animação se o estado mudou (exceto para transição de/para attack)
        if self.estado != estado_anterior and estado_anterior != "attack":
            self.frame_index = 0

    def update(self, player_rect=None):
        """Atualiza a posição, movimento e estado do inimigo a cada frame."""
        self.atualizar_estado(player_rect)

        # Aplica gravidade e colisão vertical mesmo se morto ou ferido
        if self.esta_morto or self.esta_hurting:
            self.vel_y += self.gravidade
            if self.vel_y > 10:
                self.vel_y = 10
            self.rect.y += self.vel_y
            for plataforma in self.grupo_plataformas:
                if self.rect.colliderect(plataforma.rect):
                    if self.vel_y > 0:
                        self.rect.bottom = plataforma.rect.top
                        self.vel_y = 0
                        self.no_chao = True
                    elif self.vel_y < 0:
                        self.rect.top = plataforma.rect.bottom
                        self.vel_y = 0
            self.animar() # Continua animando (ex: animação de morte)
            return

        dx = 0 # Deslocamento horizontal
        if self.estado == "walk":
            dx = self.velocidade * self.direcao_movimento

            # Lógica de patrulha: inverte a direção ao atingir os limites
            if self.direcao_movimento == -1:  # Movendo para a esquerda
                if self.rect.x + dx < self.patrol_min_x:
                    dx = self.patrol_min_x - self.rect.x  # Ajusta para parar no limite
                    self.direcao_movimento = 1  # Inverte direção
                    self.flip = False
            elif self.direcao_movimento == 1:  # Movendo para a direita
                if self.rect.x + dx > self.patrol_max_x:
                    dx = self.patrol_max_x - self.rect.x
                    self.direcao_movimento = -1  # Inverte direção
                    self.flip = True

        self.rect.x += dx  # Aplica o movimento horizontal

        # Aplica gravidade ao movimento vertical
        self.vel_y += self.gravidade
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += self.vel_y

        # Verifica colisão com plataformas para movimento vertical
        self.no_chao = False
        for plataforma in self.grupo_plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.vel_y > 0: # Caindo
                    self.rect.bottom = plataforma.rect.top
                    self.vel_y = 0
                    self.no_chao = True
                elif self.vel_y < 0: # Subindo
                    self.rect.top = plataforma.rect.bottom
                    self.vel_y = 0

        self.animar() # Atualiza a animação com base no estado atual

    def animar(self):
        """Atualiza o frame da animação e a imagem do sprite."""
        animacao = self.animacoes[self.estado]
        self.frame_index += self.velocidade_animacao

        # Lógica para loop da animação e transições de estado
        if self.frame_index >= len(animacao):
            self.frame_index = 0
            if self.estado == "dead":
                self.frame_index = len(animacao) - 1 # Trava no último frame da morte
            elif self.estado == "attack":
                self.estado = "idle" # Volta para idle após o ataque

        imagem_atual_original = animacao[int(self.frame_index)]

        # Aplica o flip horizontal à imagem se necessário
        self.image = pygame.transform.flip(imagem_atual_original, self.flip, False)

        # Calcula a posição de desenho da imagem na tela (considerando o offset)
        self.image_draw_pos = (
            self.rect.centerx - self.image.get_width() / 2,
            self.rect.top + self.offset_y_imagem
        )

    def draw(self, screen, camera_x):
        """Desenha o inimigo e sua hitbox (para depuração) na tela."""
        screen_x = self.image_draw_pos[0] - camera_x
        screen_y = self.image_draw_pos[1]
        screen.blit(self.image, (screen_x, screen_y))