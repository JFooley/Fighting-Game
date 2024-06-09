import pygame
from pygame import Vector3
from generic_asset import GenericAsset
from input import Input
from characters import *
from settings import *

# STATES
stage_states_list = [("stage", 5)]                

class BattleScene():
    OFF_BATTLE = 0
    INTRO = 1
    ROUND_START = 2
    BATTLING = 3
    ROUND_END = 4
    ENDING = 5

    def __init__(self, game, char_A= '', char_B= '', stage= 0):
        self.game = game
        self.state = self.OFF_BATTLE
        self.frame_counter = 0

        self.char_A = char_A
        self.char_B = char_B
        self.stage = stage

        self.scene_objects = pygame.sprite.Group()
        self.background_objects = pygame.sprite.Group()

        self.camera = Vector3(WIDTH // 2, HEIGTH // 2, WIDTH)

    
    def run(self):
        if self.game.state == ON_BATTLE:
            self.do_behaviour()
            self.do_display()

        if self.game.state == MENU:
            ## DEBUG
            if Input().key_down("start"):
                self.game.state = ON_BATTLE
            ## DEBUG


    def do_display(self):
        if self.state == self.INTRO:
            ## Load
            playerA = Character("Ken")
            self.scene_objects.add(playerA)

            stage = GenericAsset("stage", "Assets/stages", stage_states_list)
            self.background_objects.add(stage)

            self.state = self.ROUND_START


        elif self.state == self.ROUND_START:
            self.background_objects.draw(surface=self.game.screen)
            self.scene_objects.draw(surface=self.game.screen)

            self.play_util(2, self.BATTLING)


        elif self.state == self.BATTLING:
            self.background_objects.draw(surface=self.game.screen)
            self.scene_objects.draw(surface=self.game.screen)


        elif self.state == self.ROUND_END:
            self.background_objects.draw(surface=self.game.screen)
            self.scene_objects.draw(surface=self.game.screen)

            self.play_util(2, self.ENDING)

        
        elif self.state == self.ENDING:
            if self.play_util(3, self.OFF_BATTLE):
                self.scene_objects.empty()
                self.game.state = MENU


    def do_behaviour(self):
        if self.state == self.OFF_BATTLE:
            self.state = self.INTRO

        if self.state == self.BATTLING:
            self.scene_objects.update()

            ## DEBUG
            if Input().key_down("start"):
                self.state = self.ROUND_END
            ## DEBUG
            
    def play_util(self, seconds, next_state):
        self.frame_counter += 1
        if self.frame_counter >= seconds * 60:
            self.frame_counter = 0
            self.state = next_state
            return True        
        
        return False

        