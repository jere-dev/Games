import pygame

class entity():
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.vel = [0,0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
    def getRect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, ts, mov=(0,0), apos=None):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        if apos:
            apos = ((apos[0]-self.pos[0])//20, (apos[1]-self.pos[1])//20)
            if apos[1] < 1:
                self.vel[0] = 0
        else:
            apos = (0,0)

        frameMovment = (mov[0]+self.vel[0]+apos[0], mov[1]+self.vel[1]+apos[1])

        self.pos[0] += frameMovment[0]
        er = self.getRect()
        for rect in ts.getRectsAround(self.pos):
            if er.colliderect(rect):
                if frameMovment[0] > 0:
                    er.right = rect.left
                    self.collisions['right'] = True
                if frameMovment[0] < 0:
                    er.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = er.x

        self.pos[1] += frameMovment[1]
        er = self.getRect()
        for rect in ts.getRectsAround(self.pos):
            if er.colliderect(rect):
                if frameMovment[1] > 0:
                    er.bottom = rect.top
                    self.collisions['down'] = True
                if frameMovment[1] < 0:
                    er.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = er.y

        self.vel[1] = min(5, self.vel[1] + 0.1)
        
        if self.collisions['down'] or self.collisions['up']:
            self.vel[1] = 0

    def render(self, surf):
        surf.blit(self.game.assets["player"], self.pos)