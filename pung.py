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
    Behold! Here happends the Main Shit. 

    """
    pygame.init()
    size = 800, 600
    # initialize controllers
    input_controller = controllers.InputController()
    loop = controllers.LoopController()
    event_manager.register_listener(input_controller)
    event_manager.register_listener(loop)

    # initialize views
    main_view = View(size=size)
    event_manager.register_listener(main_view)

    # start master loop
    loop.run()

    pygame.quit()

if __name__ == '__main__':
    main()
