# -*- coding: utf-8 -*-
import pygame, os

class Score(object):
    def __init__(self, background=None):
        self.player = 0
        self.ai = 0
        self.avatars = pygame.image.load(os.path.join("data","score.png"))
        self.avatars.convert_alpha()
        self.avatars_rect = self.avatars.get_rect()
        screen = pygame.display.get_surface()
        self.avatars_rect.midtop = [screen.get_size()[0]/2, 0]
        background.blit(self.avatars, self.avatars_rect)

    def reset(self):
        """
        Reset both score
    
        """
        self.player = 0
        self.ai = 0

    def __check_win(self):
        """
        Checks if one of the players won
    
        """
    
        if self.player != self.ai:
            if self.player - self.ai > 1:
                print 'player won'
            elif self.ai - self.player > 1:
                print 'ai won'

    def point_for_player(self):
        """
        Increment score
    
        """
        self.player += 1
        self.__check_win()
    
    def point_for_ai(self):
        """
        Increment score
    
        """
        self.ai += 1
        self.__check_win()

class Pad(pygame.sprite.Sprite):
    def __init__(self, relative_to=None, align=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("data","pad.png"))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.align = align
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

class Ball(pygame.sprite.Sprite):
    def __init__(self, pad_left=None, relative_to=None, background=None):
        pygame.sprite.Sprite.__init__(self)
        self.pad_left = pad_left
        self.image = pygame.image.load(os.path.join("data", "trollface.png"))
        self.image = self.image.convert_alpha()
        colorkey = self.image.get_at((0,0))
        self.image.set_colorkey(colorkey, pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.relative_to = relative_to
        self.rect.topleft = screen.get_size()[0]/2, screen.get_size()[1]/2 # start pos
        self.move = [4,6] # movement vector
        self.score = Score(background)
        #self.move = [15,10]

    def update(self):
        self._fly() # leć, kurwa, leć!

    def _fly(self):
        """
        Latanie jakie jest, każdy widzi
    
        """
    
        newpos = self.rect.move(self.move[0], self.move[1])
        if not self.relative_to.contains(newpos):
            if self.rect.right > self.relative_to.right:
                self.move[0] = -self.move[0]
                if self.move[0] > 15:
                    self.move[0] -= 10
                if self.move[1] > 10:
                    self.move[1] -= 5
                self.image = pygame.transform.flip(self.image, 1, 0)
            if self.rect.top < self.relative_to.top or self.rect.bottom > self.relative_to.bottom:
                self.move[1] = -self.move[1]
                if self.move[0] > 15:
                    self.move[0] -= 10
                if self.move[1] > 10:
                    self.move[1] -= 5
            #if self.pad_left.rect.colliderect(self.rect):
            if self.rect.colliderect(self.pad_left.rect):
                self.move[0] = -self.move[0]
                if self.rect.colliderect(self.pad_left.hitzones[0]):
                    print 'top'
                    self.move[1] -= 5
                elif self.rect.colliderect(self.pad_left.hitzones[1]):
                    print 'bot'
                    self.move[1] += 5
                self.image = pygame.transform.flip(self.image, 1, 0)
            else:
                if self.rect.left < self.relative_to.left:
                    # begin fadeout
                    from pygame import surfarray
                    import numpy as N
                    rgbarray = surfarray.array3d(self.image)
                    src = N.array(rgbarray)
                    dest = N.zeros(rgbarray.shape)
                    dest[:] = 0, 0, 0
                    diff = (dest - src) * 0.50
                    if surfarray.get_arraytype() == 'numpy':
                        xfade = src + diff.astype(N.uint)
                    else:
                        xfade = src + diff.astype(N.Int)
                    surfarray.blit_array(self.image, xfade)
                    pygame.display.flip()
                    # end fadeout
                    self.move = [0,0] # stop
                    self.kill() # die :]
            newpos = self.rect.move((self.move[0], self.move[1]))
        self.rect = newpos

