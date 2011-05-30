import pygame

class View(object):
    def __init__(self, size=(800,600)):
        self.allsprites = None
        self.surfaces = []
        self.screen = pygame.display.set_mode(size)
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
        from events import TickEvent, RegisterSurface
        if isinstance(event, TickEvent):
            self.allsprites.update()
            self.surfaces_update()
            self.allsprites.draw()
            pygame.display.flip()
        elif isinstance(event, RegisterSurface):
            self.register_surface(event.surface)
