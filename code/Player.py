import pygame
from code.Effect import EfeitoVisual


def carregar_sprite_sheet(caminho, largura_frame, altura_frame):
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
        self.grupo_efeitos = grupo_efeitos
        self.velocidade = 5
        self.largura_tela = largura_tela
        self.grupo_plataformas = grupo_plataformas
        self.comprimento_fase = comprimento_fase

        self.animacoes = {
            "idle": carregar_sprite_sheet("assets/images/player/idle/idle.png", 128, 128),
            "run": carregar_sprite_sheet("assets/images/player/run/run.png", 128, 128),
            "jump": carregar_sprite_sheet("assets/images/player/jump/jump.png", 128, 128),
            "attack": carregar_sprite_sheet("assets/images/player/attack/attack.png", 128, 128)
        }

        self.estado = "idle"
        self.frame_index = 0

        # --- DEFINIÇÃO DA HITBOX FIXA E OFFSETS ---
        self.hitbox_largura = 40  # Largura da hitbox (exemplo)
        self.hitbox_altura = 90  # Altura da hitbox (ajustado para 90 conforme sua preferência)

        # O self.rect é a HITBOX. É o que o jogo usa para colisões e posicionamento.
        # O (x,y) passado para o Player é o topleft da HITBOX.
        self.rect = pygame.Rect(x, y, self.hitbox_largura, self.hitbox_altura)

        # Offsets da IMAGEM VISUAL (128x128) em relação ao topleft da HITBOX (40x90).
        # Ajustados para a sua imagem. Você mencionou -45 e -40 ficaram bons.
        self.offset_x_imagem_normal = -45
        self.offset_y_imagem = -40

        self.image = self.animacoes[self.estado][self.frame_index]  # A imagem visual atual (128x128)
        self.image_draw_pos = (self.rect.x + self.offset_x_imagem_normal,
                               self.rect.y + self.offset_y_imagem)  # Posição real de desenho

        # Ajustes para pulo e gravidade
        self.vel_y = 0
        self.gravidade = 1.0  # Gravidade por frame. Ajuste se o pulo estiver muito rápido.
        self.forca_pulo = -22  # Força inicial do pulo. Experimente -25 ou -30 se precisar pular mais alto.

        self.no_chao = False
        self.flip = False
        self.contador_animacao = 0

        # Cooldown do ataque
        self.tempo_ultimo_ataque = 0
        self.cooldown_ataque = 500  # milissegundos

    def atualizar_estado(self, teclas):
        estado_anterior = self.estado

        # Se estiver atacando e a animação não terminou, não muda de estado
        if self.estado == "attack":
            # Permite que a animação de ataque termine antes de mudar o estado
            # Verifica se está no último frame ou já passou
            if self.frame_index >= len(self.animacoes["attack"]) - 1:
                self.estado = "idle"  # Volta para idle após o ataque
            return  # Não processa outras entradas enquanto ataca

        agora = pygame.time.get_ticks()

        # Detecta o ataque
        if teclas[pygame.K_z] and agora - self.tempo_ultimo_ataque > self.cooldown_ataque:
            self.tempo_ultimo_ataque = agora
            self.estado = "attack"

            # --- NOVOS CÁLCULOS PARA A POSIÇÃO DO EFEITO DE ATAQUE ---
            # O offset_y_efeito é para ajustar a altura do ataque em relação ao centro vertical do player.
            # Valores negativos movem para cima, positivos para baixo.
            offset_y_efeito = -53  # Ajuste este valor se o ataque estiver muito alto/baixo

            # O offset_x_efeito depende da direção do personagem (flip)
            if self.flip:  # Personagem virado para a esquerda
                # Quando virado para a esquerda, o EfeitoVisual anexa ao self.dono.rect.left
                # Queremos que o lado DIREITO do efeito (80px de largura) esteja um pouco à frente da mão esquerda.
                # Se a mão está um pouco dentro da hitbox esquerda (digamos, +10px do rect.left),
                # e o efeito tem 80px, então o topleft do efeito deve ser (rect.left + 10 - 80)
                offset_x_efeito = -70  # Ajuste este valor para mover mais para a esquerda/direita
            else:  # Personagem virado para a direita
                # Quando virado para a direita, o EfeitoVisual anexa ao self.dono.rect.right
                # Queremos que o lado ESQUERDO do efeito comece um pouco à frente da mão direita.
                # Se a mão está um pouco dentro da hitbox direita (digamos, -10px do rect.right),
                # então o topleft do efeito deve ser (rect.right - 10)
                offset_x_efeito = -10  # Ajuste este valor para mover mais para a esquerda/direita

            # O EfeitoVisual já lida com o flip e anexa corretamente à hitbox do dono usando esses offsets.
            efeito = EfeitoVisual(self, "assets/images/effects/slash", offset_x_efeito, offset_y_efeito)
            self.grupo_efeitos.add(efeito)
            # --- FIM DOS NOVOS CÁLCULOS ---

        elif not self.no_chao:
            self.estado = "jump"
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]:
            self.estado = "run"
        else:
            self.estado = "idle"

        # Se o estado mudou, reseta a animação
        if self.estado != estado_anterior:
            self.frame_index = 0
            self.contador_animacao = 0

    # O método update NÃO recebe mais camera_x e NÃO retorna deslocamento_camera
    def update(self, teclas):
        self.atualizar_estado(teclas)  # Processa estados e ataques PRIMEIRO

        # --- MOVIMENTO HORIZONTAL ---
        dx = 0  # Movimento horizontal que o player TENTA fazer
        if teclas[pygame.K_LEFT]:
            dx = -self.velocidade
            self.flip = True
        elif teclas[pygame.K_RIGHT]:
            dx = self.velocidade
            self.flip = False

        # Aplica movimento horizontal (inicialmente)
        self.rect.x += dx

        # --- TRATAMENTO DE COLISÃO HORIZONTAL ---
        # AQUI, o dx pode ser zerado se houver colisão
        for plataforma in self.grupo_plataformas:
            if self.rect.colliderect(plataforma.rect):
                if dx > 0:  # movendo para a direita
                    self.rect.right = plataforma.rect.left
                    dx = 0  # Player está bloqueado, não se move horizontalmente
                elif dx < 0:  # movendo para a esquerda
                    self.rect.left = plataforma.rect.right
                    dx = 0  # Player está bloqueado, não se move horizontalmente

        # Confinar o player dentro dos limites da fase (horizontalmente)
        # O player não pode ir além dos limites da fase no mundo
        if self.rect.right > self.comprimento_fase:
            self.rect.right = self.comprimento_fase
            # Se o player colidiu com o limite direito da fase, seu dx "efetivo" é 0
            # Isso é crucial para que a câmera não tente avançar mais se o player está no limite.
            if dx > 0:  # Se ele estava tentando ir para a direita
                dx = 0

        if self.rect.left < 0:
            self.rect.left = 0
            # Se o player colidiu com o limite esquerdo do mundo, seu dx "efetivo" é 0
            if dx < 0:  # Se ele estava tentando ir para a esquerda
                dx = 0

        # --- PULO E GRAVIDADE ---
        # Aplica pulo ANTES da gravidade
        if teclas[pygame.K_SPACE] and self.no_chao:
            self.vel_y = self.forca_pulo
            self.no_chao = False
            self.estado = "jump"

        self.vel_y += self.gravidade  # Aplica gravidade
        # Limita velocidade máxima de queda
        if self.vel_y > 10:  # Limite para evitar que caia rápido demais
            self.vel_y = 10

        # Aplica movimento vertical
        self.rect.y += self.vel_y

        # --- TRATAMENTO DE COLISÃO VERTICAL ---
        self.no_chao = False  # Assume que não está no chão até colidir para baixo
        for plataforma in self.grupo_plataformas:
            if self.rect.colliderect(plataforma.rect):
                # Colisão vindo de cima (caindo)
                if self.vel_y > 0:
                    self.rect.bottom = plataforma.rect.top
                    self.vel_y = 0
                    self.no_chao = True
                # Colisão vindo de baixo (pulando e batendo no teto)
                elif self.vel_y < 0:
                    self.rect.top = plataforma.rect.bottom
                    self.vel_y = 0  # Para o movimento vertical para cima

        # --- ANIMAÇÃO E EFEITOS ---
        self.animar()  # Atualiza self.image e self.image_draw_pos
        self.grupo_efeitos.update()

        # REMOVIDA TODA A LÓGICA DE DESLOCAMENTO DA CÂMERA DAQUI
        # A câmera será controlada apenas no main.py

    def animar(self):
        animacao = self.animacoes[self.estado]
        self.frame_index += 0.2  # Velocidade da animação

        if self.frame_index >= len(animacao):
            self.frame_index = 0
            # A lógica de reset do estado "attack" é feita em atualizar_estado()
            # Isso garante que a animação termine e o estado volte para "idle"
            # apenas quando o último frame é alcançado.
            if self.estado == "attack":  # Garante que o ataque só resete o estado uma vez
                self.estado = "idle"

                # Carrega a imagem do frame atual (que é 128x128)
        imagem_atual_original = animacao[int(self.frame_index)]

        # Aplica o flip na imagem
        if self.flip:
            self.image = pygame.transform.flip(imagem_atual_original, True, False)
        else:
            self.image = imagem_atual_original

        # Calcula a posição de desenho da imagem VISUAL em relação à hitbox (self.rect)
        # A hitbox (self.rect) não muda de tamanho aqui.
        if self.flip:
            self.image_draw_pos = (
                self.rect.right - (self.image.get_width() - abs(self.offset_x_imagem_normal)),
                self.rect.top + self.offset_y_imagem
            )
        else:
            self.image_draw_pos = (
                self.rect.left + self.offset_x_imagem_normal,
                self.rect.top + self.offset_y_imagem
            )

    def draw(self, screen, camera_x):
        # Desenha a imagem visual do player
        screen_x = self.image_draw_pos[0] - camera_x
        screen_y = self.image_draw_pos[1]
        screen.blit(self.image, (screen_x, screen_y))

        # Desenha a hitbox para depuração (MANTENHA ISSO DESCOMENTADO PARA DEPURAR!)
        hitbox_screen_x = self.rect.x - camera_x
        pygame.draw.rect(screen, (0, 255, 0), (hitbox_screen_x, self.rect.y, self.rect.width, self.rect.height), 2)