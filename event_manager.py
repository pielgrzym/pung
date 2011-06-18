class EventManager(object):
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    def register_listener(self, listener):
        """
        Register new listener

        """

        self.listeners[listener] = 1

    def unregister_listener(self, listener):
        """
        Unregister existing listener

        """

        if listener in self.listeners.keys():
            del self.listeners[listener]

    def post(self, event):
        """
        Post new event

        """

        for listener in self.listeners.keys():
            listener.notify(event)

event_manager = EventManager()
