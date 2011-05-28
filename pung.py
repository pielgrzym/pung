# -*- coding: utf-8 -*-
import sys, pygame
pygame.init()
size = width, height = 800, 600
bg_col = 0,0,0

screen = pygame.display.set_mode(size)

class Loop(object):
    def __init__(self, register=[], interactive=[]):
        """
        Inicjalizacja głównej pętli programu
        """
    
        self.object_queue = register
        self.interactive_queue = interactive
        self.start()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            for game_object in self.interactive_queue:
                game_object(event)

    def start(self):
        """
        To tutaj kręci się główna pętla :>
    
        """
    
        while 1:
            self.refresh()
            self.process_events()
    
    def refresh(self):
        """
        Odświeża ekran
    
        """
    
        screen.fill(bg_col)
        for game_object in self.object_queue:
            game_object()
            screen.blit(game_object.image, game_object.rect)
        pygame.display.flip()

class Movable(object):
    def move(self, coords):
        """
        Moves to desired coords
    
        """
        x,y = coords
        self.rect = self.rect.move(x,y)

    def smooth_move(self, coords):
        x,y = coords
        for i in range(60):
            self.move([x,y])
            screen.blit(self.image, self.rect)
            pygame.display.update(self.rect)
            pygame.time.delay(1)

class Pad(Movable):
    def __init__(self, start=[0,0]):
        self.image = pygame.image.load("img/pad.png")
        self.rect = self.image.get_rect()
        self.move(start)

    def __call__(self,event=None):
        if not event: return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.smooth_move([0,-2])
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.smooth_move([0,2])

class Ball(Movable):
    def __init__(self, start=[0,0], pad=None):
        self.image = pygame.image.load("img/ball.gif")
        self.rect = self.image.get_rect()
        self.move(start)
        self.pad = pad
        self.speed = [2,2]

    def __call__(self, event=None):
        if self.rect.right > width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed[1] = -self.speed[1]
        if self.rect.left <= self.pad.rect.right:
            if self.rect.y >= self.pad.rect.y-50 and self.rect.y <= self.pad.rect.y+159:
                self.speed[0] = -self.speed[0]
            elif self.rect.left <= 0:
                sys.exit(0)
        self.move(self.speed)


pad1 = Pad()
ball = Ball(start=[20,100],pad=pad1)
loop = Loop(register=[ball,pad1], interactive=[pad1,])
