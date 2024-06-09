import pygame
from settings import *
from input import Input

# STATES
states = [("idle", 10),
("walk_forward", 11),
("walk_backward", 11),
("jump_neutral", 12),
("jump_diagonal", 13),
("dash_forward", 6),
("dash_backward", 6),
("crouch_in", 6),
("crouch_idle", 7),
("block_stand", 4),
("block_overhead", 6),
("block_jump_neutral", 4),
("block_jump_diagonal", 1),
("block_crouch", 5)]

class Character(pygame.sprite.Sprite):
    def __init__(self, label):
        super().__init__()
        self.label = label
        self.base_path = f"Assets/chars/{label}"

        # Sprites
        self.frame = 0
        self.sprites = {}

        self.states_list = states
        self.state = states[0][0]
        self.last_frame_state = states[0][0]

        self.is_mirrored = False
        self.on_last_frame = False
        self.walk_speed = 3

        # Carrega todas as imagens para cada estado
        for state, frame_count in self.states_list:
            self.sprites[state] = []
            for frame in range(1, frame_count + 1):
                image_path = f"{self.base_path}/{state} ({frame}).png"
                image = pygame.image.load(image_path).convert_alpha()
                self.sprites[state].append(image)

        # Configura a imagem inicial e o retângulo
        self.image = self.sprites[self.state][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGTH // 2)

    def update(self):
        # Faz o behaviour
        self.do_behaviour()

        # Atualiza a imagem do sprite
        self.image = self.sprites[self.state][self.frame]

        self.flip_frame()

    # Atualiza o frame da animação
    def flip_frame(self):
        frame_exato = int((pygame.time.get_ticks() / 1000) * FPS) % FPS

        if frame_exato % (FPS // CHARACTER_FPS) == 0:
            # self.frame = self.frame + 1 if (self.frame + 1) < len(self.sprites) else 0
            self.frame = self.frame + 1 
            self.on_last_frame = False

            if self.frame == len(self.sprites[self.state]) - 1:
                self.on_last_frame = True
            elif self.frame >= len(self.sprites[self.state]):
                self.frame = 0  # Reinicia a animação passa do último frame
    
    def do_behaviour(self):
        self.last_frame_state = self.state

        if Input().key_down("down"):
            self.state = "crouch_in"
            if self.last_frame_state != self.state:
                self.frame = 0
        
        elif Input().key_hold("down"):
            if self.state == "crouch_in" and self.on_last_frame:
                self.state = "crouch_idle"
                self.frame = 0

        elif Input().key_hold("left"):
            if self.is_mirrored:
                self.state = "walk_forward"
                if self.last_frame_state != self.state:
                    self.frame = 0
            if not self.is_mirrored:
                self.state = "walk_backward"
                if self.last_frame_state != self.state:
                    self.frame = 0

            self.rect.x -= self.walk_speed
            
        elif Input().key_hold("right"):
            if self.is_mirrored:
                self.state = "walk_backward"
                if self.last_frame_state != self.state:
                    self.frame = 0
            if not self.is_mirrored:
                self.state = "walk_forward"
                if self.last_frame_state != self.state:
                    self.frame = 0

            self.rect.x += self.walk_speed

        else:
            self.state = "idle"
 
