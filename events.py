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
    Register surface for direct blitting into screen
    """
    def __init__(self, surface):
        if not isinstance(surface, list) or len(surface) < 2:
            surface = [surface, surface.get_rect()]
        self.surface = surface
        self.name = "Register surface"

class InputEvent(Event):
    def __init__(self, event):
        """
        docstring
    
        """
    
        self.event = event
