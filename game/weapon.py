from sprite import *
from settings import *
from collections import deque

class Weapon(AnimatedSprite):
    def __init__(self, game, pos=(0,0), path='./ressources/sprites/weapon/shotgun/0.png', height_shift=30, animation_time=120) -> None:
      super().__init__(game=game, pos=pos, path=path, height_shift=height_shift, animation_time=animation_time)
      self.game = game
      self.images = deque(
            [pygame.transform.scale(img, (self.sprite.get_width() * 0.5, self.sprite.get_height() * 0.5))
             for img in self.images])
      self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
    
    def draw_weapon(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)
    