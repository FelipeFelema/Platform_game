# code/Enemy.py
import pygame

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Exemplo de imagem para o inimigo
        self.image = pygame.Surface((50, 70))
        self.image.fill((0, 128, 0)) # Inimigo verde
        self.rect = self.image.get_rect(topleft=(x, y))
        self.saude = 50 # Pontos de vida do inimigo
        self.velocidade = 2

    def update(self, player_rect):
        # Exemplo simples de movimento de inimigo: persegue o player
        if self.rect.x < player_rect.x:
            self.rect.x += self.velocidade
        elif self.rect.x > player_rect.x:
            self.rect.x -= self.velocidade

        # Manter inimigo dentro dos limites (opcional, dependendo do design)
        # if self.rect.right > comprimento_fase:
        #     self.rect.right = comprimento_fase
        # if self.rect.left < 0:
        #     self.rect.left = 0

    def levar_dano(self, dano):
        self.saude -= dano
        if self.saude <= 0:
            self.kill() # Remove o inimigo se a saúde for <= 0

    def draw(self, screen, camera_x):
        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y
        screen.blit(self.image, (screen_x, screen_y))
        # Opcional: Desenhar a hitbox do inimigo para depuração
        # pygame.draw.rect(screen, (255, 255, 0), (screen_x, screen_y, self.rect.width, self.rect.height), 2)