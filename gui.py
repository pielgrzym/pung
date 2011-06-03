import pygame
import events
from event_manager import event_manager

class Widget(pygame.sprite.Sprite):
    event_manager = event_manager

    def __init__(self, container=None):
        self.container = container
        self.focused = 0
        self.dirty = 1

    def set_focus(self, val):
        self.focused = val
        self.dirty = 1

    def kill(self):
        """
        Remove widget
    
        """
    
        self.container = None
        del self.container
        pygame.sprite.Sprite.kill(self)

    def notify(self, event):
        if isinstance(event, events.FocusWidgetEvent) and event.widget is self:
            self.set_focus(1)
        elif isinstance(event, events.FocusWidgetEvent) and self.focused:
            self.set_focus(0)

class LabelWidget(Widget):
    def __init__(self, text, container=None):
        Widget.__init__(self, container)
        self.color = (200, 200, 200)
        self.font = pygame.font.Font(None, 30)
        self.__text = text
        self.image = self.font.render(self.__text, 1, self.color)
        self.rect = self.image.get_rect()
