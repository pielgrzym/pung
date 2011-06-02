class Event(object):
    """
    Event masterclass
    """
    def __init__(self):
        self.name = "Generic Event"

class PauseEvent(Event):
    pass

class TickEvent(Event):
    pass

class QuitEvent(Event):
    pass

class RegisterSurfaceEvent(Event):
    """
    Register surface for constant re-blitting into screen
    """
    def __init__(self, surface):
        if not isinstance(surface, list) or len(surface) < 2:
            surface = [surface, surface.get_rect()]
        self.surface = surface
        self.name = "Register surface"

class BlitRequestEvent(Event):
    def __init__(self, surface_name, element, element_rect):
        """
        Used to call View and blit an element into surface accessible only from
        view
    
        """
    
        self.surface_name = surface_name
        self.element = element
        self.element_rect = element_rect

class ModifyScoreEvent(Event):
    def __init__(self, player=0, ai=0):
        """
        Adds some score
    
        """
        self.ai = ai
        self.player = player

class GameOverEvent(Event):
    def __init__(self, win=True):
        self.win = win

class ControlPadEvent(Event):
    def __init__(self, pos, left=False):
        self.left = left
        self.pos = pos[1]

class BallMoveEvent(Event):
    def __init__(self, coords):
        """
        Ball movement event - for ai to determine next move

        """

        self.coords = coords
        self.x, self.y = coords

class PadMoveEvent(Event):
    def __init__(self, coords, right=0):
        """
        Ball movement event - for ai to determine next move

        """

        self.coords = coords
        self.x, self.y = coords
        self.right = right
