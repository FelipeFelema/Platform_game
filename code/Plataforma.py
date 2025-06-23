import pygame


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, textura_path=None, tile_tamanho=32):
        super().__init__()
        self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)

        if textura_path:
            textura = pygame.image.load(textura_path).convert_alpha()
            textura = pygame.transform.scale(textura, (tile_tamanho, tile_tamanho))     # tamanho base do tile

            for i in range(0, largura, tile_tamanho):
                for j in range(0, altura, tile_tamanho):
                    self.image.blit(textura, (i, j))
        else:
            self.image.fill(139, 69, 19)        # cor padrão se não tiver textura

        self.rect = self.image.get_rect(topleft=(x, y))