import pygame
import math
import time
import numpy as np

WIDTH = 1200
HALF_WIDTH = WIDTH // 2
HEIGHT = 700
HALF_HEIGHT = HEIGHT // 2

FOV = math.pi / 3
HALF_FOV = FOV / 2

CELL_SIZE = 100

NUM_RAYS = WIDTH // 5
DELTA_ANGLE = FOV / NUM_RAYS

DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 2 * DIST * CELL_SIZE
SCALE = WIDTH // NUM_RAYS

MAX_FPS = 300

pygame.init()

sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

map = [
    ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
    ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
    ['W', '.', '.', 'W', 'W', 'W', '.', '.', '.', 'W', '.', 'W'],
    ['W', 'W', '.', '.', 'W', '.', '.', '.', '.', '.', '.', 'W'],
    ['W', '.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', 'W'],
    ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
    ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']
]

MAX_DEPTH = 20

world_map = set()
for j, row in enumerate(map):
    for i, char in enumerate(row):
        if char == 'W':
            world_map.add((i * CELL_SIZE, j * CELL_SIZE))

class Player:
    def __init__(self) -> None:
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.angle = 0
        self.player_speed = 150
        
    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x // CELL_SIZE), int(self.y // CELL_SIZE)
    
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
        if keys[pygame.K_LEFT]:
            self.angle -= 2.25 * dt
        if keys[pygame.K_RIGHT]:
            self.angle += 2.25 * dt

    def check_collision(self, x, y):
        map_x, map_y = int(x // CELL_SIZE), int(y // CELL_SIZE)
        if (0 <= map_x < len(map[0])) and (0 <= map_y < len(map)):
            if map[map_y][map_x] == 'W':
                return True
        return False
    

player = Player()

def mapping(a, b):
    return (a // CELL_SIZE) * CELL_SIZE, (b // CELL_SIZE) * CELL_SIZE


def ray_cast(player: Player):
    # draw background
    pygame.draw.rect(sc, (0, 255, 0), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
    pygame.draw.rect(sc, (0, 0, 255), (0, 0, WIDTH, HEIGHT // 2))
    
    ox, oy = player.pos
    x_map, y_map = (ox // CELL_SIZE) * CELL_SIZE, (oy // CELL_SIZE) * CELL_SIZE
    curr_angle = player.angle - HALF_FOV + 1e-6
    
    for ray in range(NUM_RAYS):
        sin_a = math.sin(curr_angle)
        cos_a = math.cos(curr_angle)
        
        # vertical line
        x, dx = (x_map + CELL_SIZE, 1) if cos_a >= 0 else (x_map, -1)
        for _ in range(0, WIDTH, CELL_SIZE):
            depth_v = (x - ox) / cos_a
            y = oy + depth_v * sin_a
            if mapping(x + dx, y) in world_map:
                break
            x += dx * CELL_SIZE
        
        # horizontal line
        y, dy = (y_map + CELL_SIZE, 1) if sin_a >= 0 else (y_map, -1)
        for _ in range(0, HEIGHT, CELL_SIZE):
            depth_h = (y - oy) / sin_a
            x = ox + depth_h * cos_a
            if mapping(x, y + dy) in world_map:
                break
            y += dy * CELL_SIZE
            
            
        depth = depth_v if depth_v < depth_h else depth_h
        depth *= math.cos(player.angle - curr_angle)
        proj_height = PROJ_COEFF / depth
        c = 255 / (1 + depth * depth * 0.00001)
        color = (63 + c // 2, 63 + c // 2, 63 +c // 2)
        pygame.draw.rect(sc, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

        curr_angle += DELTA_ANGLE

def no_ray_cast(player: Player):
    # draw the player
    pygame.draw.circle(sc, (255, 255, 255), (int(player.x), int(player.y)), 10)
    
    # draw the player direction
    pygame.draw.line(sc, (255, 255, 255), player.pos, (player.x + WIDTH * math.cos(player.angle), player.y + WIDTH * math.sin(player.angle)))
    
    # draw the player FOV
    pygame.draw.line(sc, (255, 255, 255), player.pos, (player.x + WIDTH * math.cos(player.angle + HALF_FOV), player.y + WIDTH * math.sin(player.angle + HALF_FOV)))
    pygame.draw.line(sc, (255, 255, 255), player.pos, (player.x + WIDTH * math.cos(player.angle - HALF_FOV), player.y + WIDTH * math.sin(player.angle - HALF_FOV)))
    
    # draw the walls
    for x, y in world_map:
        pygame.draw.rect(sc, (255, 255, 255), (x, y, CELL_SIZE, CELL_SIZE), 2)


prev_time = time.time()
while True:
    clock.tick(MAX_FPS)
    
    dt = time.time() - prev_time
    prev_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    player.movement(dt)
    sc.fill((0, 0, 0))

    # no_ray_cast(player)
    ray_cast(player)
    
    # Debug info
    font = pygame.font.SysFont('Arial', 20, bold=True)
    text_fps = font.render('FPS : ' + str(int(clock.get_fps())), True, pygame.Color('white'))
    text_x = font.render('Player X:' + str(int(player.x)), True, pygame.Color('white'))
    text_y = font.render('Player Y: ' + str(int(player.y)), True, pygame.Color('white'))
    map_pos = player.map_pos
    text_map_x = font.render('Player Map Pos X: ' + str(map_pos[0]), True, pygame.Color('white'))
    text_map_y = font.render('Player Map Pos Y: ' + str(map_pos[1]), True, pygame.Color('white'))
    text_angle = font.render('Player Angle : ' + str(int(math.degrees(player.angle) % 360)), True, pygame.Color('white'))
    sc.blit(text_fps, (50, 50))
    sc.blit(text_x, (50, 100))
    sc.blit(text_y, (50, 150))
    sc.blit(text_angle, (50, 200))
    sc.blit(text_map_x, (50, 250))
    sc.blit(text_map_y, (50, 300))
    
    pygame.display.flip()