import pygame, sys
from scenes.battle_scene import BattleScene
from input import Input
from UI import UI
from settings import *
from debug import debug

class Game:
    # States
    MENU = 0
    ON_BATTLE = 1

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.UI = UI(self)
        
        pygame.display.set_caption("Fight Game")

        self.scenes: list = []
        self.state: int = self.MENU

    def run(self):
        Input().initialize()
        battle_scene = BattleScene(self)

        while True: # Main Loop
            for event in pygame.event.get(): # Event Handdler
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

            # First
            Input().update()

            # Draws
            battle_scene.run()
            self.UI.display()

            debug(f"Battle state: {battle_scene.state}")

            debug(str(Input().keys_buffer[0] if len(Input().keys_buffer) > 0 else "").ljust(50), y=110)
            debug(str(Input().keys_buffer[1] if len(Input().keys_buffer) > 1 else "").ljust(50), y=160)
            debug(str(Input().keys_buffer[2] if len(Input().keys_buffer) > 2 else "").ljust(50), y=210)
            debug(str(Input().keys_buffer[3] if len(Input().keys_buffer) > 3 else "").ljust(50), y=260)
            debug(str(Input().keys_buffer[4] if len(Input().keys_buffer) > 4 else "").ljust(50), y=310)
            debug(str(Input().keys_buffer[5] if len(Input().keys_buffer) > 5 else "").ljust(50), y=360)
            debug(str(Input().keys_buffer[6] if len(Input().keys_buffer) > 6 else "").ljust(50), y=410)
            debug(str(Input().keys_buffer[7] if len(Input().keys_buffer) > 7 else "").ljust(50), y=460)
            debug(str(Input().keys_buffer[8] if len(Input().keys_buffer) > 8 else "").ljust(50), y=510)
            debug(str(Input().keys_buffer[9] if len(Input().keys_buffer) > 9 else "").ljust(50), y=560)

            # Finnally
            pygame.display.update()
            self.clock.tick(FPS)

game = Game()
game.run()