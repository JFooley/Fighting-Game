import pygame, sys
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
        
        pygame.display.set_caption("Fight Game")

        self.scenes: list = []
        self.state: int = self.MENU

    def run(self):
        Input().initialize()
        gameUI = UI(self)

        while True: # Main Loop
            for event in pygame.event.get(): # Event Handdler
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

            # First
            debug(Input().readble_buffer()[0] if len(Input().keys_buffer) > 0 else "", y=10)
            debug(Input().readble_buffer()[1] if len(Input().keys_buffer) > 1 else "", y=60)
            debug(Input().readble_buffer()[2] if len(Input().keys_buffer) > 2 else "", y=110)
            debug(Input().readble_buffer()[3] if len(Input().keys_buffer) > 3 else "", y=160)
            debug(Input().readble_buffer()[4] if len(Input().keys_buffer) > 4 else "", y=210)

            # Then
            gameUI.display()

            # Finnally
            pygame.display.update()
            self.clock.tick(FPS)

game = Game()
game.run()