# -*- coding: utf-8 -*-
import pygame, os
import events
from event_manager import event_manager

class MVCSprite(pygame.sprite.Sprite):
    event_manager = event_manager

class Pad(MVCSprite):
    def __init__(self, relative_to=None, align=0, pos=300):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("data","pad.png"))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.relative_to = relative_to
        self._align(align) # align the paddle
        self.pos = pos # initial pos

    def _align(self, align):
        """
        Align the paddle to left or right

        """
        if align: # aligned to the right
            self.border = self.relative_to.right-self.rect.width
            self.rect.right = pygame.display.get_surface().get_size()[0]
            self.image = pygame.transform.flip(self.image, 1, 0)
        else: # aligned to the left
            self.border = self.relative_to.left
            self.rect.left = 0
        self.align = align

    def _playarea_collisions(self):
        """
        Correct paddle position so it won't stick out
        of the playarea

        """
        if self.pos < self.relative_to.top+(self.rect.height/2):
            self.rect.top = self.relative_to.top
        elif self.pos > self.relative_to.bottom-(self.rect.height/2):
            self.rect.bottom = self.relative_to.bottom

    def update(self):
        self.rect.midleft = [self.border, self.pos]
        self._playarea_collisions()
        self.event_manager.post(
                events.PadMoveEvent(self.rect.center, self.align)
                )

class Ball(MVCSprite):
    def __init__(self, relative_to=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("data", "trollface.png"))
        self.image = self.image.convert_alpha()
        colorkey = self.image.get_at((0,0))
        self.image.set_colorkey(colorkey, pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.reset()
        self.relative_to = relative_to
        self.movement_vector = [8,6] # base movement vector

    def update(self):
        coords = self.rect.center
        self.event_manager.post(events.BallMoveEvent(coords))
        self._fly()

    def reset(self):
        """
        Sets the ball in right place :]
    
        """
        screen = pygame.display.get_surface()
        self.rect.topleft = screen.get_size()[0]/2, screen.get_size()[1]/2 # start pos

    def _fly(self):
        """
        This function only checks collisions with playarea_rect
        and if they occur with left/right edge it calls score events
    
        """
        from events import ModifyScoreEvent
        newpos = self.rect.move(self.movement_vector[0], self.movement_vector[1])
        if not self.relative_to.contains(newpos):
            # right edge
            if self.rect.right > self.relative_to.right:
                self.movement_vector[0] = -self.movement_vector[0]
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.event_manager.post(ModifyScoreEvent(player=1))
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
                self.event_manager.post(ModifyScoreEvent(ai=1))
                pygame.time.delay(200)
                self.reset()
            newpos = self.rect.move((self.movement_vector[0], self.movement_vector[1]))
        self.rect = newpos

