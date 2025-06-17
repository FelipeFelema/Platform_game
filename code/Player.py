import pygame


def carregar_sprite_sheet(caminho, largura_frame, altura_frame):
    imagem = pygame.image.load(caminho).convert_alpha()
    largura_total, altura_total = imagem.get_size()

    frames = []
    for i in range(largura_total // largura_frame):
        frame = imagem.subsurface(pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame))
        frames.append(frame)

    return frames


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.animacoes = {
            "idle": carregar_sprite_sheet("assets/images/player/idle/idle.png", 128, 128),
            "run": carregar_sprite_sheet("assets/images/player/run/run.png", 128, 128),
            "jump": carregar_sprite_sheet("assets/images/player/jump/jump.png", 128, 128)
        }

        self.estado = "idle"
        self.frame_index = 0
        self.image = self.animacoes[self.estado][self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_y = 0
        self.no_chao = False
        self.flip = False
        self.contador_animacao = 0

    def atualizar_estado(self, teclas):
        estado_anterior = self.estado

        if not self.no_chao:
            self.estado = "jump"
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]:
            self.estado = "run"
        else:
            self.estado = "idle"

        # Se o estado mudou, reseta a animação
        if self.estado != estado_anterior:
            self.frame_index = 0
            self.contador_animacao = 0

    def update(self, teclas):
        velocidade = 5
        gravidade = 0.5
        pulo_forca = -10

        # Movimento
        if teclas[pygame.K_LEFT]:
            self.rect.x -= velocidade
            self.flip = True
        elif teclas[pygame.K_RIGHT]:
            self.rect.x += velocidade
            self.flip = False

        if teclas[pygame.K_SPACE] and self.no_chao:
            self.vel_y = pulo_forca
            self.no_chao = False

        self.vel_y += gravidade
        self.rect.y += self.vel_y

        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.vel_y = 0
            self.no_chao = True

        self.atualizar_estado(teclas)
        self.animar()

    def animar(self):
        total_frames = len(self.animacoes[self.estado])

        self.contador_animacao += 1
        if self.contador_animacao >= 10:  # troca a cada 10 frames (~6 fps)
            self.frame_index = (self.frame_index + 1) % total_frames
            self.contador_animacao = 0

        self.image = self.animacoes[self.estado][self.frame_index]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
