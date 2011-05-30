import pygame
from event_manager import event_manager
from events import TickEvent, QuitEvent, PauseEvent

class Controller(object):
    event_manager = event_manager

    def notify(self, event):
        raise NotImplementedError

class CPUSpinnerController(Controller):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.is_running = True

    def run(self):
        """
        Main cpu loop
    
        """
        while self.is_running:
            self.clock.tick(60)
            event = TickEvent()
            self.event_manager.post(event)

    def notify(self, event):
        if isinstance(event, QuitEvent):
            self.is_running = False

class InputController(Controller):
    """
    Handle controller events

    """
    def notify(self, e):
        if isinstance(e, TickEvent):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.event_manager.post(QuitEvent())
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.event_manager.post(QuitEvent())
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.event_manager.post(PauseEvent())
