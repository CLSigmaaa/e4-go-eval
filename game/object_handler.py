from sprite import Sprite
from settings import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.objects = []
        self.sprites = []
        self.add_sprite(Sprite(self.game, './ressources/sprites/static/candlebra.png', (WIDTH // 3, HALF_HEIGHT)))
        
    def add_sprite(self, sprite):
        self.sprites.append(sprite)
        
    def update(self):
        [sprite.update() for sprite in self.sprites]