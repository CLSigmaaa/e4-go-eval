from sprite import *
from npc import *
from settings import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.objects = []
        self.sprites = []
        self.npcs = []
        self.npc_positions = {}
        # self.add_sprite(Sprite(self.game, (WIDTH // 3, HALF_HEIGHT), height_shift=0.12))
        # self.add_sprite(AnimatedSprite(self.game, (WIDTH // 4, HALF_HEIGHT), './ressources/sprites/animated/red_light/0.png', height_shift=0.1))
        
        # self.add_npc(NPC(self.game, (WIDTH // 3, HALF_HEIGHT), './ressources/sprites/animated/red_light/0.png', height_shift=0.1))
        # self.add_npc(SoldierNPC(self.game, (WIDTH // 3, HALF_HEIGHT)))
        
    
    def spawn_npc(self):
        for pos, npc in self.game.map.ennemies_map.items():
            if npc == 'Z':
                self.add_npc(CyberDemonNPC(self.game, pos))
            elif npc == 'Y':
                self.add_npc(CacoNPC(self.game, pos))
            elif npc == 'X':
                self.add_npc(SoldierNPC(self.game, pos))
    
    def add_sprite(self, sprite):
        self.sprites.append(sprite)
    
    def add_npc(self, npc):
        self.npcs.append(npc)
    
    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npcs if npc.alive}
        [sprite.update() for sprite in self.sprites]
        [npc.update() for npc in self.npcs]