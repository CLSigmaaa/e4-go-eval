from settings import * 
from map import *
from player import *
from raycasting import *
import pygame
import math
import time

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.prev_time = time.time()
        self.new_game()
        
    def new_game(self):
        self.player = Player(self)
        self.map = Map(self, self.player)
        self.map.generate_basic_map()
        self.map.generate_world_map()
        self.player.set_map(self.map.map)
        self.raycasting = Raycasting(self)
    
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
    def update(self, dt):
        self.player.update(dt)
        self.raycasting.draw()
        self.map.draw()
        pygame.display.flip()
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')
    
    def run(self):
        while True:
            self.check_events()
            self.delta_time = time.time() - self.prev_time
            self.prev_time = time.time()
            self.update(self.delta_time)
            self.clock.tick(MAX_FPS)
            
if __name__ == '__main__':
    game = Game()
    game.run()