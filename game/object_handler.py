from sprite import *
from npc import *
from settings import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.objects = []
        self.sprites = []
        self.npcs = []
        # self.add_sprite(Sprite(self.game, (WIDTH // 3, HALF_HEIGHT), height_shift=0.12))
        # self.add_sprite(AnimatedSprite(self.game, (WIDTH // 4, HALF_HEIGHT), './ressources/sprites/animated/red_light/0.png', height_shift=0.1))
        
        self.add_npc(NPC(self.game, (WIDTH // 3, HALF_HEIGHT), './ressources/sprites/animated/red_light/0.png', height_shift=0.1))
        
    def add_sprite(self, sprite):
        self.sprites.append(sprite)
    
    def add_npc(self, npc):
        self.npcs.append(npc)
    
    def update(self):
        [sprite.update() for sprite in self.sprites]
        [npc.update() for npc in self.npcs]