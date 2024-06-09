import pygame
from input import Input
from characters import *
from settings import *

class GenericAsset(pygame.sprite.Sprite):
    def __init__(self, label, base_path, states_list, fps= FPS, size= None):
        super().__init__()
        self.label = label
        self.base_path = base_path

        # Inicializa as animações dos estados
        self.states_list = states_list
        self.state = states_list[0][0]
        self.frame = 0
        self.fps = fps
        self.sprites = {}

        # Carrega todas as imagens para cada estado
        for state, frame_count in self.states_list:
            self.sprites[state] = []
            for frame in range(1, frame_count + 1):
                image_path = f"{self.base_path}/{state} ({frame}).png"
                image = pygame.image.load(image_path).convert_alpha()
                self.sprites[state].append(image)

        # Configura a imagem inicial e o retângulo
        self.size = size
        self.image = self.sprites[self.state][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGTH // 2)

    def update(self):
        # Faz o behaviour
        self.do_behaviour()

        # Atualiza o frame da animação
        frame_exato = int((pygame.time.get_ticks() / 1000) * FPS) % FPS
        animation_tick = frame_exato % (FPS // self.fps) == 0

        if animation_tick:
            self.frame = self.frame + 1 if (self.frame + 1) < len(self.sprites) else 0
        if self.frame >= len(self.sprites[self.state]):
            self.frame = 0  # Reinicia a animação quando atinge o último frame

        # Atualiza a imagem do sprite
        self.image = self.sprites[self.state][self.frame]
    
    def do_behaviour(self):
        pass