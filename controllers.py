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
                elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
                    self.event_manager.post(events.FocusWidgetEvent('up'))
                elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    self.event_manager.post(events.FocusWidgetEvent('down'))
                elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                    self.event_manager.post(events.FocusWidgetEvent('select'))
            # move the left pad with mouse
            self.event_manager.post(
                    events.ControlPadEvent(pygame.mouse.get_pos(), True)
                    )

class AIController(Controller):
    """
    Handle kickass Artificial Inteligence which by some queer accident
    escaped from Area 51!
    """

    def notify(self, event):
        """
        Some serious AI shit here

        """

        if isinstance(event, events.PadMoveEvent):
            if event.right:
                self.last_pos = event.coords[1]
        elif isinstance(event, events.BallMoveEvent):
            if event.x > 400:
                delta = event.y - self.last_pos or 1
                pos = [0, self.last_pos + delta/14]
                self.event_manager.post(
                        events.ControlPadEvent(pos, False)
                        )
