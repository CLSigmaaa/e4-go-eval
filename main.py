import pygame
import math

WIDTH = 1200
HEIGHT = 700

FOV = math.pi / 3
HALF_FOV = FOV / 2

NUM_RAYS = 200
DELTA_ANGLE = FOV / NUM_RAYS

SCREEN_DIST = WIDTH / 2*math.tan(HALF_FOV)
PROJ_COEFF = 2*SCREEN_DIST*100
SCALE = WIDTH // NUM_RAYS


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
            world_map.add((i * 100, j * 100))

class Player:
    def __init__(self) -> None:
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.angle = 0
        self.player_speed = 3
        
    @property
    def pos(self):
        return self.x, self.y
    
    def movement(self):
        current_x_pos, current_y_pos = self.pos
        # collision detection
        # if map[int(current_y_pos // 100)][int(current_x_pos // 100)] == 'W':
        #     self.x, self.y = current_x_pos - 2 * self.player_speed * math.cos(self.angle), current_y_pos - 2 * self.player_speed * math.sin(self.angle)
            
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += self.player_speed * cos_a
            self.y += self.player_speed * sin_a
        if keys[pygame.K_s]:
            self.x += -self.player_speed * cos_a
            self.y += -self.player_speed * sin_a
        if keys[pygame.K_a]:
            self.x += self.player_speed * sin_a
            self.y += -self.player_speed * cos_a
        if keys[pygame.K_d]:
            self.x += -self.player_speed * sin_a
            self.y += self.player_speed * cos_a
        if keys[pygame.K_LEFT]:
            self.angle -= 0.05
        if keys[pygame.K_RIGHT]:
            self.angle += 0.05
    


player = Player()


def ray_cast(player: Player):
    curr_angle = player.angle - HALF_FOV
    pos_x, pos_y = player.pos
    for ray in range(NUM_RAYS):
        sin_a = math.sin(curr_angle)
        cos_a = math.cos(curr_angle)
        for depth in range(WIDTH):
            x = pos_x + depth * cos_a
            y = pos_y + depth * sin_a
            map_x, map_y = int(x // 100), int(y // 100)
            if (0 <= map_x < len(map[0])) and (0 <= map_y < len(map)):
                if map[map_y][map_x] == 'W':
                    # pygame.draw.circle(sc, (0, 255, 255), (int(x), int(y)), 2)
                    depth *= math.cos(player.angle - curr_angle) # fix the fisheye effect
                    proj_height = PROJ_COEFF / (depth + 0.00001)
                    c = 255 / (1 + depth * depth * 0.00001)
                    color = (63 + c // 2, 63 + c // 2, 63 +c // 2)
                    pygame.draw.rect(sc, color, (ray * SCALE, (HEIGHT // 2) - proj_height // 2, SCALE, proj_height ))
                    break
        curr_angle += DELTA_ANGLE


while True:
    # dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    player.movement()
    sc.fill((0, 0, 0))
    
    """ # draw the player
    pygame.draw.circle(sc, (255, 255, 255), (int(player.x), int(player.y)), 10)
    
    # draw the player direction
    pygame.draw.line(sc, (255, 255, 255), player.pos, (player.x + WIDTH * math.cos(player.angle), player.y + WIDTH * math.sin(player.angle)))
    
    # draw the player FOV
    pygame.draw.line(sc, (255, 255, 255), player.pos, (player.x + WIDTH * math.cos(player.angle + HALF_FOV), player.y + WIDTH * math.sin(player.angle + HALF_FOV)))
    pygame.draw.line(sc, (255, 255, 255), player.pos, (player.x + WIDTH * math.cos(player.angle - HALF_FOV), player.y + WIDTH * math.sin(player.angle - HALF_FOV)))
    
    # draw the walls
    for x, y in world_map:
        pygame.draw.rect(sc, (255, 255, 255), (x, y, 100, 100), 2) """
    # draw background
    pygame.draw.rect(sc, (0, 255, 0), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
    pygame.draw.rect(sc, (0, 0, 255), (0, 0, WIDTH, HEIGHT // 2))
    
    # draw the rays
    ray_cast(player)
        
    # show the player variables on screen
    # font = pygame.font.SysFont('Arial', 20, bold=True)
    # text_fps = font.render('FPS : ' + str(int(clock.get_fps())), True, pygame.Color('white'))
    # text_x = font.render('Player X:' + str(int(player.x)), True, pygame.Color('white'))
    # text_y = font.render('Player Y: ' + str(int(player.y)), True, pygame.Color('white'))
    # text_angle = font.render('Player Angle : ' + str(int(math.degrees(player.angle) % 360)), True, pygame.Color('white'))
    # sc.blit(text_fps, (50, 50))
    # sc.blit(text_x, (50, 100))
    # sc.blit(text_y, (50, 150))
    # sc.blit(text_angle, (50, 200))
    
    
    pygame.display.flip()
    clock.tick(60)