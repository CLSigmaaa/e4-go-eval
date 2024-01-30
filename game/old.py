import pygame
import math
import time
import numpy as np
import random

from settings import *
from map import *

pygame.init()

wall_texture = pygame.image.load('./ressources/textures/1.png')
wall_texture = pygame.transform.scale(wall_texture, (TEXTURE_SIZE, TEXTURE_SIZE))
sky_texture = pygame.image.load('./ressources/textures/sky.png')
sky_texture = pygame.transform.scale(sky_texture, (WIDTH, HEIGHT // 2))
sky_offset = 0

textures = {
    'W': wall_texture
}

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

# map = [
#     ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
#     ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
#     ['W', '.', '.', 'W', 'W', 'W', '.', '.', '.', 'W', '.', 'W'],
#     ['W', 'W', '.', '.', 'W', '.', '.', '.', '.', '.', '.', 'W'],
#     ['W', '.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', 'W'],
#     ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
#     ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']
# ]

def generate_basic_map(width, height, cell_size):
    max_map_width = width // cell_size
    max_map_height = height // cell_size
    
    map = []
    for y in range(max_map_height):
        row = []
        for x in range(max_map_width):
            if x == 0 or x == max_map_width - 1 or y == 0 or y == max_map_height - 1:
                row.append('W')
            else:
                if random.random() < 0.2:  # Adjust the probability as needed
                    row.append('W')
                else:
                    row.append('.')
        map.append(row)
    return map

map = generate_basic_map(WIDTH, HEIGHT, CELL_SIZE)

MAX_DEPTH = 20

world_map = set()
mini_map = set()
for j, row in enumerate(map):
    for i, char in enumerate(row):
        if char == 'W':
            world_map.add((i * CELL_SIZE, j * CELL_SIZE))
            mini_map.add((i * MINI_MAP_TILE, j * MINI_MAP_TILE))

class Player:
    def __init__(self) -> None:
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.angle = 0
        self.player_speed = 150
        self.rel = None
        self.diag_corr = 1 / math.sqrt(2)
        
    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x // CELL_SIZE), int(self.y // CELL_SIZE)
    
    def get_rel(self):
        return self.rel
    
    def movement(self, dt):
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            new_x = self.x + self.player_speed * cos_a * dt
            new_y = self.y + self.player_speed * sin_a * dt
            if not self.check_collision(new_x, new_y):
                self.x = new_x
                self.y = new_y
        if keys[pygame.K_s]:
            new_x = self.x - self.player_speed * cos_a * dt
            new_y = self.y - self.player_speed * sin_a * dt
            if not self.check_collision(new_x, new_y):
                self.x = new_x
                self.y = new_y
        if keys[pygame.K_a]:
            new_x = self.x + self.player_speed * sin_a * dt
            new_y = self.y - self.player_speed * cos_a * dt
            if not self.check_collision(new_x, new_y):
                self.x = new_x
                self.y = new_y
        if keys[pygame.K_d]:
            new_x = self.x - self.player_speed * sin_a * dt
            new_y = self.y + self.player_speed * cos_a * dt
            if not self.check_collision(new_x, new_y):
                self.x = new_x
                self.y = new_y

    def mouse_control(self, dt):
        mx, my = pygame.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * dt
    
    # TODO: Fix the collision, i can pass through diagonal walls
    def check_collision(self, x, y):
        map_x, map_y = int(x // CELL_SIZE), int(y // CELL_SIZE)
        if (0 <= map_x < len(map[0])) and (0 <= map_y < len(map)):
            if map[map_y][map_x] == 'W':
                return True
        return False
    

player = Player()

def mapping(a, b):
    return (a // CELL_SIZE) * CELL_SIZE, (b // CELL_SIZE) * CELL_SIZE

def mini_mapping(a, b):
    return (a // MINI_MAP_TILE) * MINI_MAP_TILE, (b // MINI_MAP_TILE) * MINI_MAP_TILE

def display_mini_map():
    def mini_mapping(a, b):
        return (a // MINI_MAP_TILE) * MINI_MAP_TILE, (b // MINI_MAP_TILE) * MINI_MAP_TILE
    
    # Create a surface for the mini map
    mini_map_surface = pygame.Surface((WIDTH // MINI_MAP_SCALE, WIDTH // MINI_MAP_SCALE))
    
    # set the alpha
    mini_map_surface.set_alpha(300)
    
    # draw the player
    pygame.draw.circle(mini_map_surface, pygame.Color('red'), (int(player.x // MINI_MAP_SCALE), int(player.y // MINI_MAP_SCALE)), 5)
    
    # draw the fov
    # pygame.draw.line(mini_map_surface, pygame.Color('white'), (player.x // MINI_MAP_SCALE, player.y // MINI_MAP_SCALE), ((player.x + WIDTH // MINI_MAP_SCALE * math.cos(player.angle - HALF_FOV)) // MINI_MAP_SCALE, (player.y + WIDTH // MINI_MAP_SCALE * math.sin(player.angle - HALF_FOV)) // MINI_MAP_SCALE), 2)
    # pygame.draw.line(mini_map_surface, pygame.Color('white'), (player.x // MINI_MAP_SCALE, player.y // MINI_MAP_SCALE), ((player.x + WIDTH // MINI_MAP_SCALE * math.cos(player.angle + HALF_FOV)) // MINI_MAP_SCALE, (player.y + WIDTH // MINI_MAP_SCALE * math.sin(player.angle + HALF_FOV)) // MINI_MAP_SCALE), 2)
    
    # draw the walls
    for x, y in mini_map:
        pygame.draw.rect(mini_map_surface, (255, 255, 255), (x, y, MINI_MAP_TILE, MINI_MAP_TILE), 2)

    # Draw the mini map on the screen
    sc.blit(mini_map_surface, MINI_MAP_POS)



def ray_cast(player: Player):
    # draw background
    # pygame.draw.rect(sc, (0, 255, 0), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
    pygame.draw.rect(sc, (30, 30, 30), (0, HALF_HEIGHT, WIDTH, HEIGHT))

    # draw sky
    sky_offset = (player.angle * 1840) % WIDTH

    sc.blit(sky_texture, (-sky_offset, 0))
    sc.blit(sky_texture, (-sky_offset + WIDTH, 0))
    
    # On récupère la position du joueur
    ox, oy = player.pos
    # On récupère la cellule dans laquelle se trouve le joueur
    x_map, y_map = (ox // CELL_SIZE) * CELL_SIZE, (oy // CELL_SIZE) * CELL_SIZE
    # On récupère l'angle de vue du joueur en commencant par l'angle le plus à gauche
    curr_angle = player.angle - HALF_FOV + 1e-6
    
    # On itère le nombre de rayons
    for ray in range(NUM_RAYS):
        # On calcule le cosinus et le sinus de l'angle actuel
        sin_a = math.sin(curr_angle)
        cos_a = math.cos(curr_angle)

        y, dy = (y_map + CELL_SIZE, 1) if sin_a >= 0 else (y_map, -1)
        for _ in range(0, HEIGHT, CELL_SIZE):
            depth_h = (y - oy) / sin_a
            x = ox + depth_h * cos_a
            if mapping(x, y + dy) in world_map:
                texture_offset_x = x % CELL_SIZE
                break
            y += dy * CELL_SIZE
        
        x, dx = (x_map + CELL_SIZE, 1) if cos_a >= 0 else (x_map, -1)
        for _ in range(0, WIDTH, CELL_SIZE):
            depth_v = (x - ox) / cos_a
            y = oy + depth_v * sin_a
            if mapping(x + dx, y) in world_map:
                texture_offset_y = y % CELL_SIZE
                break
            x += dx * CELL_SIZE
        

        # wall texture
        depth, offset, texture = (depth_v, texture_offset_y, 'W') if depth_v < depth_h else (depth_h, texture_offset_x, 'W')
        depth *= math.cos(player.angle - curr_angle)
        depth = max(depth, 0.00001)
        proj_height = (WALL_HEIGHT / depth) * WALL_HEIGHT
        wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE,
                                        0, TEXTURE_SCALE, TEXTURE_SIZE)
        wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
        sc.blit(wall_column, (ray * SCALE, HALF_HEIGHT - proj_height // 2))
        curr_angle += DELTA_ANGLE


prev_time = time.time()
while True:
    clock.tick(MAX_FPS)
    
    dt = time.time() - prev_time
    prev_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    player.movement(dt)
    player.mouse_control(dt)
    # sc.fill((0, 0, 0))

    # no_ray_cast(player)
    ray_cast(player)
    
    display_mini_map()

    # Debug info
    font = pygame.font.SysFont('Arial', 20, bold=True)
    text_fps = font.render('FPS : ' + str(int(clock.get_fps())), True, pygame.Color('white'))
    # text_x = font.render('Player X:' + str(int(player.x)), True, pygame.Color('white'))
    # text_y = font.render('Player Y: ' + str(int(player.y)), True, pygame.Color('white'))
    # map_pos = player.map_pos
    # text_map_x = font.render('Player Map Pos X: ' + str(map_pos[0]), True, pygame.Color('white'))
    # text_map_y = font.render('Player Map Pos Y: ' + str(map_pos[1]), True, pygame.Color('white'))
    # text_angle = font.render('Player Angle : ' + str(int(math.degrees(player.angle) % 360)), True, pygame.Color('white'))
    # text_player_rel_x = font.render('Player Rel X : ' + str(player.get_rel()), True, pygame.Color('white'))
    # sc.blit(text_player_rel_x, (50, 350))
    sc.blit(text_fps, (50, 50))
    # sc.blit(text_angle, (50, 200))
    # sc.blit(text_map_x, (50, 250))
    # sc.blit(text_map_y, (50, 300))
    
    pygame.display.flip()
