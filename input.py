import pygame
import time
from debug import debug

class Input:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def initialize(self):
        if not self._initialized:
            self._initialized = True

            self.keys = 0
            self.last_frame = 0
            self.keys_buffer = []

            self.A = pygame.K_z
            self.B = pygame.K_x
            self.X = pygame.K_a
            self.Y = pygame.K_s
            self.L = pygame.K_d
            self.LB = pygame.K_c
            self.R = pygame.K_f
            self.RB = pygame.K_v
            self.select = pygame.K_SPACE
            self.start = pygame.K_RETURN
            self.up = pygame.K_UP
            self.down = pygame.K_DOWN
            self.left = pygame.K_LEFT
            self.right = pygame.K_RIGHT

            self.button_mapping = {
                'A': 0, 'B': 1, 'X': 2, 'Y': 3,
                'L': 4, 'LB': 5, 'R': 6, 'RB': 7,
                'select': 8, 'start': 9, 'up': 10, 'down': 11,
                'left': 12, 'right': 13
            }

        else:
            raise Exception("Input already initialized.")
        
    def update(self):
        self.last_frame = self.keys # Saves the last frame

        raw_keys = pygame.key.get_pressed()
        for button, index in self.button_mapping.items():
            key = getattr(self, button)
            if raw_keys[key]:
                self.keys |= (1 << index)  # Update key to 1
            else:
                self.keys &= ~(1 << index)  # Update key to 0

            if (self.keys >> index) & 1 and not ((self.last_frame >> index) & 1):
                self.keys_buffer.insert(0, (self.keys, time.time()))

    def readble_buffer(self):
        last_keys = []
        for keys, timestamp in self.keys_buffer[:5]:
            key_info = []
            for button, index in self.button_mapping.items():
                if (keys >> index) & 1:
                    key_info.append(button)
            # Formatar o timestamp para hh:mm:ss
            formatted_time = time.strftime("%H:%M:%S", time.localtime(timestamp))
            last_keys.append((key_info, formatted_time))
        return last_keys

    def key_hold(self, button):
        index = self.button_mapping.get(button)
        if index is not None:
            return (self.keys >> index) & 1
        return None

    def key_down(self, button):
        index = self.button_mapping.get(button)
        if index is not None:
            return (self.keys >> index) & 1 and not ((self.last_frame >> index) & 1)
        return None
    
    def key_up(self, button):
        index = self.button_mapping.get(button)
        if index is not None:
            return not (self.keys >> index) & 1 and ((self.last_frame >> index) & 1)
        return None