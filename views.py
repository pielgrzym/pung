import pygame, os
from event_manager import event_manager
import events
import gui

class View(object):
    event_manager = event_manager

    def __init__(self, size=(800,600)):
        """
        Setup the screen
    
        """
    
        self._setup_screen(size)

    def register_surface(self, surface):
        if hasattr(self, 'surfaces'): 
            self.surfaces.append(surface)
        else:
            self.surfaces = [surface]

    def _blit_registered_surfaces(self):
        """
        Blit registered surfaces - called on each tick
    
        """
        if hasattr(self, 'surfaces'): 
            for surface, rect in self.surfaces:
                self.background.blit(surface, rect)

    def _setup_screen(self, size):
        """
        Sets up the screen
    
        """
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Trollface pung. Enjoy. v0.40")
        pygame.mouse.set_visible(0)

class MenuView(View):
    def __init__(self, size=(800,600)):
        self._setup_screen(size)
        self._setup_background()
        self.surfaces = []
        self.title_widget = gui.LabelWidget("PUNG - main menu", container=self.menu_rect,
                pos=[10,10])
        self.menu_start = gui.ButtonWidget("Start game", container=self.menu_rect,
                pos=[30,50])
        self.menu_start.set_focus(1)
        self.menu_options = gui.ButtonWidget("Options", container=self.menu_rect,
                pos=[30,75])
        self.menu_exit = gui.ButtonWidget("Exit game", container=self.menu_rect,
                pos=[30,100])

        self.allsprites = pygame.sprite.Group((
            self.title_widget,
            self.menu_start,
            self.menu_options,
            self.menu_exit
            ))
        self.menu = pygame.sprite.Group((
            self.menu_start,
            self.menu_options,
            self.menu_exit
            ))

    def _setup_background(self):
        self.background = pygame.Surface((self.screen.get_size()))
        self.background = self.background.convert()
        self.background.fill((0,0,0))

        self.menu_rect = pygame.Rect(100,100, 600, 400)
        self.menu = pygame.Surface((600,400))
        self.menu = self.menu.convert()
        self.menu.fill((180,180,180))
        self.background.blit(self.menu, self.menu_rect)


    def notify(self, event):
        """
        Recieve events
    
        """
        if isinstance(event, events.TickEvent):
            if self.surfaces:
                self._blit_registered_surfaces()
            self.screen.blit(self.background, (0,0))
            self.allsprites.draw(self.screen)
            pygame.display.flip()
    

class GameView(View):
    def __init__(self, size=(800,600)):
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

    def _setup_background(self):
        self.background = pygame.Surface((self.screen.get_size()))
        self.background = self.background.convert()
        self.background.fill((0,0,0))

        self.playarea = pygame.image.load(os.path.join("data", "playfield.png"))
        self.playarea.convert_alpha()
        self.playarea_rect = self.playarea.get_rect()
        self.playarea_rect.top = 50
        self.background.blit(self.playarea, self.playarea_rect)

    def game_over(self, win=True):
        """
        What do you think it does??

        """
        self.ball.kill()
        if win:
            image = pygame.image.load(os.path.join("data", "fuckyea.jpg"))
        else:
            image = pygame.image.load(os.path.join("data", "fuuu.jpg"))
        image = image.convert()
        image_rect = image.get_rect()
        image_rect.center = [400, 300]
        self.background.blit(image, image_rect)
        pygame.display.flip()
        self.event_manager.unregister_listener(self)

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
        elif isinstance(event, events.GameOverEvent):
            self.game_over(event.win)
        elif isinstance(event, events.ControlPadEvent):
            if event.left:
                self.pad_left.pos =  event.pos
            else:
                self.pad_right.pos =  event.pos
