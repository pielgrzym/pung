# -*- coding: utf-8 -*-
import pygame, os
from sprite import Pad, Ball
import controllers
from views import View
from event_manager import event_manager

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
    # initialize controllers
    input_controller = controllers.InputController()
    loop = controllers.LoopController()
    # initialize views
    main_view = View(size=size)


    pad_left = Pad(relative_to=main_view.playarea_rect)
    pad_right = Pad(relative_to=main_view.playarea_rect, align=1)
    ball = Ball(pad_left=pad_left, pad_right=pad_right, relative_to=main_view.playarea_rect, background=main_view.background)
    main_view.allsprites = pygame.sprite.RenderUpdates((pad_left,pad_right,ball))
    # register them
    print input_controller, loop, main_view
    event_manager.register_listener(input_controller)
    event_manager.register_listener(loop)
    event_manager.register_listener(main_view)
    # start master loop
    loop.run()


    #if pygame.font:
        #font = pygame.font.Font(None, 36)
        #text = font.render("Trollface pung. Enjoy. v0.40", 1, (255,255,255))
        #textpos = text.get_rect(centerx=background.get_width()/2)
        #background.blit(text, textpos)

    #screen.blit(background, (0,0))
    #pygame.display.flip()

    #background.blit(playarea, playarea_rect)

    #clock = pygame.time.Clock()

    #while 1:
        #clock.tick(60)
        #if not controller_tick():
            #return
        #view_tick()
        #if ball in allsprites:
            #allsprites.update()
            #screen.blit(ball.score.avatars, ball.score.avatars_rect)
            #screen.blit(background, (0, 0))
            #allsprites.draw(screen)
            #pygame.display.flip()
        #else:
            #game_over(background)
            #pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
