import pygame
import events
from event_manager import event_manager

class Widget(pygame.sprite.Sprite):
    event_manager = event_manager

    def __init__(self, container=None):
        pygame.sprite.Sprite.__init__(self)
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
    def __init__(self, text, container=None, pos=None, color=None):
        Widget.__init__(self, container)
        self.color = color or (20, 20, 20)
        self.font = pygame.font.Font(None, 30)
        self.__text = text
        self.image = self.font.render(self.__text, 1, self.color)
        self.rect = self.image.get_rect()
        if not pos:
            self.rect = self.rect.move(container.topleft)
        else:
            rx, ry = container.topleft
            self.rect = self.rect.move((rx+pos[0],ry+pos[1]))

class ButtonWidget(Widget):
    def __init__(self, text, container=None, pos=None, color=None, active_color=None):
        Widget.__init__(self, container)
        self.color = color or (20, 20, 20)
        self.active_color = active_color or (120,0,0)
        self.font = pygame.font.Font(None, 30)
        self.focused = 0
        self.dirty = 1
        self.__text = text
        self.image = self.font.render(self.__text, 1, self.color)
        self.rect = self.image.get_rect()

        if not pos:
            self.rect = self.rect.move(container.topleft)
        else:
            rx, ry = container.topleft
            self.rect = self.rect.move((rx+pos[0],ry+pos[1]))

    def set_focus(self, val):
        if self.focused == val:
            return
        else:
            self.focused = val
            if val:
                color = self.active_color
            else:
                color = self.color
            self.image = self.font.render(self.__text, 1, color)
