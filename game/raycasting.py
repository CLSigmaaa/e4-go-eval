from settings import *
import math
import pygame

class Raycasting:
    def __init__(self, game) -> None:
        self.screen = game.screen
        self.player = game.player
        self.world_map = game.map.world_map
        self.wall_texture =  pygame.image.load('./ressources/textures/1.png')
        self.textures = {
            'W':  pygame.transform.scale(self.wall_texture, (TEXTURE_SIZE, TEXTURE_SIZE))
        }
        self.sky_offset = 0
        self.sky_texture = pygame.image.load('./ressources/textures/sky.png')
        self.sky_texture = pygame.transform.scale(self.sky_texture, (WIDTH, HEIGHT // 2))
    
    def mapping(self, a, b):
        return (a // CELL_SIZE) * CELL_SIZE, (b // CELL_SIZE) * CELL_SIZE
    
    def wall_casting(self):
        ox, oy = self.player.pos
        # On récupère la cellule dans laquelle se trouve le joueur
        x_map, y_map = (ox // CELL_SIZE) * CELL_SIZE, (oy // CELL_SIZE) * CELL_SIZE
        # On récupère l'angle de vue du joueur en commencant par l'angle le plus à gauche
        curr_angle = self.player.angle - HALF_FOV + 1e-6
        
        # On itère le nombre de rayons
        for ray in range(NUM_RAYS):
            # On calcule le cosinus et le sinus de l'angle actuel
            sin_a = math.sin(curr_angle)
            cos_a = math.cos(curr_angle)

            y, dy = (y_map + CELL_SIZE, 1) if sin_a >= 0 else (y_map, -1)
            texture_offset_x = 0  # Initialize texture_offset_y
            for _ in range(0, HEIGHT, CELL_SIZE):
                depth_h = (y - oy) / sin_a
                x = ox + depth_h * cos_a
                if self.mapping(x, y + dy) in self.world_map:
                    texture_offset_x = x % CELL_SIZE
                    break
                y += dy * CELL_SIZE
            
            x, dx = (x_map + CELL_SIZE, 1) if cos_a >= 0 else (x_map, -1)
            texture_offset_y = 0  # Initialize texture_offset_x
            for _ in range(0, WIDTH, CELL_SIZE):
                depth_v = (x - ox) / cos_a
                y = oy + depth_v * sin_a
                if self.mapping(x + dx, y) in self.world_map:
                    texture_offset_y = y % CELL_SIZE
                    break
                x += dx * CELL_SIZE
            

            # wall texture
            depth, offset, texture = (depth_v, texture_offset_y, 'W') if depth_v < depth_h else (depth_h, texture_offset_x, 'W')
            depth *= math.cos(self.player.angle - curr_angle)
            depth = max(depth, 0.00001)
            proj_height = (WALL_HEIGHT / depth) * WALL_HEIGHT
            wall_column = self.textures[texture].subsurface(offset * TEXTURE_SCALE,
                                            0, TEXTURE_SCALE, TEXTURE_SIZE)
            wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
            self.screen.blit(wall_column, (ray * SCALE, HALF_HEIGHT - proj_height // 2))
            curr_angle += DELTA_ANGLE
    
    def floor_casting(self):
        pygame.draw.rect(self.screen, (30, 30, 30), (0, HALF_HEIGHT, WIDTH, HEIGHT))
    
    def sky_casting(self):
        sky_offset = (self.player.angle * 1840) % WIDTH
        self.screen.blit(self.sky_texture, (-sky_offset, 0))
        self.screen.blit(self.sky_texture, (-sky_offset + WIDTH, 0))
    
    def draw(self):
        self.sky_casting()
        self.floor_casting()
        self.wall_casting()