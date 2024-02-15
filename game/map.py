import random
import pygame
from settings import *

class Map:
    def __init__(self, game, player) -> None:
        self.screen = game.screen
        self.player = player
        self.map = []
        self.world_map = set()
        self.mini_map = set()
        self.second_world_map = {}
        self.ennemies_map = {}
        self.max_map_width = WIDTH // CELL_SIZE
        self.max_map_height = HEIGHT // CELL_SIZE
        self.mini_map_surface = pygame.Surface((WIDTH // MINI_MAP_SCALE, (HEIGHT // MINI_MAP_SCALE)))
        
    def generate_basic_map(self):
        # for y in range(self.max_map_height):
        #     row = []
        #     for x in range(self.max_map_width):
        #         if x == 0 or x == self.max_map_width - 1 or y == 0 or y == self.max_map_height - 1:
        #             row.append('W')
        #         else:
        #             if random.random() < 0.05:  # Adjust the probability as needed
        #                 row.append('W')
        #             else:
        #                 row.append('.')
        #     self.map.append(row)
        
        self.map = [
            ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
            ['W', ' ', 'W', ' ', 'W', 'Y', ' ', ' ', 'W', ' ', ' ', 'Y', 'W', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', 'Y', 'W', ' ', 'W', 'Z', 'W'],
            ['W', ' ', 'W', ' ', 'W', 'W', 'W', ' ', ' ', ' ', 'W', 'W', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', 'W', ' ', ' ', 'W', 'Z', 'W'],
            ['W', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'W', 'W', ' ', 'W', 'W', ' ', 'W', ' ', 'W', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', 'W', ' ', 'W'],
            ['W', ' ', 'W', ' ', 'W', 'Y', 'W', ' ', ' ', 'X', ' ', ' ', 'W', ' ', 'W', ' ', ' ', 'Y', 'W', ' ', 'X', 'W', 'W', ' ', 'W', 'W', 'X', 'W'],
            ['W', 'W', ' ', ' ', 'W', 'W', ' ', ' ', 'W', 'W', ' ', ' ', 'W', ' ', ' ', ' ', 'W', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', 'X', 'W'],
            ['W', 'Y', 'W', ' ', 'X', ' ', ' ', ' ', 'W', ' ', 'W', ' ', ' ', 'X', 'W', ' ', 'W', ' ', 'W', 'W', ' ', 'W', 'W', ' ', ' ', 'W', 'X', 'W'],
            ['W', ' ', 'X', 'W', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', 'W', 'W', ' ', 'W', ' ', 'W', ' ', 'W', ' ', ' ', ' ', 'W', ' ', 'W', 'X', 'W'],
            ['W', ' ', ' ', 'W', ' ', 'W', ' ', 'W', 'Y', 'W', ' ', 'W', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', 'Y', 'W', ' ', 'W', ' ', 'W'],
            ['W', ' ', ' ', ' ', ' ', 'W', ' ', 'X', ' ', ' ', ' ', 'W', ' ', ' ', 'W', ' ', 'W', 'W', ' ', 'W', ' ', 'W', 'W', 'W', ' ', 'W', 'Y', 'W'],
            ['W', 'W', 'W', 'W', 'W', 'Y', 'W', ' ', 'W', 'W', 'W', 'W', ' ', 'W', ' ', 'W', ' ', 'W', ' ', ' ', 'W', 'W', ' ', ' ', ' ', 'W', 'Y', 'W'],
            ['W', 'Y', 'W', ' ', 'W', ' ', 'Y', 'W', ' ', 'W', ' ', 'W', ' ', 'W', ' ', ' ', ' ', ' ', 'W', 'W', ' ', ' ', 'W', 'W', ' ', 'W', 'Y', 'W'],
            ['W', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', 'W', ' ', 'W', ' ', ' ', 'W', ' ', 'W', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'W', ' ', 'W'],
            ['W', ' ', 'W', 'W', ' ', 'W', ' ', ' ', 'W', ' ', 'Z', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', ' ', 'W', 'Z', 'W', ' ', 'W'],
            ['W', ' ', ' ', 'Y', 'W', ' ', ' ', 'W', ' ', ' ', 'Y', 'W', 'W', 'W', ' ', ' ', ' ', ' ', 'W', ' ', 'W', 'W', ' ', ' ', 'W', 'W', ' ', 'W'],
            ['W', ' ', 'W', 'W', 'X', 'W', ' ', 'W', ' ', 'W', ' ', 'W', ' ', 'X', 'W', ' ', 'W', 'W', ' ', ' ', ' ', 'W', 'W', 'W', ' ', 'W', ' ', 'W'],
            ['W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', ' ', ' ', 'W', ' ', 'W'],
            ['W', 'W', ' ', ' ', ' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'Z', ' ', 'W', ' ', ' ', 'W', 'W', ' ', 'W', ' ', 'W'],
            ['W', ' ', ' ', 'W', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', 'W', ' ', 'W', ' ', ' ', 'W', 'W', ' ', ' ', ' ', ' ', ' ', 'W', ' ', 'W'],
            ['W', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'W', ' ', 'W', 'W', 'W', ' ', 'W'],
            ['W', ' ', 'Z', ' ', ' ', ' ', 'W', 'X', ' ', ' ', ' ', ' ', 'Z', ' ', ' ', ' ', 'W', ' ', ' ', ' ', 'W', ' ', 'Z', ' ', ' ', ' ', 'Y', 'W'],
            ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
        ]
        
        return self.map
    
    def generate_world_map(self):
        for j, row in enumerate(self.map):
            for i, char in enumerate(row):
                if char == 'W':
                    self.world_map.add((i * CELL_SIZE, j * CELL_SIZE))
                    self.second_world_map[(i, j)] = 'W'
                    self.mini_map.add((i * MINI_MAP_TILE, j * MINI_MAP_TILE))
                elif char == 'X':
                    self.ennemies_map[(i * CELL_SIZE + HALF_CELL_SIZE // 2, j * CELL_SIZE + HALF_CELL_SIZE // 2)] = 'X'
                elif char == 'Y':
                    self.ennemies_map[(i * CELL_SIZE + HALF_CELL_SIZE // 2, j * CELL_SIZE + HALF_CELL_SIZE // 2)] = 'Y'
                elif char == 'Z':
                    self.ennemies_map[(i * CELL_SIZE + HALF_CELL_SIZE // 2, j * CELL_SIZE + HALF_CELL_SIZE // 2)] = 'Z'
    
    def draw(self):
        pass
        # Create a surface for the mini map
        # self.mini_map_surface.fill((0, 0, 0))
        
        # # set the alpha
        # self.mini_map_surface.set_alpha(300)
        
        # # draw the player
        # pygame.draw.circle(self.mini_map_surface, pygame.Color('red'), (int(self.player.x // MINI_MAP_SCALE), int(self.player.y // MINI_MAP_SCALE)), 5)
        
        # # draw the walls
        # for x, y in self.mini_map:
        #     pygame.draw.rect(self.mini_map_surface, (255, 255, 255), (x, y, MINI_MAP_TILE, MINI_MAP_TILE), 2)

        # # Draw the mini map on the screen
        # self.screen.blit(self.mini_map_surface, MINI_MAP_POS)