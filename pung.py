# -*- coding: utf-8 -*-
import pygame, os

class SpritePad(pygame.sprite.Sprite):
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

class SpriteBall(pygame.sprite.Sprite):
    def __init__(self, pad_left=None, relative_to=None):
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

def game_over(background):
    """
    What do you think it does??

    """
    background = pygame.display.get_surface()
    if pygame.font:
        font = pygame.font.Font(None, 128)
        text = font.render("FAIL!", 1, (255,15,15))
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
    pygame.display.set_caption("Trollface pung. Enjoy. v0.40")
    pygame.mouse.set_visible(0)
    background = pygame.Surface((screen.get_size()))
    background = background.convert()
    background.fill((0,0,0))

    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Trollface pung. Enjoy. v0.40", 1, (255,255,255))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

    screen.blit(background, (0,0))
    pygame.display.flip()

    playarea = pygame.image.load(os.path.join("data", "playfield.png"))
    playarea.convert_alpha()
    playarea_rect = playarea.get_rect()
    playarea_rect.top = 50
    background.blit(playarea, playarea_rect)

    pad_left = SpritePad(relative_to=playarea_rect)
    pad_right = SpritePad(relative_to=playarea_rect, align=1)
    ball = SpriteBall(pad_left=pad_left, relative_to=playarea_rect)
    allsprites = pygame.sprite.RenderUpdates((pad_left,pad_right,ball))
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
