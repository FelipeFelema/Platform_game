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
        self.image = self.animacoes[self.estado][self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_y = 0
        self.no_chao = False
        self.flip = False
        self.contador_animacao = 0

        # Cooldown do ataque
        self.tempo_ultimo_ataque = 0
        self.cooldown_ataque = 300  # milissegundos

    def atualizar_estado(self, teclas):
        estado_anterior = self.estado

        if self.estado == "attack":
            return  # mantém ataque até terminar a animação

        agora = pygame.time.get_ticks()

        # Detecta ataque com cooldown
        if teclas[pygame.K_z] and agora - self.tempo_ultimo_ataque > self.cooldown_ataque:
            self.tempo_ultimo_ataque = agora
            self.estado = "attack"

            largura_efeito = 80
            altura_efeito = 80
            offset_x = -50
            offset_y = -10

            efeito = EfeitoVisual(self, "assets/images/effects/slash", offset_x, offset_y)
            self.grupo_efeitos.add(efeito)

        elif not self.no_chao:
            self.estado = "jump"
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]:
            self.estado = "run"
        else:
            self.estado = "idle"

        if self.estado != estado_anterior:
            self.frame_index = 0
            self.contador_animacao = 0

    def update(self, teclas):
        deslocamento_camera = 0

        # Colisão com plataformas
        for plataforma in self.grupo_plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.vel_y > 0:  # caiu de cima
                    self.rect.bottom = plataforma.rect.top
                    self.vel_y = 0
                    self.no_chao = True

        self.atualizar_estado(teclas)

        if teclas[pygame.K_LEFT]:
            if self.rect.x > self.largura_tela // 3:
                self.rect.x -= self.velocidade
            else:
                deslocamento_camera = -self.velocidade
            self.flip = True

        elif teclas[pygame.K_RIGHT]:
            if self.rect.x < self.largura_tela * 2 // 3:
                self.rect.x += self.velocidade
            else:
                deslocamento_camera = self.velocidade
            self.flip = False

        # Pulo
        if teclas[pygame.K_SPACE] and self.no_chao:
            self.vel_y = -15
            self.no_chao = False
            self.estado = "jump"

        # Gravidade
        self.vel_y += 1
        self.rect.y += self.vel_y

        if self.rect.bottom > 500:
            self.rect.bottom = 500
            self.vel_y = 0
            self.no_chao = True

        self.animar()
        self.grupo_efeitos.update()
        return deslocamento_camera

    def animar(self):
        animacao = self.animacoes[self.estado]
        self.frame_index += 0.2  # pode ajustar a velocidade

        if self.frame_index >= len(animacao):
            self.frame_index = 0
            if self.estado == "attack":
                self.estado = "idle"  # volta para idle após ataque

        self.image = animacao[int(self.frame_index)]

        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def get_posicao_mundo(self, camera_x):
        return self.rect.x + camera_x
