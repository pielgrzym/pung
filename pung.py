# -*- coding: utf-8 -*-
import pygame
import controllers
import views
from event_manager import event_manager

def main():
    """
    Behold! Here happens The Main Shit. 

    """
    pygame.init()
    size = 800, 600
    # initialize controllers
    player_controller = controllers.PlayerController()
    ai_controller = controllers.AIController()
    loop = controllers.LoopController()
    event_manager.register_listener(player_controller)
    event_manager.register_listener(ai_controller)
    event_manager.register_listener(loop)

    # initialize views
    game_view = views.GameView(size=size)
    event_manager.register_listener(game_view)

    # start master loop
    loop.run()

    pygame.quit()

if __name__ == '__main__':
    main()
