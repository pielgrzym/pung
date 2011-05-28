# -*- coding: utf-8 -*-
import sys, pygame
pygame.init()
size = width, height = 800, 600
bg_col = 0,0,0

screen = pygame.display.set_mode(size)

class Loop(object):
    def __init__(self, register=[]):
        """
        Inicjalizacja głównej pętli programu
        """
    
        self.object_queue = register
        self.start()

    def start(self):
        """
        To tutaj kręci się główna pętla :>
    
        """
    
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                for game_object in self.object_queue:
                    game_object(event)
            self.refresh()
    
    def refresh(self):
        """
        Odświeża ekran
    
        """
    
        screen.fill(black)
        for game_object in self.object_queue:
            screen.blit(game_object.image, game_object.rect)
            pygame.display.flip()

class Ball(object):
    def __init__(self, start=[0,0]):
        self.image = pygame.image.load("img/ball.gif")
        self.rect = self.image.get_rect()
