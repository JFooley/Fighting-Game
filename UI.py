import pygame
from pygame import Rect
from settings import * 
from debug import debug

class UI:
    def __init__(self, game):
        # General variables
        self.game = game
        self.clock = pygame.time.Clock()

        # general 
        self.display_surface = pygame.display.get_surface()
        self.font_medium = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.font_type = pygame.font.Font(UI_FONT, TYPE_FONT_SIZE)

        # hp bar setup 
        self.daoA_hpbar = pygame.Rect(HP_A_POS_X, HP_A_POS_Y, HP_BAR_WIDTH, BAR_HEIGHT)
        self.daoB_hpbar = pygame.Rect(HP_B_POS_X, HP_B_POS_Y, HP_BAR_WIDTH, BAR_HEIGHT)
        self.daoA_hptext = pygame.Rect(HPTEXT_A_POS_X, HPTEXT_A_POS_Y, HP_BAR_WIDTH, BAR_HEIGHT)
        self.daoB_hptext = pygame.Rect(HPTEXT_B_POS_X, HPTEXT_B_POS_Y, HP_BAR_WIDTH, BAR_HEIGHT)
        self.daoA_hpsize = 0
        self.daoB_hpsize = 0

    def show_bar(self, current, max_amount, shadow_value, bg_rect: Rect, color, shadow_color):
        # draw bg 
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stat to a pixel equivalent
        ratio_curret = max(0, min(current / max_amount, 1))
        ratio_shadow = max(0, min(shadow_value / max_amount, 1))
        current_rect = bg_rect.copy()
        shadow_rect = bg_rect.copy()
        current_rect.width = bg_rect.width * ratio_curret
        shadow_rect.width = bg_rect.width * ratio_shadow

        # drawing the bar
        pygame.draw.rect(self.display_surface, shadow_color, shadow_rect)
        pygame.draw.rect(self.display_surface, color, current_rect)

    def show_text(self, text, rect, color):
        # drawning the text
        text_surface = self.font_medium.render(text, True, color)
        self.display_surface.blit(text_surface, rect)

    def show_button(self, text, textcolor, rect: Rect, l_radius, r_radius, type1= '', type2= ''):
        # draw bg 
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, rect, 
                border_top_left_radius= l_radius, 
                border_bottom_left_radius= l_radius,
                border_top_right_radius= r_radius,
                border_bottom_right_radius= r_radius)
        
        # draw type bg (if needs)
        if type1 != '':
            line_width = BUTTON_HEIGTH // 10

            rect_L = pygame.Rect(rect.x, rect.y, BUTTON_WIDTH // 2 , BUTTON_HEIGTH)
            rect_R = pygame.Rect(rect.centerx, rect.y, BUTTON_WIDTH // 2, BUTTON_HEIGTH)
            rect_culling = pygame.Rect(rect.centerx - BUTTON_HEIGTH // 2, rect.centery - (BUTTON_HEIGTH - 2 * line_width) // 2, BUTTON_HEIGTH, BUTTON_HEIGTH - 2 * line_width)

            pygame.draw.rect(self.display_surface,
                self.colorChart[type1], 
                rect_L,
                border_top_left_radius= l_radius, 
                border_bottom_left_radius= l_radius,
                width= line_width)
        
            pygame.draw.rect(self.display_surface, 
                self.colorChart[type2] if type2 != '' else self.colorChart[type1], 
                rect_R,
                border_top_right_radius= r_radius,
                border_bottom_right_radius= r_radius,
                width= line_width)
            
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, rect_culling)
        
        # Text offset
        text_surface = self.font_medium.render(text, True, textcolor)

        padding_X = text_surface.get_rect().width // 2
        padding_Y = text_surface.get_rect().height // 2
        
        text_rect = pygame.Rect((rect.centerx - padding_X), (rect.centery - padding_Y), BUTTON_WIDTH, BUTTON_HEIGTH)

        # draw text
        self.display_surface.blit(text_surface, text_rect)

    def show_button_UI(self, text, button_ID, color, active_color, pos_X, pos_Y, l_radius, r_radius):
        rect = pygame.Rect(pos_X, pos_Y, BUTTON_HEIGTH, BUTTON_HEIGTH)
        
        # Draw bg
        selected_color = active_color if Input().key_hold(button_ID) else color

        pygame.draw.rect(self.display_surface, selected_color, rect,
            border_top_left_radius= l_radius, 
            border_bottom_left_radius= l_radius, 
            border_top_right_radius= r_radius, 
            border_bottom_right_radius= r_radius)
        
        # Text offset
        text_surface = self.font_medium.render(text, True, UI_BG_COLOR)

        padding_X = text_surface.get_rect().width // 2
        padding_Y = text_surface.get_rect().height // 2
        
        text_rect = pygame.Rect((rect.centerx - padding_X), (rect.centery - padding_Y), BUTTON_HEIGTH, BUTTON_HEIGTH)

        # draw text
        self.display_surface.blit(text_surface, text_rect)

    def show_chatbox(self, textcolor):
        # draw bg and button
        rect = pygame.Rect(CHATBOX_POS_X, CHATBOX_POS_Y, CHATBOX_WIDTH, CHATBOX_HEIGTH)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, rect, border_radius= int(HALF_UNIT))
        self.show_button_UI("A", Input().A, ABXY_COLOR, ON_SELECT_COLOR, CHATBOX_BUTTON_X, CHATBOX_BUTTON_Y, BUTTON_ABXY_RADIUS, BUTTON_ABXY_RADIUS)

        # text offset
        text_surface = self.font_medium.render(self.on_screen_text, True, textcolor)

        padding_X = HALF_UNIT
        padding_Y = HALF_UNIT
        
        text_rect = pygame.Rect((rect.left + padding_X), (rect.top + padding_Y), CHATBOX_WIDTH, CHATBOX_WIDTH)

        # draw text
        self.display_surface.blit(text_surface, text_rect)

    def display(self):
        self.show_bar(85, 100, 95, self.daoA_hpbar, HP_COLOR, HP_SHADOW_COLOR)
        self.show_bar(60, 100, 90, self.daoB_hpbar, HP_COLOR, HP_SHADOW_COLOR)