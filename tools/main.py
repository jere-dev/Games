import pygame
import gui

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("unseen forces")
        self.screen = pygame.display.set_mode((900, 600))
        self.win = gui.window(30, 60)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.rects = [pygame.Rect(0,0,30,30)]
        self.bdown = False
        self.curserPos = pygame.mouse.get_pos()


    def run(self):
        while self.running:
            self.screen.fill((255, 0 , 0))
            self.screen.blit(self.win.display, (200, 200))
            self.curserPos = pygame.mouse.get_pos()

            for rect in self.rects:
                drawreact = rect.copy()
                drawreact.normalize()
                pygame.draw.rect(self.screen, (255, 255, 255), drawreact)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.bdown = True
                        self.rects.append(pygame.Rect(self.curserPos[0], self.curserPos[1], 0, 0))

                if event.type == pygame.MOUSEMOTION:
                    if self.bdown:
                        w = self.curserPos[0] - self.rects[-1].x
                        h = self.curserPos[1] - self.rects[-1].y
                        self.rects[-1].width = w
                        self.rects[-1].height = h
                        print(self.rects[-1])

                if event.type == pygame.MOUSEBUTTONUP:
                    self.bdown = False

            pygame.display.update()
            self.clock.tick(60)


Game().run()