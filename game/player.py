import pygame
import math
from settings import *

class Player:
    def __init__(self, game) -> None:
        self.map = None
        self.game = game
        self.x, self.y = 150, 150
        self.angle = 0
        self.player_speed = 150
        self.rel = None
        self.shot = False
        self.health = 100
        self.health_recovery_delay = 300
        
    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x // CELL_SIZE), int(self.y // CELL_SIZE)
    
    def get_rel(self):
        return self.rel
    
    def get_damage(self, damage):
        self.health -= damage
        self.game.sound.player_pain.play()
        # self.check_game_over()
    
    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < 100:
            self.health += 1

    def check_health_recovery_delay(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True
    
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
        self.angle += (self.rel * MOUSE_SENSITIVITY * dt) 
        self.angle = self.angle % (math.tau)
    
    def check_collision(self, x, y):
        map_x, map_y = int(x // CELL_SIZE), int(y // CELL_SIZE)
        if (0 <= map_x < len(self.game.map.map[0])) and (0 <= map_y < len(self.game.map.map[1])):
            if self.map[map_y][map_x] == 'W':
                return True
        # Vérifier la collision pour x + PLAYER_SIZE
        map_x = int((x + PLAYER_SIZE) // CELL_SIZE)
        if (0 <= map_x < len(self.game.map.map[0])) and (0 <= map_y < len(self.game.map.map[1])):
            if self.map[map_y][map_x] == 'W':
                return True
        # Vérifier la collision pour y + PLAYER_SIZE
        map_y = int((y + PLAYER_SIZE) // CELL_SIZE)
        if (0 <= map_x < len(self.game.map.map[0])) and (0 <= map_y < len(self.game.map.map[1])):
            if self.map[map_y][map_x] == 'W':
                return True

        # Vérifier la collision pour x - PLAYER_SIZE
        map_x = int((x - PLAYER_SIZE) // CELL_SIZE)
        if (0 <= map_x < len(self.game.map.map[0])) and (0 <= map_y < len(self.game.map.map[1])):
            if self.map[map_y][map_x] == 'W':
                return True
        
        # Vérifier la collision pour y - PLAYER_SIZE
        map_y = int((y - PLAYER_SIZE) // CELL_SIZE)
        if (0 <= map_x < len(self.game.map.map[0])) and (0 <= map_y < len(self.game.map.map[1])):
            if self.map[map_y][map_x] == 'W':
                return True
        return False
    
    def check_fire_weapon(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True
    
    # setter
    def set_map(self, map):
        self.map = map
    
    def update(self, dt):
        self.movement(dt)
        self.mouse_control(dt)
        self.recover_health()