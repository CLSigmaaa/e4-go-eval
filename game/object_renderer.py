from settings import *
import pygame

class ObjectRenderer:
    def __init__(self, game) -> None:
        self.game = game
        self.screen = game.screen
        self.raycasting = game.raycasting
        self.wall_texture =  pygame.image.load('./ressources/textures/1.png')
        self.textures = {
            'W':  pygame.transform.scale(self.wall_texture, (TEXTURE_SIZE, TEXTURE_SIZE))
        }
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'./ressources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        
    def render_game_objects(self):
        # print(self.raycasting.objects_to_render)
        list_objects = sorted(self.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        # print(list_objects)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)
    
    def draw_crosshair(self):
        pygame.draw.line(self.screen, (0, 255, 0), (HALF_WIDTH - 15, HALF_HEIGHT), (HALF_WIDTH + 15, HALF_HEIGHT))
        pygame.draw.line(self.screen, (0, 255, 0), (HALF_WIDTH, HALF_HEIGHT - 15), (HALF_WIDTH, HALF_HEIGHT + 15))
    
    def draw_player_health(self):
        try:
            health = str(self.game.player.health)
            for i, char in enumerate(health):
                self.screen.blit(self.digits[char], (i * self.digit_size, 0))
            self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))
        except:
            font = pygame.font.SysFont('Arial', 20, bold=True)
            text_health = font.render('Player health : ' + str(self.game.player.health), True, pygame.Color('white'))
            self.screen.blit(text_health, (10, 30))
    
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pygame.image.load(path)
        return pygame.transform.scale(texture, res)