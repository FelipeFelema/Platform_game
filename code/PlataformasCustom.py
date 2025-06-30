import pygame
import os

class ParedeVertical(pygame.sprite.Sprite):
    def __init__(self, x, y, altura_tiles, pasta_tiles, tile_top="tile_09.png", tile_meio="tile_18.png", tile_base="tile_27.png", tile_size=32):
        super().__init__()
        self.tile_size = tile_size
        altura_px = altura_tiles * tile_size
        self.image = pygame.Surface((tile_size, altura_px), pygame.SRCALPHA)

        # Carrega e desenha os tiles
        tile_top_img = pygame.image.load(os.path.join(pasta_tiles, tile_top)).convert_alpha()
        tile_top_img = pygame.transform.scale(tile_top_img, (tile_size, tile_size))
        tile_meio_img = pygame.image.load(os.path.join(pasta_tiles, tile_meio)).convert_alpha()
        tile_meio_img = pygame.transform.scale(tile_meio_img, (tile_size, tile_size))
        tile_base_img = pygame.image.load(os.path.join(pasta_tiles, tile_base)).convert_alpha()
        tile_base_img = pygame.transform.scale(tile_base_img, (tile_size, tile_size))

        self.image.blit(tile_top_img, (0, 0))
        for i in range(1, altura_tiles - 1):
            self.image.blit(tile_meio_img, (0, i * tile_size))
        self.image.blit(tile_base_img, (0, (altura_tiles - 1) * tile_size))

        # Hitbox do tamanho exato da imagem
        self.rect = pygame.Rect(x, y, tile_size, altura_px)


class PlataformaHorizontal(pygame.sprite.Sprite):
    def __init__(self, x, y, largura_tiles, pasta_tiles, tile_esquerda="tile_23.png", tile_meio="tile_24.png", tile_direita="tile_26.png", tile_size=32):
        super().__init__()
        self.tile_size = tile_size
        largura_px = largura_tiles * tile_size
        self.image = pygame.Surface((largura_px, tile_size), pygame.SRCALPHA)

        # Carrega e desenha os tiles
        tile_esq = pygame.image.load(os.path.join(pasta_tiles, tile_esquerda)).convert_alpha()
        tile_esq = pygame.transform.scale(tile_esq, (tile_size, tile_size))
        tile_meio = pygame.image.load(os.path.join(pasta_tiles, tile_meio)).convert_alpha()
        tile_meio = pygame.transform.scale(tile_meio, (tile_size, tile_size))
        tile_dir = pygame.image.load(os.path.join(pasta_tiles, tile_direita)).convert_alpha()
        tile_dir = pygame.transform.scale(tile_dir, (tile_size, tile_size))

        self.image.blit(tile_esq, (0, 0))
        for i in range(1, largura_tiles - 1):
            self.image.blit(tile_meio, (i * tile_size, 0))
        self.image.blit(tile_dir, ((largura_tiles - 1) * tile_size, 0))

        # Hitbox exato da plataforma
        self.rect = pygame.Rect(x, y, largura_px, tile_size)
