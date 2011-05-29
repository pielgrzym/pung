# -*- coding: utf-8 -*-
import pygame, os
from sprite import Pad, Ball

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

    pad_left = Pad(relative_to=playarea_rect)
    pad_right = Pad(relative_to=playarea_rect, align=1)
    ball = Ball(pad_left=pad_left, relative_to=playarea_rect)
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
