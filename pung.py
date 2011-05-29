# -*- coding: utf-8 -*-
import pygame

class SpritePad(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/pad.png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()[1]
        self.rect.midleft = [0,pos]

class SpriteBall(pygame.sprite.Sprite):
    def __init__(self, pad=None):
        pygame.sprite.Sprite.__init__(self)
        self.pad = pad
        self.image = pygame.image.load("data/ball.png")
        self.image = self.image.convert()
        colorkey = self.image.get_at((0,0))
        self.image.set_colorkey(colorkey, pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        #self.move = [5,5]
        self.move = [15,10]

    def update(self):
        self._fly() # leć, kurwa, leć!

    def _fly(self):
        """
        Latanie jakie jest, każdy widzi
    
        """
    
        newpos = self.rect.move(self.move[0], self.move[1])
        if not self.area.contains(newpos):
            if self.rect.right > self.area.right:
                self.move[0] = -self.move[0]
            if self.rect.top < self.area.top or self.rect.bottom > self.area.bottom:
                self.move[1] = -self.move[1]
            #if self.pad.rect.colliderect(self.rect):
            if self.rect.colliderect(self.pad.rect):
                self.move[0] = -self.move[0]
            else:
                if self.rect.left < self.area.left:
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
                    screen = pygame.display.get_surface()
                    surfarray.blit_array(self.image, xfade)
                    pygame.display.flip()
                    # end fadeout
                    self.move = [0,0] # stop
                    self.kill() # die :]
            newpos = self.rect.move((self.move[0], self.move[1]))
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos

def game_over(background):
    """
    What do you think it does??

    """
    background = pygame.display.get_surface()
    if pygame.font:
        font = pygame.font.Font(None, 128)
        text = font.render("Gej over", 1, (255,255,255))
        textpos = text.get_rect(centerx=background.get_width()/2,
                centery=background.get_height()/2)
        background.blit(text, textpos)
        pygame.display.flip()


def main():
    """
    docstring

    """
    pygame.init()
    size = width, height = 800, 600

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pung - Pielgrzym's pong")
    pygame.mouse.set_visible(0)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("PUNG motherfucker v0.25", 1, (255,255,255))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

    screen.blit(background, (0,0))
    pygame.display.flip()
    pad = SpritePad()
    ball = SpriteBall(pad=pad)
    allsprites = pygame.sprite.RenderUpdates((pad,ball))
    clock = pygame.time.Clock()

    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
        if ball in allsprites:
            allsprites.update()
            screen.blit(background, (0, 0))
            allsprites.draw(screen)
            pygame.display.flip()
        else:
            game_over(background)
            pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
