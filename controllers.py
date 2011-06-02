import pygame
from event_manager import event_manager
import events

class Controller(object):
    event_manager = event_manager

    def notify(self, event):
        raise NotImplementedError

class LoopController(Controller):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.is_running = True

    def run(self):
        """
        Main cpu loop
    
        """
        event = events.TickEvent()
        while self.is_running:
            self.clock.tick(60)
            self.event_manager.post(event)

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            self.is_running = False

class PlayerController(Controller):
    """
    Handle controller events

    """
    def notify(self, e):
        if isinstance(e, events.TickEvent):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.event_manager.post(events.QuitEvent())
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.event_manager.post(events.QuitEvent())
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.event_manager.post(events.PauseEvent())
            self.event_manager.post(events.MovePadEvent(pygame.mouse.get_pos()))

class AIController(Controller):
    """
    Handle kickass Artificial Inteligence which by some queer accident
    escaped from Area 51!
    """
    pass
