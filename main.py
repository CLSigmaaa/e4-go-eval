import pygame
import math
import time

WIDTH = 1200
HEIGHT = 700

FOV = math.pi / 3
HALF_FOV = FOV / 2

CELL_SIZE = 100

NUM_RAYS = 100
DELTA_ANGLE = FOV / NUM_RAYS

SCREEN_DIST = WIDTH / 2*math.tan(HALF_FOV)
PROJ_COEFF = 2*SCREEN_DIST*CELL_SIZE
SCALE = WIDTH // NUM_RAYS

MAX_FPS = 600

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

def ray_cast(player: Player):
    # draw background
    pygame.draw.rect(sc, (0, 255, 0), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
    pygame.draw.rect(sc, (0, 0, 255), (0, 0, WIDTH, HEIGHT // 2))
    
    # actual ray casting
    curr_angle = player.angle - HALF_FOV
    pos_x, pos_y = player.pos
    for ray in range(NUM_RAYS):
        sin_a = math.sin(curr_angle)
        cos_a = math.cos(curr_angle)
        for depth in range(int(WIDTH)):
            x = pos_x + depth * cos_a
            y = pos_y + depth * sin_a
            map_x, map_y = int(x // CELL_SIZE), int(y // CELL_SIZE)
            if (0 <= map_x < len(map[0])) and (0 <= map_y < len(map)):
                if map[map_y][map_x] == 'W':
                    depth *= math.cos(player.angle - curr_angle) # fix the fisheye effect
                    proj_height = PROJ_COEFF / (depth + 0.00001)
                    c = 255 / (1 + depth * depth * 0.00001)
                    color = (63 + c // 2, 63 + c // 2, 63 +c // 2)
                    pygame.draw.rect(sc, color, (ray * SCALE, (HEIGHT // 2) - proj_height // 2, SCALE, proj_height ))
                    break
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
    text_angle = font.render('Player Angle : ' + str(int(math.degrees(player.angle) % 360)), True, pygame.Color('white'))
    sc.blit(text_fps, (50, 50))
    sc.blit(text_x, (50, 100))
    sc.blit(text_y, (50, 150))
    sc.blit(text_angle, (50, 200))
    
    pygame.display.flip()