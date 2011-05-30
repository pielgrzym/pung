# -*- coding: utf-8 -*-
import pygame, os
from event_manager import event_manager

class MVCSprite(pygame.sprite.Sprite):
    event_manager = event_manager


class Pad(MVCSprite):
    def __init__(self, relative_to=None, align=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("data","pad.png"))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.align = align
        if align:
            self.rect.right = pygame.display.get_surface().get_size()[0]
            self.image = pygame.transform.flip(self.image, 1, 0)
        else:
            self.rect.left = 0
        self.relative_to = relative_to
        self.hitzones = [ 
                pygame.Rect(self.rect.left, self.rect.top, 20, 20),
                pygame.Rect(self.rect.left, self.rect.top+140, 20, 20),
                ]

    def update(self):
        if self.align:
            border = self.relative_to.right-self.rect.width
        else:
            border = self.relative_to.left
        pos = pygame.mouse.get_pos()[1]
        if pos < self.relative_to.top+(self.rect.height/2):
            self.rect.top = self.relative_to.top
        elif pos > self.relative_to.bottom-(self.rect.height/2):
            self.rect.bottom = self.relative_to.bottom
        else:
            self.rect.midleft = [border, pos]
        self.hitzones[0].top = self.rect.top
        self.hitzones[1].bottom = self.rect.bottom

class Ball(MVCSprite):
    def __init__(self, pad_left=None, pad_right=None, relative_to=None, background=None):
        from score import Score
        pygame.sprite.Sprite.__init__(self)
        self.pad_left = pad_left
        self.pad_right = pad_right
        self.image = pygame.image.load(os.path.join("data", "trollface.png"))
        self.image = self.image.convert_alpha()
        colorkey = self.image.get_at((0,0))
        self.image.set_colorkey(colorkey, pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.reset()
        self.relative_to = relative_to
        self.movement_vector = [8,6] # movement vector
        self.score = Score(background)
        #self.move = [15,10]

    def update(self):
        self._fly() # leć, kurwa, leć!

    def reset(self):
        """
        Sets the ball in right place :]
    
        """
        screen = pygame.display.get_surface()
        self.rect.topleft = screen.get_size()[0]/2, screen.get_size()[1]/2 # start pos

    def _fly(self):
        """
        Latanie jakie jest, każdy widzi
    
        """
    
        newpos = self.rect.move(self.movement_vector[0], self.movement_vector[1])
        if not self.relative_to.contains(newpos):
            # right edge
            if self.rect.right > self.relative_to.right:
                self.movement_vector[0] = -self.movement_vector[0]
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.score.point_for_player()
                pygame.time.delay(200)
                self.reset()
            # top/bottom edge
            if self.rect.top < self.relative_to.top or self.rect.bottom > self.relative_to.bottom:
                self.movement_vector[1] = -self.movement_vector[1]
                if self.movement_vector[0] > 15:
                    self.movement_vector[0] -= 10
                if self.movement_vector[1] > 10:
                    self.movement_vector[1] -= 5
            # left edge
            if self.rect.left < self.relative_to.left:
                self.movement_vector[0] = -self.movement_vector[0]
                #self.kill() # die :]
                self.score.point_for_ai()
                pygame.time.delay(200)
                self.reset()
            newpos = self.rect.move((self.movement_vector[0], self.movement_vector[1]))
        self.rect = newpos

