from settings import * 
from map import *
from player import *
from raycasting import *
from debug import *
from sprite import *
from object_renderer import *
from object_handler import *
from weapon import *
from pathfinding import *
from websocket_client import *
from sound import *
import pygame
import time
import uuid
from websocket import WebSocketConnectionClosedException

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.prev_time = time.time()
        self.game_id = str(uuid.uuid4())
        self.new_game()
        
    def new_game(self):
        self.sound = Sound(self)
        self.player = Player(self)
        self.map = Map(self, self.player)
        self.map.generate_basic_map()
        self.map.generate_world_map()
        self.player.set_map(self.map.map)
        self.raycasting = Raycasting(self)
        self.weapon = Weapon(self)
        self.pathfinding = PathFinding(self)
        self.object_handler = ObjectHandler(self)
        self.object_handler.spawn_npc()
        self.object_renderer = ObjectRenderer(self)
        self.debug = Debug(self)
        self.ws_client = WebSocketClient(self, "ws://localhost:8080/ws")
        pygame.mixer.music.play(-1)
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            self.player.check_fire_weapon(event)
    
    def update(self, dt):
        self.player.update(dt)
        self.raycasting.draw()
        self.object_handler.update()
        self.object_renderer.render_game_objects()
        self.object_renderer.draw_crosshair()
        self.weapon.draw()
        self.weapon.update()
        self.map.draw()
        self.debug.draw()
        try:
            self.ws_client.send(
                {
                    "game_id": self.game_id,
                    "player": {
                        "position": {
                            "x": self.player.x,
                            "y": self.player.y
                        },
                        "health": self.player.health,
                    },
                    "npcs": [npc.get_info() for npc in self.object_handler.npcs],
                }
            )
        except WebSocketConnectionClosedException as e:
            pass
        finally:
            pygame.display.flip()
    
    def run(self):
        while True:
            self.check_events()
            self.delta_time = time.time() - self.prev_time
            self.prev_time = time.time()
            self.update(self.delta_time)
            self.clock.tick(MAX_FPS)
            
if __name__ == '__main__':
    game = Game()
    game.run()