import pygame
import pygame_gui

pygame.init()
pygame.display.set_caption("unseen forces")
screen = pygame.display.set_mode((900, 600))

manager = pygame_gui.UIManager((900, 600))

clock = pygame.time.Clock()
running = True

while running:
    screen.fill((255, 0 , 0))
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)

    manager.update(time_delta)

    manager.draw_ui(screen)
    
    pygame.display.update()
    clock.tick(60)
            
            