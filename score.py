# -*- coding: utf-8 -*-
import pygame, os
import events
from event_manager import event_manager

class Score(object):
    def __init__(self, background=None):
        self.event_manager = event_manager
        self.player = 0
        self.ai = 0
        self.avatars = pygame.image.load(os.path.join("data","score.png"))
        self.avatars.convert_alpha()
        self.avatars_rect = self.avatars.get_rect()
        screen = pygame.display.get_surface()
        self.avatars_rect.midtop = [screen.get_size()[0]/2, 0]
        background.blit(self.avatars, self.avatars_rect)
        self.background = background
        self.draw_player_score()
        self.draw_ai_score()

    def draw_player_score(self):
        """
        Draws text with player score

        """
        background = self.background
        font = pygame.font.Font(None, 42)
        text = font.render("%d" % self.player, 1, (255,255,255))
        textpos = text.get_rect(centerx=background.get_width()/2-80, top=12)
        background.blit(text, textpos)
        self.player_text = text
        self.player_textpos = textpos

    def erase_player_score(self):
        """
        Removes text with player score

        """
        background = self.background
        self.player_text.fill((0,0,0))
        background.blit(self.player_text, self.player_textpos)

    def draw_ai_score(self):
        """
        Draws text with ai score

        """
        background = self.background
        font = pygame.font.Font(None, 42)
        text = font.render("%d" % self.ai, 1, (255,255,255))
        textpos = text.get_rect(centerx=background.get_width()/2+80, top=12)
        background.blit(text, textpos)
        self.ai_text = text
        self.ai_textpos = textpos

    def erase_ai_score(self):
        """
        Removes text with ai score

        """
        background = self.background
        self.ai_text.fill((0,0,0))
        background.blit(self.ai_text, self.ai_textpos)

    def reset(self):
        """
        Reset all scores

        """
        self.player = 0
        self.ai = 0

    def __check_win(self):
        """
        Checks if one of the players won

        """

        if self.player != self.ai:
            if self.player - self.ai > 1:
                self.event_manager.post(events.GameOverEvent(win=True))
            elif self.ai - self.player > 1:
                self.event_manager.post(events.GameOverEvent(win=False))

    def modify_score(self, event):
        """
        Modify score based on event

        """

        if event.ai:
            self.point_for_ai()
        elif event.player:
            self.point_for_player()
        else:
            raise ValueError

    def point_for_player(self):
        """
        Increment score for player

        """
        self.erase_player_score()
        self.player += 1
        self.draw_player_score()
        self.__check_win()

    def point_for_ai(self):
        """
        Increment score for ai

        """
        self.erase_ai_score()
        self.ai += 1
        self.draw_ai_score()
        self.__check_win()

