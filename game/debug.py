import pygame

class Debug:
    def __init__(self, game):
        self.font = pygame.font.SysFont('Arial', 20, bold=True)
        self.clock = game.clock
        self.screen = game.screen
    
    def draw(self):
        text_fps = self.font.render('FPS : ' + str(int(self.clock.get_fps())), True, pygame.Color('white'))
        self.screen.blit(text_fps, (10, 10))