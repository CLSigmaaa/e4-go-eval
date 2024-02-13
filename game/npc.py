from settings import *
from sprite import *
import random

class NPC(AnimatedSprite):
    def __init__(self, game, pos, path, height_shift=30, animation_time=120) -> None:
        super().__init__(game, pos, path, height_shift, animation_time)
        
        # self.attack_images = self.get_images(self.path + '/attack')
        # self.death_images = self.get_images(self.path + '/death')
        # self.idle_images = self.get_images(self.path + '/idle')
        # self.pain_images = self.get_images(self.path + '/pain')
        # self.walk_images = self.get_images(self.path + '/walk')

        self.attack_dist = random.randint(3, 6)
        self.speed = 0.03
        self.size = 20
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False
        self.is_npc_visible = False
    
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

        y, dy = (y_map + CELL_SIZE, 1) if sin_a >= 0 else (y_map, -1)
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
        
        x, dx = (x_map + CELL_SIZE, 1) if cos_a >= 0 else (x_map, -1)
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
            self.is_npc_visible = True
            return True
        self.is_npc_visible = False
        return False
    
    def run_logic(self):
        self.ray_cast_player_npc()  # Call the method instead of assigning a boolean value
        font = pygame.font.SysFont('Arial', 20, bold=True)
        text_is_visible = font.render('Is visible by the player : ' + str(self.is_npc_visible), True, pygame.Color('white'))  # Call the method to get the updated value
        self.game.screen.blit(text_is_visible, (10, 120))
    
    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()