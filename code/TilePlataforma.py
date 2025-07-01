import pygame
import os

class TilePlataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, matriz_tiles, pasta_tiles, visual_offset_y=0):
        super().__init__()
        self.x = x
        self.y = y  # Coordenada Y do topo da hitbox
        self.matriz_tiles = matriz_tiles
        self.pasta = pasta_tiles
        self.tamanho_tile = 32
        self.visual_offset_y = visual_offset_y # Offset para ajustar a posição visual dos tiles

        self.tiles = {}
        # Carrega e escala todas as imagens de tiles necessárias
        for linha in matriz_tiles:
            for nome in linha:
                if nome not in self.tiles:
                    caminho = os.path.join(pasta_tiles, nome)
                    self.tiles[nome] = pygame.transform.scale(
                        pygame.image.load(caminho).convert_alpha(),
                        (self.tamanho_tile, self.tamanho_tile)
                    )

        self.linhas = len(matriz_tiles)
        self.colunas = len(matriz_tiles[0])
        self.largura = self.colunas * self.tamanho_tile
        self.altura = self.linhas * self.tamanho_tile # Altura total da hitbox

        # Define a hitbox da plataforma
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)

    def update(self):
        pass # Não há lógica de atualização contínua para plataformas estáticas

    def draw(self, tela, camera_x):
        # Desenha os tiles da plataforma, movendo-se com a câmera
        for i, linha in enumerate(self.matriz_tiles):
            for j, nome_tile in enumerate(linha):
                tile = self.tiles[nome_tile]
                x_tela = self.x + j * self.tamanho_tile - camera_x
                y_tela = self.y + i * self.tamanho_tile + self.visual_offset_y # Aplica o offset visual
                tela.blit(tile, (x_tela, y_tela))