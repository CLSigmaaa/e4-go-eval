from settings import *
import pygame

class ObjectRenderer:
    def __init__(self, game) -> None:
        self.screen = game.screen
        self.raycasting = game.raycasting
        self.wall_texture =  pygame.image.load('./ressources/textures/1.png')
        self.textures = {
            'W':  pygame.transform.scale(self.wall_texture, (TEXTURE_SIZE, TEXTURE_SIZE))
        }
        
    def render_game_objects(self):
        # print(self.raycasting.objects_to_render)
        list_objects = sorted(self.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        # print(list_objects)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)