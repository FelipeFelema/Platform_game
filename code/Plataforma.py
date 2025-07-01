import pygame


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, textura_path=None, tile_tamanho=32):
        """
        Inicializa uma plataforma.

        Args:
            x (int): Posição X.
            y (int): Posição Y.
            largura (int): Largura da plataforma.
            altura (int): Altura da plataforma.
            textura_path (str, optional): Caminho para a imagem da textura.
            tile_tamanho (int, optional): Tamanho do tile da textura.
        """
        super().__init__()
        self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)

        if textura_path:
            # Carrega e escala a textura para preencher a plataforma
            textura = pygame.image.load(textura_path).convert_alpha()
            textura = pygame.transform.scale(textura, (tile_tamanho, tile_tamanho))

            # Preenche a plataforma com tiles da textura
            for i in range(0, largura, tile_tamanho):
                for j in range(0, altura, tile_tamanho):
                    self.image.blit(textura, (i, j))
        else:
            # Cor padrão se nenhuma textura for fornecida
            self.image.fill((139, 69, 19))

        # Define o retângulo de colisão da plataforma
        self.rect = self.image.get_rect(topleft=(x, y))