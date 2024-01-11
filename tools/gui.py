import pygame

class button():
    def __init__(self, width, height, func, x=0, y=0, color=(255, 255, 255, 150), highlightColor=(255, 0, 255, 250), pos=[200, 200]):
        self.color = color
        self.highlightColor = highlightColor

        self.highlight = False
        self.pos = pos
        
        self.Rect = pygame.Rect(x, y, width, height)

        self.func = func

    def render(self, surface, scrollpos):
        renRect = self.Rect.copy()
        renRect.y -= scrollpos
        if self.highlight:
            pygame.draw.rect(surface, self.highlightColor, renRect)
        else:
            pygame.draw.rect(surface, self.color, renRect)

    def update(self, event, curserpos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.Rect.collidepoint(curserpos[0]-self.pos[0], curserpos[1]-self.pos[1]):
                self.func()
        if event.type == pygame.MOUSEMOTION:
            if self.Rect.collidepoint(curserpos[0]-self.pos[0], curserpos[1]-self.pos[1]):
                self.highlight = True
            else:
                self.highlight = False

def trangleCords(pos, size, color, shape=((0,1),(1,1),(1,0))):
    p1 = (pos[0]+(shape[0][0]*size), pos[1]+(shape[0][1]*size))
    p2 = (pos[0]+(shape[1][0]*size), pos[1]+(shape[1][1]*size))
    p3 = (pos[0]+(shape[2][0]*size), pos[1]+(shape[2][1]*size))
        
    return (color, (p1, p2, p3))

class window():
    def __init__(self, width, height, title, font='Comic Sans MS', pos=[200, 200]):
        self.display = pygame.Surface((width, height)).convert_alpha()
        self.display.fill((0, 0, 0, 0))

        self.action = "none"

        self.width = width
        self.height = height

        self.toprect = pygame.Rect(0, 0, width, 20)
        self.rect = pygame.Rect(0, 0, width, height)
        self.scroll = pygame.Rect(width-5, self.toprect.bottom+5, 10, height/5)
        self.scrollpos = 0
        self.extri = [[width-15, height-15], (15), (255, 0, 0)]
        self.triRect = pygame.draw.polygon(self.display, *trangleCords(*self.extri))

        self.font = pygame.font.SysFont(font, 15)
        self.titleText = title
        self.pos = pos
        self.circle = ((0, 0, 0, 150), (15, 11), 7)

        pygame.draw.rect(self.display, (0, 0, 0, 150), self.rect, border_radius=10)
        pygame.draw.rect(self.display, (39, 61, 227, 250), self.toprect, border_top_left_radius=10, border_top_right_radius=10)
        pygame.draw.circle(self.display, self.circle[0], self.circle[1], self.circle[2])

        self.title = self.font.render(title, True, (0, 0, 0))

        self.btns = {}
        self.texts = {}
        self.renderItems = 0

        self.bottom = self.toprect.bottom+10

        self.display.blit(self.title, (30,-1))

    def render(self, screen):
        self.display.fill((0, 0, 0, 0))

        pygame.draw.rect(self.display, (0, 0, 0, 150), self.rect, border_radius=10)

        for order in range(self.renderItems):
            if self.btns.get(order, None):
                self.btns[order].render(self.display, self.scrollpos)
            if self.texts.get(order, None):
                pos = (self.texts[order][1][0], self.texts[order][1][1]-self.scrollpos)
                self.display.blit(self.texts[order][0], pos)    
        
        pygame.draw.rect(self.display, (39, 61, 227, 250), self.toprect, border_top_left_radius=10, border_top_right_radius=10)
        pygame.draw.circle(self.display, self.circle[0], self.circle[1], self.circle[2])
        pygame.draw.rect(self.display, (0, 0, 0), self.scroll)

        self.triRect = pygame.draw.polygon(self.display, *trangleCords(*self.extri))

        self.display.blit(self.title, (30,-1))
        screen.blit(self.display, self.pos)

    def update(self, event, curserpos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.clicked(curserpos[0], curserpos[1])
            if self.scroll.collidepoint(curserpos[0]-self.pos[0], curserpos[1]-self.pos[1]):
                self.action = "scroll"
            if self.triRect.collidepoint(curserpos[0]-self.pos[0], curserpos[1]-self.pos[1]):
                self.action = "stretch"

        if event.type == pygame.MOUSEMOTION:
            if self.action == "move":
                self.pos[0] += event.rel[0]
                self.pos[1] += event.rel[1]
            if self.action == "stretch":
                self.extri[0][0] += event.rel[0]
                self.extri[0][1] += event.rel[1]
                self.width += event.rel[0]
                self.height += event.rel[1]
                self.display = pygame.Surface((self.width,self.height)).convert_alpha()
                self.toprect.width = self.width
                self.rect.width = self.width
                self.rect.height = self.height
                self.scroll.x = self.width-5
                self.scrollSize()
            if self.action == "scroll":
                if event.rel[1] < 0:
                    if (self.scroll.y >= self.toprect.bottom+3):
                        self.scroll.y += event.rel[1]
                        self.scrollpos += event.rel[1]
                else:
                    if (self.scroll.bottom <= self.height-7-5):
                        self.scroll.y += event.rel[1]
                        self.scrollpos += event.rel[1]
                if self.scroll.y < self.toprect.bottom+4:
                    self.scroll.y = self.toprect.bottom+4
                if self.scroll.bottom > self.height-7:
                    self.scroll.bottom = self.height-7
                if self.scrollpos < 0:
                    self.scrollpos = 0
                if self.scrollpos > self.bottom-self.toprect.bottom+10:
                    self.scrollpos = self.height-7 - self.toprect.bottom+3+3

        if event.type == pygame.MOUSEBUTTONUP:
            self.action = "none"
        
        for btn in self.btns:
            self.btns[btn].update(event, curserpos)

    def clicked(self, x, y):
        x = x-self.pos[0]
        y = y-self.pos[1]
        if self.rect.collidepoint(x, y):
            if self.toprect.collidepoint(x, y):
                self.action = "move"

    def scrollSize(self):
        size = ((self.height-self.toprect.bottom-7)/(self.bottom-self.toprect.bottom))*(self.height-self.toprect.bottom)
        print("size before cap: ", size)
        # if size > (self.height-self.toprect.bottom)-7:
        #     size = 76
        # if size < 1:
        #     size = 1
        self.scroll.height = size
        print("height: ", (self.height-self.toprect.bottom-7))
        print("info size: ", (self.bottom-self.toprect.bottom))
        print("scroll size: ", size)

    def addText(self, text, color, font='Comic Sans MS', size=15, pos=None):
        font = pygame.font.SysFont(font, size)
        if pos:
            pos = (pos[0], pos[1])
            self.texts[self.renderItems] = (font.render(text, True, color, wraplength=self.width-10), pos, size)
        else:
            pos = (10, self.bottom)
            self.texts[self.renderItems] = (font.render(text, True, color, wraplength=self.width-10), pos, size)
        self.bottom += self.texts[self.renderItems][0].get_rect().height + 10
        self.renderItems += 1
        self.scrollSize()
    
    def addButton(self, color, highlightColor, function, width, height, pos = None):
        if pos:
            self.btns[self.renderItems] = button(width, height, function, pos[0], pos[1], color, highlightColor, self.pos)
        else:
            x = 10
            y = self.bottom
            self.btns[self.renderItems] = button(width, height, function, x, y, color, highlightColor, self.pos)
        self.bottom += height+10
        self.renderItems += 1
        self.scrollSize()


pygame.init()
pygame.font.init()
pygame.display.set_caption("unseen forces")
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
running = True

win = window(200, 100, "Hello World")
win.addButton((255, 255, 255), (0, 0, 0), lambda : print("clicked"), 100, 20)
win.addText("test jkfgjdbfbdgfnbfgb d d i; gbndm fgbdglkn bdfbg;l bdgfbv;dfkln bdfvgbc;lxknbg fmbdf;lkbnmd bd.gf fgkl.bnm vfbd.km dfbgndmf,gb", (0, 0, 0))
win.addButton((255, 255, 255), (0, 0, 0), lambda : print("clicked"), 100, 20)

while running:
    screen.fill((255, 255, 255))
    win.render(screen)
    curserpos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        win.update(event, curserpos)
        

    pygame.display.update()
    clock.tick(60)