from event.rate_limit import rate_limit
from glbl.PinState import PinState
import threading

class EventManager:

    def start(self):
        self._run()

    def stop(self):
        self._please_stop()

    def dropHandlers(self):
        self._reset_events()

    def registerHandler(self, listener):
        self._add_listener(listener)

    ############# PRIVATE SECTION ################

    # signal to ask event loop to end 
    _wantStop = True

    # link to the current instance (for singleton)
    _instance = None

    # link to the current thread 
    _thread: threading.Thread = None

    # start event handling if not started yet
    def _run(self):
        if not self._thread.is_alive():
            self._thread.start()

    # clear all bindings ( when move from screen to screen )
    def _reset_events(self):
        self.listeners = []         

    # add binding - key_event(pin, state), can handle all buttons in one func, can be splitted
    def _add_listener(self, listener):
        self.listeners.append(listener)

    # mark as 'want to stop'. Event will stop its processing on the next loop iteration
    def _please_stop(self):
        self._wantStop = True

    # singleton-related
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EventManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # prepare all fields
    def __init__(self):
        # prevent constuctor from call several time
        if not hasattr(self, 'initialized'):
            self.listeners = []
            self.initialized = True
            self._thread = threading.Thread(target=self._loop)

    @rate_limit(calls_per_second=50)
    def notify(self, pin, state):
        for listener in self.listeners:
            listener(pin, state)

    # event manager loop
    def _loop(self):
        # global singleton, hold all current buttons state
        state = PinState()
        while not self._wantStop:
            for pin in state.all():
                if input(pin) != state.get(pin):
                    state.set(pin, input(pin))
                    self.notify(pin, state.get(pin))