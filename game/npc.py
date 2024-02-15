from settings import *
from sprite import *
import random

class NPC(AnimatedSprite):
    def __init__(self, game, pos, attack_dist, size, health, attack_damage, accuracy, speed, type='npc', path='./ressources/sprites/static/candlebra.png', height_shift=0.27, scale=0.6, animation_time=120) -> None:
        super().__init__(game, pos, path, height_shift, scale, animation_time)
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.type = type
        
        self.attack_dist = attack_dist
        self.speed = speed
        self.size = size
        self.health = health
        self.attack_damage = attack_damage
        self.accuracy = accuracy
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False
        
    
    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x // CELL_SIZE), int(self.y // CELL_SIZE)
    
    def mapping(self, a, b):
        return (a // CELL_SIZE) * CELL_SIZE, (b // CELL_SIZE) * CELL_SIZE
    
    def another_mapping(self, a, b):
        return (a // CELL_SIZE), (b // CELL_SIZE)
    
    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        ox, oy = self.game.player.pos
        # On récupère la cellule dans laquelle se trouve le joueur
        x_map, y_map = (ox // CELL_SIZE) * CELL_SIZE, (oy // CELL_SIZE) * CELL_SIZE
        
        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0
        
        curr_angle = self.theta
        
        sin_a = math.sin(curr_angle)
        cos_a = math.cos(curr_angle)

        y, dy = (y_map + CELL_SIZE, 1) if sin_a > 0 else (y_map, -1)
        for _ in range(0, HEIGHT, CELL_SIZE):
            depth_h = (y - oy) / sin_a
            x = ox + depth_h * cos_a
            # print('self.another_mapping(x, y) : ' + str(self.another_mapping(x, y + dy)))
            # print('self.map_pos : ' + str(self.map_pos))
            if self.another_mapping(x, y + dy) == self.map_pos:
                player_dist_h = depth_h
                break
            if self.mapping(x, y + dy) in self.game.map.world_map:
                wall_dist_h = depth_h
                break
            y += dy * CELL_SIZE
        
        x, dx = (x_map + CELL_SIZE, 1) if cos_a > 0 else (x_map, -1)
        for _ in range(0, WIDTH, CELL_SIZE):
            depth_v = (x - ox) / cos_a
            y = oy + depth_v * sin_a
            # print('self.another_mapping(x + dx, y) : ' + str(self.another_mapping(x + dx, y)))
            # print('self.map_pos : ' + str(self.map_pos))
            if self.another_mapping(x + dx, y) == self.map_pos:
                player_dist_v = depth_v
                break
            if self.mapping(x + dx, y) in self.game.map.world_map:
                wall_dist_v = depth_v
                break
            x += dx * CELL_SIZE

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False
    
    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_width < self.screen_x < HALF_WIDTH + self.sprite_width:
                self.game.sound.npc_pain.play()
                self.player.shot = False
                self.health -= self.game.weapon.damage
                self.pain = True
                self.check_health()
    
    def animate_death(self):
        if not self.alive:
            if self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.sprite = self.death_images[0]
                self.frame_counter += 1
    
    def check_health(self):
        if self.health <= 0:
            self.alive = False
            self.game.sound.npc_death.play()
        
    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False
    
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int((self.x + dx * self.size) // CELL_SIZE) * CELL_SIZE, int((self.y // CELL_SIZE) * CELL_SIZE)):
            self.x += dx
        if self.check_wall(int((self.x // CELL_SIZE) * CELL_SIZE), int((self.y + dy * self.size) // CELL_SIZE) * CELL_SIZE):
            self.y += dy
    
    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos
        next_x, next_y = next_x * CELL_SIZE, next_y * CELL_SIZE
        
        angle = math.atan2(next_y + HALF_CELL_SIZE - self.y, next_x + HALF_CELL_SIZE - self.x)
        dx = math.cos(angle) * self.speed
        dy = math.sin(angle) * self.speed
        self.check_wall_collision(dx, dy)
    
    def attack(self):
        if self.animation_trigger:
            self.game.sound.npc_shot.play()
            if random.random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)
    
    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            self.check_hit_in_npc()

            if self.pain:
                self.animate_pain()

            elif self.ray_cast_value:
                self.player_search_trigger = True

                if self.distance_to_player < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()

            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()

            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()
    
    def get_info(self):
        return {
            "position": {
                "x": self.x,
                "y": self.y
            },
            "type": self.type,
        }
    
    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()


class SoldierNPC(NPC):
    def __init__(self, game, pos, attack_dist=CELL_SIZE * 2.5, size=25, health=30, attack_damage=10, accuracy=0.10, speed=1.98, type='soldier', path='./ressources/sprites/npc/soldier/0.png', height_shift=0.27, scale=0.6, animation_time=120) -> None:
        super().__init__(game, pos, attack_dist, size, health, attack_damage, accuracy, speed, type, path, height_shift, scale, animation_time)

class CacoNPC(NPC):
    def __init__(self, game, pos, attack_dist=CELL_SIZE, size=25, health=40, attack_damage=5, accuracy=0.35, speed=2, type='caco', path='./ressources/sprites/npc/caco_demon/0.png', height_shift=0.30, scale=0.6, animation_time=120) -> None:
        super().__init__(game, pos, attack_dist, size, health, attack_damage, accuracy, speed, type, path, height_shift, scale, animation_time)

class CyberDemonNPC(NPC):
    def __init__(self, game, pos, attack_dist=CELL_SIZE * 5, size=25, health=100, attack_damage=15, accuracy=0.20, speed=1.05, type='cyber_demon', path='./ressources/sprites/npc/cyber_demon/0.png', height_shift=0.05, scale=1.15, animation_time=240) -> None:
        super().__init__(game, pos, attack_dist, size, health, attack_damage, accuracy, speed, type, path, height_shift, scale, animation_time)