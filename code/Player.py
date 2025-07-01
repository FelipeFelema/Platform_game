import pygame
from code.Effect import EfeitoVisual # Importa a classe para criar efeitos visuais


def carregar_sprite_sheet(caminho, largura_frame, altura_frame):
    """Carrega uma sprite sheet e a divide em frames individuais."""
    imagem = pygame.image.load(caminho).convert_alpha()
    largura_total, altura_total = imagem.get_size()

    frames = []
    for i in range(largura_total // largura_frame):
        frame = imagem.subsurface(pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame))
        frames.append(frame)

    return frames


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, grupo_efeitos, largura_tela, grupo_plataformas, comprimento_fase):
        super().__init__()
        self.grupo_efeitos = grupo_efeitos # Grupo para adicionar efeitos visuais (ex: ataque)
        self.velocidade = 5
        self.largura_tela = largura_tela
        self.grupo_plataformas = grupo_plataformas # Grupo de sprites de plataformas para colisão
        self.comprimento_fase = comprimento_fase # Limite horizontal da fase

        # Carrega as animações do player
        self.animacoes = {
            "idle": carregar_sprite_sheet("assets/images/player/idle/idle.png", 128, 128),
            "run": carregar_sprite_sheet("assets/images/player/run/run.png", 128, 128),
            "jump": carregar_sprite_sheet("assets/images/player/jump/jump.png", 128, 128),
            "attack": carregar_sprite_sheet("assets/images/player/attack/attack.png", 128, 128),
            "hurt": carregar_sprite_sheet("assets/images/player/hurt/hurt.png", 128, 128),
            "dead": carregar_sprite_sheet("assets/images/player/dead/dead.png", 128, 128)
        }
        # Fallback para animações de "hurt" e "dead" se não existirem
        if not self.animacoes.get("hurt"):
            self.animacoes["hurt"] = self.animacoes["idle"]
        if not self.animacoes.get("dead"):
            self.animacoes["dead"] = self.animacoes["idle"]

        self.estado = "idle" # Estado atual da animação do player
        self.frame_index = 0 # Índice do frame atual da animação

        # Dimensões da hitbox do player
        self.hitbox_largura = 40
        self.hitbox_altura = 90
        self.rect = pygame.Rect(x, y, self.hitbox_largura, self.hitbox_altura)

        # Offsets para ajustar a posição da imagem em relação à hitbox
        self.offset_x_imagem_normal = -45
        self.offset_y_imagem = -40

        self.image = self.animacoes[self.estado][self.frame_index] # Imagem atual do player
        self.image_draw_pos = (self.rect.x + self.offset_x_imagem_normal,
                               self.rect.y + self.offset_y_imagem) # Posição de desenho da imagem

        self.vel_y = 0 # Velocidade vertical (para gravidade e pulo)
        self.gravidade = 1.0
        self.forca_pulo = -20

        self.no_chao = False # Indica se o player está no chão
        self.flip = False # Indica se a imagem deve ser virada horizontalmente
        self.contador_animacao = 0 # Contador para controlar a velocidade da animação

        self.tempo_ultimo_ataque = 0
        self.cooldown_ataque = 500 # Tempo de espera entre ataques

        # Atributos de vida e dano do player
        self.vida_maxima = 100
        self.vida_atual = self.vida_maxima
        self.esta_morto = False
        self.esta_hurting = False # Indica se o player está sofrendo dano
        self.tempo_inicio_hurt = 0
        self.duracao_hurt = 300 # Duração do estado "hurt" (em milissegundos)
        self.invencivel = False # Invencibilidade temporária após tomar dano
        self.tempo_invencivel = 0
        self.duracao_invencibilidade = 1000 # Duração da invencibilidade (1 segundo)
        self.dano_sofrido_cooldown = 0 # Usado para evitar dano repetido do mesmo inimigo

    def tomar_dano(self, quantidade_dano):
        """Reduz a vida do player e inicia o estado de 'hurt' se não estiver invencível ou morto."""
        if not self.invencivel and not self.esta_morto:
            self.vida_atual -= quantidade_dano
            if self.vida_atual <= 0:
                self.morrer()
            else:
                self.esta_hurting = True
                self.tempo_inicio_hurt = pygame.time.get_ticks()
                self.estado = "hurt"
                self.frame_index = 0
                self.invencivel = True
                self.tempo_invencivel = pygame.time.get_ticks()

    def morrer(self):
        """Define o player como morto e inicia a animação de morte."""
        if not self.esta_morto:
            self.esta_morto = True
            self.estado = "dead"
            self.frame_index = 0 # Reinicia a animação de morte
            self.vel_y = 0 # Para o movimento vertical

    def atualizar_estado(self, teclas):
        """Atualiza o estado de animação do player com base nas entradas e condições."""
        estado_anterior = self.estado
        agora = pygame.time.get_ticks()

        # Lógica de invencibilidade
        if self.invencivel:
            if agora - self.tempo_invencivel > self.duracao_invencibilidade:
                self.invencivel = False

        # Lógica do estado "hurt"
        if self.esta_hurting:
            if agora - self.tempo_inicio_hurt > self.duracao_hurt:
                self.esta_hurting = False
                self.estado = "idle" # Volta para idle após o "hurt"
            else:
                return # Não processa outras entradas enquanto está "hurting"

        # Se estiver morto, apenas anima a morte
        if self.esta_morto:
            # Garante que a animação de morte pare no último frame
            if self.frame_index >= len(self.animacoes["dead"]) - 1:
                self.frame_index = len(self.animacoes["dead"]) - 1
            return

        # Se estiver atacando, permanece no estado de ataque até o fim da animação
        if self.estado == "attack":
            if self.frame_index >= len(self.animacoes["attack"]) - 1:
                self.estado = "idle" # Volta para idle após o ataque
            return

        # Detecta a entrada de ataque
        if teclas[pygame.K_z] and agora - self.tempo_ultimo_ataque > self.cooldown_ataque:
            self.tempo_ultimo_ataque = agora
            self.estado = "attack"
            offset_y_efeito = -53
            # Ajusta a posição do efeito de ataque com base na direção do player
            offset_x_efeito = -70 if self.flip else -10
            efeito = EfeitoVisual(self, "assets/images/effects/slash", offset_x_efeito, offset_y_efeito)
            self.grupo_efeitos.add(efeito)
        elif not self.no_chao: # Se não está no chão, está pulando
            self.estado = "jump"
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]: # Se está se movendo horizontalmente
            self.estado = "run"
        else: # Se nenhuma das condições acima, está parado
            self.estado = "idle"

        # Reseta o frame da animação se o estado mudou (exceto para certos estados)
        if self.estado != estado_anterior and estado_anterior not in ["hurt", "dead"]:
            self.frame_index = 0
            self.contador_animacao = 0

    def update(self, teclas):
        """Atualiza a posição, movimento, estado e animações do player."""
        self.atualizar_estado(teclas)

        # Lógica de movimento e gravidade quando o player está morto
        if self.esta_morto:
            self.vel_y += self.gravidade
            self.vel_y = min(self.vel_y, 10) # Limita a velocidade de queda
            self.rect.y += self.vel_y
            # Colisão com plataformas para o corpo morto
            for plataforma in self.grupo_plataformas:
                if self.rect.colliderect(plataforma.rect):
                    if self.vel_y > 0:
                        self.rect.bottom = plataforma.rect.top
                        self.vel_y = 0
                        self.no_chao = True
            self.animar() # Continua a animação de morte
            return # Não processa outras ações se estiver morto

        # Lógica de movimento e gravidade quando o player está "hurting"
        if self.esta_hurting:
            self.animar() # Continua a animação de "hurt"
            self.vel_y += self.gravidade
            self.vel_y = min(self.vel_y, 10)
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
            return # Não processa movimento normal ou ataque se estiver "hurting"

        # Movimento horizontal do player
        dx = 0
        if teclas[pygame.K_LEFT]:
            dx = -self.velocidade
            self.flip = True
        elif teclas[pygame.K_RIGHT]:
            dx = self.velocidade
            self.flip = False

        self.rect.x += dx # Aplica o movimento horizontal

        # Colisão horizontal com plataformas
        for plataforma in self.grupo_plataformas:
            if self.rect.colliderect(plataforma.rect):
                if dx > 0: # Se movendo para a direita
                    self.rect.right = plataforma.rect.left
                    dx = 0
                elif dx < 0: # Se movendo para a esquerda
                    self.rect.left = plataforma.rect.right
                    dx = 0

        # Limita o player dentro dos limites da fase
        if self.rect.right > self.comprimento_fase:
            self.rect.right = self.comprimento_fase
        if self.rect.left < 0:
            self.rect.left = 0

        # Lógica de pulo
        if teclas[pygame.K_SPACE] and self.no_chao:
            self.vel_y = self.forca_pulo
            self.no_chao = False
            self.estado = "jump"

        # Aplica gravidade ao movimento vertical
        self.vel_y += self.gravidade
        self.vel_y = min(self.vel_y, 10) # Limita a velocidade de queda
        self.rect.y += self.vel_y

        # Colisão vertical com plataformas
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

        # Atualiza a animação do player e os efeitos visuais
        self.animar()
        self.grupo_efeitos.update()

    def animar(self):
        """Atualiza o frame da animação e a imagem do sprite do player."""
        animacao = self.animacoes[self.estado]
        self.frame_index += 0.2 # Avança o frame da animação

        # Lógica para loop das animações e transições de estado
        if self.frame_index >= len(animacao):
            self.frame_index = 0
            if self.estado == "attack":
                self.estado = "idle" # Retorna para idle após o ataque
            elif self.estado == "dead":
                self.frame_index = len(animacao) - 1 # Trava no último frame da morte

        imagem_atual_original = animacao[int(self.frame_index)] # Pega a imagem do frame atual

        # Aplica o flip horizontal à imagem se necessário
        self.image = pygame.transform.flip(imagem_atual_original, self.flip, False)

        # Calcula a posição de desenho da imagem na tela, considerando o offset
        self.image_draw_pos = (
            self.rect.centerx - self.image.get_width() / 2, # Centraliza a imagem horizontalmente
            self.rect.top + self.offset_y_imagem # Aplica o offset Y
        )

    def draw(self, screen, camera_x):
        """Desenha o player e sua hitbox na tela."""
        screen_x = self.image_draw_pos[0] - camera_x # Ajusta a posição X pela câmera
        screen_y = self.image_draw_pos[1]
        screen.blit(self.image, (screen_x, screen_y)) # Desenha a imagem do player