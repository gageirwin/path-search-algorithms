import pygame, sys
from src.settings import *
from src.game import Maze

class Window:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.game = Maze()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black')
            self.game.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    window = Window()
    window.run()