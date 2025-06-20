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
    def __init__(self, x, y, grupo_efeitos, largura_tela):
        super().__init__()
        self.grupo_efeitos = grupo_efeitos
        self.velocidade = 5
        self.largura_tela = largura_tela

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

    def atualizar_estado(self, teclas):
        estado_anterior = self.estado


        # Se estiver atacando, não deixa trocar de estado até a animação acabar
        if self.estado == "attack":
            return

        # Detecta o ataque
        if teclas[pygame.K_z]:
            self.estado = "attack"

            largura_efeito = 80
            altura_efeito = 80
            offset_x = -50
            offset_y = -10

            if self.flip:
                # Se estiver virado para a esquerda, ataque parte da esquerda da mão
                x_efeito = self.rect.left - (largura_efeito // 2)
            else :
                # Se estiver virado para a direita, ataque parte da direita da mão
                x_efeito = self.rect.right - (largura_efeito // 2)

            y_efeito = self.rect.centery - (altura_efeito // 2) + offset_y

            efeito = EfeitoVisual(self, "assets/images/effects/slash", offset_x, offset_y)
            self.grupo_efeitos.add(efeito)

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

    def update(self, teclas):
        deslocamento_camera = 0

        self.atualizar_estado(teclas)  # ← processa estados e ataques

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
        self.frame_index += 0.2  # pode ajustar a velocidade depois

        if self.frame_index >= len(animacao):
            self.frame_index = 0
            if self.estado == "attack":
                self.estado = "idle"  # volta para idle depois do ataque

        self.image = animacao[int(self.frame_index)]

        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)


