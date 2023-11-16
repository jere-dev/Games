import pygame
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
class tiles():
    def __init__(self, game, size):
        self.size = size
        self.tiles = {(5, 7): "grass", (6, 7): "grass", (7,7):"grass", (7,6):"grass"}
        self.game = game

    def getTilesAround(self, pos):
        tiles = []
        tilePos = [int(pos[0]//self.size), int(pos[1]//self.size)]
        for offset in NEIGHBOR_OFFSETS:
            checkPos = (tilePos[0] + offset[0], tilePos[1] + offset[1])
            if checkPos in self.tiles:
                tiles.append(checkPos)
        return tiles
    
    def getRectsAround(self, pos):
        rects = []
        for tile in self.getTilesAround(pos):
            rects.append(pygame.Rect(tile[0]*self.size, tile[1]*self.size, self.size, self.size))
        return rects

    def render(self, surf):
        for tile in self.tiles:
            tilex = tile[0]*self.size
            tiley = tile[1]*self.size
            surf.blit(self.game.assets[self.tiles[tile]], (tilex, tiley))
