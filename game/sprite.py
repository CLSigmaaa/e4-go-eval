from settings import *
import pygame
from collections import deque
import os
import math

class Sprite:
    def __init__(self, game, pos, path='./ressources/sprites/static/candlebra.png', height_shift=0.27) -> None:
        self.game = game
        self.player = game.player
        self.raycasting = game.raycasting
        self.x, self.y = pos
        self.path = path
        self.sprite = pygame.image.load(self.path)
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        self.half_sprite_width = self.sprite_width // 2
        self.half_sprite_height = self.sprite_height // 2
        self.ratio = self.sprite_width / self.sprite_height
        self.height_shift = height_shift
        self.screen_x = 0
        self.distance_to_player = 1e-6
    
    
    def get_sprite_projection(self):
        self.distance_to_player = max(self.distance_to_player, 1e-6)
        proj_height = (WALL_HEIGHT / self.distance_to_player) * WALL_HEIGHT

        if not proj_height > WIDTH:
            sprite_height = proj_height
            sprite_width = sprite_height* self.ratio

            sprite = pygame.transform.scale(self.sprite, (int(sprite_width), int(sprite_height)))

            sprite_pos = (self.screen_x - sprite_width // 2, HALF_HEIGHT - sprite_height // 2)

            self.raycasting.objects_to_render.append((self.distance_to_player, sprite, sprite_pos))
    
    def get_sprite(self):
        dx, dy = self.x - self.player.x, self.y - self.player.y
        theta = math.atan2(dy, dx)
        
        # display theta on the screen
        font = pygame.font.SysFont('Arial', 20, bold=True)
        text_theta = font.render('theta : ' + str(theta), True, pygame.Color('white'))
        self.game.screen.blit(text_theta, (10, 40))
        
        
        delta = (theta - self.player.angle)
        
        text_delta = font.render('delta : ' + str(delta), True, pygame.Color('white'))
        self.game.screen.blit(text_delta, (10, 60))
        
        # TODO: Fix the sky clipping when delta angle is out of range
        if delta < -math.pi:
            delta += math.tau
        elif delta > math.pi:
            delta -= math.tau
        
        delta_rays = delta / DELTA_ANGLE
        
        text_delta_rays = font.render('delta_rays : ' + str(delta_rays), True, pygame.Color('white'))
        self.game.screen.blit(text_delta_rays, (10, 80))
        
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE
        
        text_screen_x = font.render('screen_x : ' + str(self.screen_x), True, pygame.Color('white'))
        self.game.screen.blit(text_screen_x, (10, 100))
        
        self.distance_to_player = math.hypot(dx, dy)
        
        if -self.half_sprite_width < self.screen_x < WIDTH + self.half_sprite_width:
            self.get_sprite_projection()
    
    def update(self):
        self.get_sprite()


class AnimatedSprite(Sprite):
    def __init__(self, game, pos, path, height_shift=30, animation_time=120) -> None:
        super().__init__(game, pos, path, height_shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.prev_animation_time = pygame.time.get_ticks()
        self.animation_trigger = False
    
    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.sprite = images[0]
    
    def check_animation_time(self):
        self.animation_trigger = False
        if pygame.time.get_ticks() - self.prev_animation_time > self.animation_time:
            self.prev_animation_time = pygame.time.get_ticks()
            self.animation_trigger = True
    
    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pygame.image.load(path + '/' + file_name)
                images.append(img)
        return images
