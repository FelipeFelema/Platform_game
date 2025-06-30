import pygame
import os

class TilePlataforma(pygame.sprite.Sprite):
    # Adicionamos 'visual_offset_y' como um novo parâmetro com valor padrão 0
    def __init__(self, x, y, matriz_tiles, pasta_tiles, visual_offset_y=0):
        super().__init__()
        self.x = x
        # Este 'y' agora representará a coordenada Y do TOPO da HITBOX (a linha vermelha)
        self.y = y
        self.matriz_tiles = matriz_tiles
        self.pasta = pasta_tiles
        self.tamanho_tile = 32
        # Armazenamos o offset para ser usado na hora de desenhar
        self.visual_offset_y = visual_offset_y

        self.tiles = {}
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
        self.altura = self.linhas * self.tamanho_tile

        # A hitbox agora é criada diretamente no 'y' passado (que é o Y da hitbox)
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)

    def update(self):
        pass

    def draw(self, tela, camera_x):
        # AQUI É A MUDANÇA: O chão principal NÃO deve ter parallax.
        # Ele deve se mover 1:1 com a câmera para permanecer "fixo" no mundo.
        # Removido o 'int(camera_x * parallax_factor)' e substituído por 'camera_x' diretamente.
        for i, linha in enumerate(self.matriz_tiles):
            for j, nome_tile in enumerate(linha):
                tile = self.tiles[nome_tile]
                x_tela = self.x + j * self.tamanho_tile - camera_x # CORREÇÃO AQUI!
                # Adicionamos o offset visual aqui. Como queremos mover o visual PARA CIMA, o offset será NEGATIVO.
                y_tela = self.y + i * self.tamanho_tile + self.visual_offset_y
                tela.blit(tile, (x_tela, y_tela))