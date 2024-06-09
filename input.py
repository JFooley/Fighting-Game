import pygame
from debug import debug

##### OBSERVAÇÕES PARA O USO CORRETO DA CLASSE #####
# Essa é uma classe singleton, ou seja, só possui uma instancia do objeto.
# Ela é feita dessa forma para poder ser acessada de forma igual em qualquer parte do código
# independente da cena que esteja sendo rodada. Ela só existe pois o pygame naturalmente não
# possui um método de verificação de Key Up e Key Down, então foi necessário implementa-los.
# Para usar corretamente, no ínicio do código é necessário chamar o método initialize() e a 
# cada frame do jogo, chamar o método update.
# Dai em diante basta importar e chamar Input() (com o parêntese, já que queremos o objeto) 
# e usar seus métodos ou acessar seus atributos.
# A respeito do funcionamento, a classe guarda a frame atual e o anterior do estado dos botões
# e guarda um buffer legível das entradas e o seu tempo de frame entre elas.

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
            self.frame_limiar = 15
            self.frame_counter = self.frame_limiar

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

        raw_keys = pygame.key.get_pressed() # Saves the current frame
        for button, index in self.button_mapping.items():
            key = getattr(self, button)
            if raw_keys[key]:
                self.keys |= (1 << index)  # Update key to 1
            else:
                self.keys &= ~(1 << index)  # Update key to 0

        self.do_buff_inputs()

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
    
    def do_buff_inputs(self):
        if (self.keys & ~self.last_frame) != 0: # Check any button key down
            key_info = []
            for button, index in self.button_mapping.items(): # Translate the frame to a button readble
                if ((self.keys & ~self.last_frame) >> index) & 1:
                    key_info.append(button)

            self.keys_buffer.insert(0, (self.frame_counter, key_info)) # Save the input and reset frame counter
            self.frame_counter = 1
        else:
            self.frame_counter = self.frame_counter + 1 if self.frame_counter <= self.frame_limiar and self.frame_counter > 0 else 0 # Increase frame counter for each non key down frame
            if self.frame_counter == self.frame_limiar:
                self.keys_buffer.insert(0, (self.frame_limiar, ["N"]))
    
    def check_string(self, move: list):
        frame_index = 0
        for frame in move:
            for button in frame:
                if self.keys_buffer[frame_index][1]:
                    pass