import pygame, os
from event_manager import event_manager
import events

class View(object):
    def __init__(self, size=(800,600)):
        self.event_manager = event_manager
        self.surfaces = []
        self.paused = False
        self._setup_screen(size)
        self._setup_background()
        self._setup_sprites()
        self._setup_score()

    def _setup_score(self):
        """
        Sets up the score object
    
        """
        from score import Score
        self.score = Score(self.background)

    def _setup_screen(self, size):
        """
        Sets up the screen
    
        """
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Trollface pung. Enjoy. v0.40")
        pygame.mouse.set_visible(0)

    def _setup_sprites(self):
        """
        Initializes all sprites
    
        """
        from sprite import Pad, Ball
        self.pad_left = Pad(relative_to=self.playarea_rect)
        self.pad_right = Pad(relative_to=self.playarea_rect, align=1)
        self.ball = Ball(relative_to=self.playarea_rect)
        self.allsprites = pygame.sprite.RenderUpdates((
                    self.pad_left,
                    self.pad_right,
                    self.ball
                    ))
        self.pads = pygame.sprite.Group((self.pad_left, self.pad_right))

    def _blit_registered_surfaces(self):
        """
        Blit registered surfaces - called on each tick
    
        """
    
        for surface, rect in self.surfaces:
            self.background.blit(surface, rect)

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

    def handle_collisions(self):
        """
        Detect ball - sprite collisions and handle them

        """
        collisions = pygame.sprite.spritecollide(self.ball, self.pads, False)
        if len(collisions):
            # in the future there will be generic collision test
            # so the ball will bounce of extra walls etc
            self.ball.movement_vector[0] = -self.ball.movement_vector[0] 
            self.ball.image = pygame.transform.flip(self.ball.image, 1, 0)
            ball_mid = self.ball.rect.midright[1]
            pad = collisions[0]
            pad_mid = pad.rect.midright[1]
            angle_speed = (pad_mid - ball_mid)/10
            self.ball.movement_vector[1] -= angle_speed

    def notify(self, event):
        """
        Recieve events
    
        """
        if isinstance(event, events.TickEvent):
            if not self.paused:
                self.handle_collisions()
                self.allsprites.update()
                if self.surfaces:
                    self._blit_registered_surfaces()
                self.screen.blit(self.background, (0,0))
                self.allsprites.draw(self.screen)
                pygame.display.flip()
        elif isinstance(event, events.RegisterSurfaceEvent):
            self.register_surface(event.surface)
        elif isinstance(event, events.PauseEvent):
            self.paused = not self.paused
        elif isinstance(event, events.BlitRequestEvent):
            surface = getattr(self, event.surface_name)
            surface.blit(event.element, event.element_rect)
        elif isinstance(event, events.ModifyScoreEvent):
            self.score.modify_score(event)
