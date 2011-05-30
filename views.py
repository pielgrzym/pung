import pygame
from event_manager import event_manager

class View(object):
    def __init__(self, size=(800,600)):
        self.allsprites = None
        self.surfaces = []
        self.event_manager = event_manager
        self.screen = pygame.display.set_mode(size)
        self.paused = False
        pygame.display.set_caption("Trollface pung. Enjoy. v0.40")
        pygame.mouse.set_visible(0)

    def surfaces_update(self):
        """
        Blits every surface
    
        """
        for surface, rect in self.surfaces:
            self.screen.blit(surface, rect)

    def register_surface(self, surface):
        self.surfaces.append(surface)

    def notify(self, event):
        """
        Recieve events
    
        """
        from events import TickEvent, RegisterSurfaceEvent, PauseEvent
        if isinstance(event, TickEvent):
            if not self.paused:
                self.allsprites.update()
                self.surfaces_update()
                self.allsprites.draw(self.screen)
                pygame.display.flip()
        elif isinstance(event, RegisterSurfaceEvent):
            self.register_surface(event.surface)
        elif isinstance(event, PauseEvent):
            self.paused = not self.paused
