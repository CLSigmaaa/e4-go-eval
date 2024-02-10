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
      self.reloading = False
      self.frame_counter = 0
      self.num_images = len(self.images)
    
    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)
    
    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.sprite = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0
      
    def update(self):
        self.check_animation_time()
        self.animate_shot()