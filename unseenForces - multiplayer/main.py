import pygame
from tileSystem import tiles
from entity import entity
from client import Client

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("unseen forces")
        self.screen = pygame.display.set_mode((900, 600))
        self.display = pygame.Surface((450, 300))

        self.clock = pygame.time.Clock()

        self.running = True
        self.assets = {
            "grass":pygame.image.load("res/grass.png"),
            "player":pygame.image.load("res/player.png")
            }
        
        self.ts = tiles(self, self.assets["grass"].get_width())
        self.player = entity(self, (0, 0), (self.assets["player"].get_width(), self.assets["player"].get_height()))
        self.movement = [False, False]

        self.client = None
        self.prevpos = [0,0]
        self.pos2 = [0,0]

        self.apos = None

    def processMessage(self, message):
        if message == "quit":
            self.client = None
            return [0,0]

        p = list(map(int, message.split(';')))
        return p

    def run(self):
        while self.running:
            self.display.fill((255, 0 , 0))

            self.ts.render(self.display)
            
            self.player.update(self.ts, (self.movement[1] - self.movement[0], 0), self.apos)
            self.player.render(self.display)

            if self.prevpos != self.player.pos:
                self.prevpos = self.player.pos.copy()
                if self.client:
                    msg = str(int(self.player.pos[0]))+";"+str(int(self.player.pos[1]))
                    self.client.sendMessage(msg)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    if self. client:
                        self.client.sendMessage("quit")

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        if not self.client:
                            self.client = Client('127.0.0.1', 9999)
                            self.client.startThread()
                            print("client started!")

                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.vel[1] = -3
                    if event.key == pygame.K_a:
                        self.apos = (100,100)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_a:
                        self.apos = None

            if self.client:
                self.pos2 = self.processMessage(self.client.getMessage("0;0"))

            self.display.blit(self.assets["player"], (self.pos2[0], self.pos2[1]))
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Game().run()