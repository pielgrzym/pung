import pygame, os
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
        self._setup_background()

    def _setup_background(self):
        self.background = pygame.Surface((self.screen.get_size()))
        self.background = self.background.convert()
        self.background.fill((0,0,0))

        self.playarea = pygame.image.load(os.path.join("data", "playfield.png"))
        self.playarea.convert_alpha()
        self.playarea_rect = self.playarea.get_rect()
        self.playarea_rect.top = 50
        self.background.blit(self.playarea, self.playarea_rect)


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
                self.screen.blit(self.background, (0,0))
                self.allsprites.draw(self.screen)
                pygame.display.flip()
        elif isinstance(event, RegisterSurfaceEvent):
            self.register_surface(event.surface)
        elif isinstance(event, PauseEvent):
            self.paused = not self.paused
