from settings import *
import pygame

class Sprite:
    def __init__(self, game, path, pos) -> None:
        self.player = game.player
        self.raycasting = game.raycasting
        self.x, self.y = pos
        self.path = path
        self.sprite = pygame.image.load(self.path)
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        self.ratio = self.sprite_width / self.sprite_height
    
    
    def get_sprite_projection(self, distance_to_player, screen_x):
        proj_height = (WALL_HEIGHT / distance_to_player) * WALL_HEIGHT
        sprite_height = proj_height
        sprite_width = sprite_height * self.ratio
        sprite = pygame.transform.scale(self.sprite, (int(sprite_width), int(sprite_height)))
        sprite_x = screen_x - sprite_width // 2
        sprite_y = HALF_HEIGHT - sprite_height // 2
        
        self.raycasting.objects_to_render.append((distance_to_player, sprite, (sprite_x, sprite_y)))
    
    def get_sprite(self):
        dx, dy = self.x - self.player.x, self.y - self.player.y
        theta = math.atan2(dy, dx)
        
        delta = theta - self.player.angle
                
        if delta < -math.pi:
            delta += math.tau
        elif delta > math.pi:
            delta -= math.tau
                
        
        delta_rays = delta / DELTA_ANGLE
        screen_x = ((NUM_RAYS // 2) + delta_rays) * SCALE
        distance_to_player = math.hypot(dx, dy)
        
        if -self.sprite_width // 2 < screen_x < WIDTH + self.sprite_width // 2:
            self.get_sprite_projection(distance_to_player, screen_x)
    
    def update(self):
        self.get_sprite()